import json
from datetime import datetime
from flask import current_app
from app.models.progress import Progress
from typing import Dict, Any


class ExportService:
    @staticmethod
    def export_progress_to_json(user_id: int) -> str:
        """Export user progress to JSON format"""
        progress_entries = Progress.query.filter_by(user_id=user_id).all()

        export_data = {
            "user_id": user_id,
            "generated_at": datetime.utcnow().isoformat(),
            "progress": [
                {
                    "lesson_id": entry.lesson_id,
                    "score": entry.score,
                    "completed_at": entry.completed_at.isoformat()
                } for entry in progress_entries
            ]
        }

        return json.dumps(export_data, indent=2, ensure_ascii=False)

    @staticmethod
    def export_progress_to_csv(user_id: int) -> str:
        """Export user progress to CSV format"""
        progress_entries = Progress.query.filter_by(user_id=user_id).all()

        csv_lines = ["lesson_id,score,completed_at"]
        for entry in progress_entries:
            csv_lines.append(
                f"{entry.lesson_id},{entry.score},{entry.completed_at.isoformat()}"
            )

        return "\n".join(csv_lines)