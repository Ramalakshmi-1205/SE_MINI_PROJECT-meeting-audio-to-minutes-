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

    def sample_minutes(self):
        return {
            "topics": ["Project progress discussion"],
            "decisions": ["Submission finalized for Friday"],
            "action_items": [
                {
                    "task": "Complete documentation",
                    "owner": "Priya",
                    "deadline": "Thursday"
                },
                {
                    "task": "Review testing",
                    "owner": None,
                    "deadline": None
                }
            ]
        }

    # 1. TXT export
    def test_txt_export(self):
        minutes = self.sample_minutes()

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "minutes.txt"
            result = export_minutes(minutes, output)

            self.assertTrue(Path(result).exists())
            content = output.read_text(encoding="utf-8")

            self.assertIn("MEETING MINUTES", content)
            self.assertIn("DISCUSSION TOPICS", content)
            self.assertIn("DECISIONS", content)
            self.assertIn("ACTION ITEMS", content)
            self.assertIn("Complete documentation", content)
            self.assertIn("Priya", content)
            self.assertIn("Thursday", content)
            self.assertIn("Owner: Not specified", content)
            self.assertNotIn("Not assigned", content)

    # 2. DOCX export
    def test_docx_export(self):
        minutes = self.sample_minutes()

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "minutes.docx"
            result = export_minutes(minutes, output)

            self.assertTrue(Path(result).exists())
            text = self.read_docx_text(output)

            self.assertIn("Meeting Minutes", text)
            self.assertIn("Discussion Topics", text)
            self.assertIn("Decisions", text)
            self.assertIn("Action Items", text)
            self.assertIn("Complete documentation", text)
            self.assertIn("Owner: Priya", text)
            self.assertIn("Not specified", text)
            self.assertNotIn("Not assigned", text)

    # 3. Each task must retain its correct owner and deadline
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
            output = Path(temp_dir) / "minutes.docx"
            export_minutes(minutes, output)
            text = self.read_docx_text(output)

            self.assertIn("Discussion Topics", text)
            self.assertIn("Decisions", text)
            self.assertIn("Action Items", text)
            self.assertIn("Prepare the budget", text)
            self.assertIn("Owner: Priya", text)
            self.assertIn("Deadline: Monday", text)
            self.assertIn("Review the design", text)
            self.assertIn("Owner: Sam", text)
            self.assertIn("Deadline: Tuesday", text)

    # 4. Empty sections in DOCX
    def test_empty_sections_are_shown_in_docx(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "empty_minutes.docx"
            export_minutes(minutes, output)
            text = self.read_docx_text(output)

            self.assertEqual(text.count("None recorded."), 3)

    # 5. Empty minutes in TXT and DOCX
    def test_empty_minutes_export(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": []
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            txt_output = Path(temp_dir) / "empty.txt"
            docx_output = Path(temp_dir) / "empty.docx"

            export_minutes(minutes, txt_output)
            export_minutes(minutes, docx_output)

            txt_content = txt_output.read_text(encoding="utf-8")
            docx_content = self.read_docx_text(docx_output)

            self.assertEqual(txt_content.count("None recorded."), 3)
            self.assertEqual(docx_content.count("None recorded."), 3)

    # 6. Missing owner and deadline
    def test_missing_owner_and_deadline_are_shown(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [
                {
                    "task": "Share the notes",
                    "owner": None,
                    "deadline": None
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing_values.docx"
            export_minutes(minutes, output)
            text = self.read_docx_text(output)

            self.assertIn("Share the notes", text)
            self.assertIn("Owner: Not specified", text)
            self.assertIn("Deadline: Not specified", text)
            self.assertNotIn("Not assigned", text)

    # 7. Unicode DOCX export
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
            output = Path(temp_dir) / "unicode_minutes.docx"
            export_minutes(minutes, output)
            text = self.read_docx_text(output)

            self.assertIn("Café budget review", text)
            self.assertIn("Prepare the ₹ report", text)

    # 8. Unicode TXT export
    def test_unicode_txt_export(self):
        minutes = {
            "topics": ["Project discussion – Bengaluru"],
            "decisions": ["Review completed ✓"],
            "action_items": []
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "unicode.txt"
            export_minutes(minutes, output)
            content = output.read_text(encoding="utf-8")

            self.assertIn("Bengaluru", content)
            self.assertIn("✓", content)

    # 9. Missing owner terminology in TXT
    def test_missing_owner_txt_export(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [
                {
                    "task": "Prepare presentation",
                    "owner": None,
                    "deadline": "Tuesday"
                }
            ]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing_owner.txt"
            export_minutes(minutes, output)
            content = output.read_text(encoding="utf-8")

            self.assertIn("Owner: Not specified", content)
            self.assertNotIn("Not assigned", content)

    # 10. Missing owner terminology in DOCX
    def test_missing_owner_docx_export(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [
                {
                    "task": "Prepare presentation",
                    "owner": None,
                    "deadline": "Tuesday"
                }
            ]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing_owner.docx"
            export_minutes(minutes, output)
            content = self.read_docx_text(output)

            self.assertIn("Owner: Not specified", content)
            self.assertNotIn("Not assigned", content)

    # 11. Unsupported file format
    def test_unsupported_format_raises_value_error(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "minutes.pdf"

            with self.assertRaises(ValueError):
                export_minutes(minutes, output)

    # 12. Invalid DOCX output folder
    def test_invalid_output_folder_raises_file_error(self):
        minutes = {
            "topics": [],
            "decisions": [],
            "action_items": [],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing_folder" / "minutes.docx"

            with self.assertRaises(OSError):
                export_minutes(minutes, output)

    # 13. Invalid TXT output folder
    def test_invalid_txt_output_path(self):
        minutes = self.sample_minutes()

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing_folder" / "minutes.txt"

            with self.assertRaises(OSError):
                export_minutes(minutes, output)


if __name__ == "__main__":
    unittest.main()