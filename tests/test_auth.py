import unittest
from app import create_app
from app.models.user import User
from app import db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_register(self):
        response = self.client.post('/api/auth/register', json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "parola123"
        })
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()