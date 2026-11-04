import tempfile
import unittest
from pathlib import Path

from docx import Document

from app.export_minutes import export_minutes


class TestExportMinutes(unittest.TestCase):
    def read_docx_text(self, path):
        document = Document(path)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    def test_docx_keeps_each_task_with_its_owner_and_deadline(self):
        minutes = {
            "topics": ["Budget planning"],
            "decisions": ["The budget was approved."],
            "action_items": [
                {
                    "task": "Prepare the budget",
                    "owner": "Priya",
                    "deadline": "Monday",
                },
                {
                    "task": "Review the design",
                    "owner": "Sam",
                    "deadline": "Tuesday",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "minutes.docx"
            export_minutes(minutes, output_path)
            text = self.read_docx_text(output_path)

        self.assertIn("Discussion Topics", text)
        self.assertIn("Decisions", text)
        self.assertIn("Action Items", text)
        self.assertIn("Prepare the budget", text)
        self.assertIn("Owner: Priya", text)
        self.assertIn("Deadline: Monday", text)
        self.assertIn("Review the design", text)
        self.assertIn("Owner: Sam", text)
        self.assertIn("Deadline: Tuesday", text)

    def test_empty_sections_are_shown_in_docx(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "empty_minutes.docx"
            export_minutes(minutes, output_path)
            text = self.read_docx_text(output_path)

        self.assertEqual(text.count("None recorded."), 3)

    def test_missing_owner_and_deadline_are_shown(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [
                {"task": "Share the notes", "owner": None, "deadline": None}
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "missing_values.docx"
            export_minutes(minutes, output_path)
            text = self.read_docx_text(output_path)

        self.assertIn("Share the notes", text)
        self.assertIn("Owner: Not assigned", text)
        self.assertIn("Deadline: Not specified", text)

    def test_unicode_text_is_preserved(self):
        minutes = {
            "topics": ["Café budget review"],
            "decisions": [],
            "action_items": [
                {
                    "task": "Prepare the ₹ report",
                    "owner": "Priya",
                    "deadline": "Friday",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "unicode_minutes.docx"
            export_minutes(minutes, output_path)
            text = self.read_docx_text(output_path)

        self.assertIn("Café budget review", text)
        self.assertIn("Prepare the ₹ report", text)

    def test_unsupported_format_raises_value_error(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "minutes.pdf"

            with self.assertRaises(ValueError):
                export_minutes(minutes, output_path)

    def test_invalid_output_folder_raises_file_error(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "missing_folder" / "minutes.docx"

            with self.assertRaises(OSError):
                export_minutes(minutes, output_path)


if __name__ == "__main__":
    unittest.main()
