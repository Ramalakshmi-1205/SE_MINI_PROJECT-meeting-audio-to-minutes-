
import unittest
from io import BytesIO

from docx import Document

from minutes_extractor import MinutesDraft, ActionItem
from minutes_editor import MinutesEditor
from docx_exporter import DocxExporter


class TestMinutesEditorAndExport(unittest.TestCase):

    def setUp(self):
        self.draft = MinutesDraft(
            topics=["Project timeline was discussed."],
            decisions=["The team decided to use Python."],
            action_items=[
                ActionItem(
                    task="Submit the report",
                    owner="Ravi",
                    deadline="by Friday"
                )
            ]
        )

    def test_edits_are_saved(self):
        edits = {
            "title": "Updated Meeting Minutes",
            "topics": ["Updated project discussion"],
            "decisions": ["Use Python for development"],
            "action_items": [
                ActionItem(
                    task="Prepare documentation",
                    owner="Priya",
                    deadline="by Monday"
                )
            ]
        }

        result = MinutesEditor.validate_and_update(
            self.draft, edits
        )

        self.assertEqual(result.title, "Updated Meeting Minutes")
        self.assertEqual(result.topics, ["Updated project discussion"])
        self.assertEqual(
            result.decisions,
            ["Use Python for development"]
        )
        self.assertEqual(
            result.action_items[0].task,
            "Prepare documentation"
        )
        self.assertEqual(result.action_items[0].owner, "Priya")
        self.assertEqual(result.action_items[0].deadline, "by Monday")

    def test_docx_export_creates_readable_document(self):
        validated = MinutesEditor.validate_and_update(self.draft)

        file_bytes = DocxExporter.export(validated)

        self.assertIsInstance(file_bytes, bytes)
        self.assertGreater(len(file_bytes), 0)

        document = Document(BytesIO(file_bytes))

        paragraph_text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

        self.assertIn("Meeting Minutes", paragraph_text)
        self.assertIn("Topics Discussed", paragraph_text)
        self.assertIn("Decisions Made", paragraph_text)
        self.assertIn("Action Items", paragraph_text)

    def test_edited_action_item_is_preserved_in_export(self):
        edits = {
            "title": "Final Minutes",
            "topics": ["Project update"],
            "decisions": ["Use Python"],
            "action_items": [
                ActionItem(
                    task="Complete final report",
                    owner="Priya",
                    deadline="by Monday"
                )
            ]
        }

        validated = MinutesEditor.validate_and_update(
            self.draft, edits
        )

        file_bytes = DocxExporter.export(validated)
        document = Document(BytesIO(file_bytes))

        table_text = [
            cell.text
            for row in document.tables[0].rows
            for cell in row.cells
        ]

        self.assertIn("Complete final report", table_text)
        self.assertIn("Priya", table_text)
        self.assertIn("by Monday", table_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
