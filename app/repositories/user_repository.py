from app.utils.security import get_password_hash, verify_password
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.user import User, UserLanguage  # Fixed import
from app.utils.security import generate_password_hash, verify_password  # Fixed imports

class UserRepository:
    """
    Repository pentru operațiuni legate de utilizatori.
    """

    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]) -> User:
        """
        Creează un nou utilizator în baza de date.

        Args:
            db: Sesiunea de bază de date.
            user_data: Dicționar cu datele utilizatorului.

        Returns:
            Obiectul utilizator creat.
        """
        # Securizarea parolei înainte de salvare
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))

        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Obține un utilizator după ID.

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului căutat.

        Returns:
            Obiectul utilizator sau None dacă nu există.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Obține un utilizator după adresa de email.

        Args:
            db: Sesiunea de bază de date.
            email: Adresa de email căutată.

        Returns:
            Obiectul utilizator sau None dacă nu există.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Obține un utilizator după numele de utilizator.

        Args:
            db: Sesiunea de bază de date.
            username: Numele de utilizator căutat.

        Returns:
            Obiectul utilizator sau None dacă nu există.
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[User]:
        """
        Obține o listă de utilizatori.

        Args:
            db: Sesiunea de bază de date.
            skip: Numărul de înregistrări de sărit.
            limit: Numărul maxim de înregistrări de returnat.
            active_only: Dacă se returnează doar utilizatorii activi.

        Returns:
            Lista de utilizatori.
        """
        query = db.query(User)
        if active_only:
            query = query.filter(User.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Actualizează datele unui utilizator.

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului de actualizat.
            update_data: Dicționar cu datele de actualizat.

        Returns:
            Obiectul utilizator actualizat sau None dacă utilizatorul nu există.
        """
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return None

        # Gestionarea parolei dacă este inclusă în actualizare
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Șterge un utilizator din baza de date.

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului de șters.

        Returns:
            True dacă utilizatorul a fost șters, False altfel.
        """
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
        """
        Autentifică un utilizator folosind numele de utilizator sau email-ul și parola.

        Args:
            db: Sesiunea de bază de date.
            username_or_email: Numele de utilizator sau email-ul pentru autentificare.
            password: Parola pentru autentificare.

        Returns:
            Obiectul utilizator autentificat sau None dacă autentificarea eșuează.
        """
        user = db.query(User).filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> Optional[User]:
        """
        Dezactivează un utilizator (alternative la ștergerea permanentă).

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului de dezactivat.

        Returns:
            Obiectul utilizator dezactivat sau None dacă utilizatorul nu există.
        """
        return UserRepository.update_user(db, user_id, {"is_active": False})

    @staticmethod
    def add_user_language(db: Session, user_id: int, language_data: Dict[str, Any]) -> Optional[UserLanguage]:
        """
        Adaugă o limbă de învățare pentru un utilizator.

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului.
            language_data: Dicționar cu datele limbii.

        Returns:
            Obiectul UserLanguage creat sau None dacă utilizatorul nu există.
        """
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return None

        language_data["user_id"] = user_id
        user_language = UserLanguage(**language_data)

        db.add(user_language)
        db.commit()
        db.refresh(user_language)
        return user_language

    @staticmethod
    def get_user_languages(db: Session, user_id: int) -> List[UserLanguage]:
        """
        Obține toate limbile de învățare ale unui utilizator.

        Args:
            db: Sesiunea de bază de date.
            user_id: ID-ul utilizatorului.

        Returns:
            Lista de limbi de învățare ale utilizatorului.
        """
        return db.query(UserLanguage).filter(UserLanguage.user_id == user_id).all()

    @staticmethod
    def update_user_language(db: Session, user_language_id: int, update_data: Dict[str, Any]) -> Optional[UserLanguage]:
        """
        Actualizează informațiile despre limba de învățare a unui utilizator.

        Args:
            db: Sesiunea de bază de date.
            user_language_id: ID-ul relației UserLanguage.
            update_data: Dicționar cu datele de actualizat.

        Returns:
            Obiectul UserLanguage actualizat sau None dacă nu există.
        """
        user_language = db.query(UserLanguage).filter(UserLanguage.id == user_language_id).first()
        if not user_language:
            return None

        for key, value in update_data.items():
            setattr(user_language, key, value)

        db.commit()
        db.refresh(user_language)
        return user_language

    @staticmethod
    def delete_user_language(db: Session, user_language_id: int) -> bool:
        """
        Șterge o limbă din lista de limbi de învățare a unui utilizator.

        Args:
            db: Sesiunea de bază de date.
            user_language_id: ID-ul relației UserLanguage.

        Returns:
            True dacă limba a fost ștearsă, False altfel.
        """
        user_language = db.query(UserLanguage).filter(UserLanguage.id == user_language_id).first()
        if not user_language:
            return False

        db.delete(user_language)
        db.commit()
        return True

    @staticmethod
    def add_user_language(db: Session, user_id: int, language_data: Dict[str, Any]) -> Optional[UserLanguage]:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return None

        language = UserLanguage(
            user_id=user_id,
            language=language_data['language'],
            level=language_data.get('level', 'beginner')
        )
        db.add(language)
        db.commit()
        db.refresh(language)
        return language
    @staticmethod
    def search_users(db: Session, query: str, limit: int = 20) -> List[User]:
        """
        Caută utilizatori după numele de utilizator, email, prenume sau nume.

        Args:
            db: Sesiunea de bază de date.
            query: Șirul de căutare.
            limit: Numărul maxim de rezultate.

        Returns:
            Lista de utilizatori care se potrivesc cu criteriile de căutare.
        """
        search_pattern = f"%{query}%"
        return db.query(User).filter(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern)
            )
        ).limit(limit).all()