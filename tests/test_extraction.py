import unittest

from app.extraction import extract_minutes


class TestExtractMinutes(unittest.TestCase):

    def test_empty_transcript(self):
        result = extract_minutes("")
        self.assertEqual(result["topics"], [])
        self.assertEqual(result["decisions"], [])
        self.assertEqual(result["action_items"], [])
        self.assertTrue(result["review_flags"])

    def test_extract_topics_and_decisions(self):
        transcript = (
            "We discussed the project timeline. "
            "We decided to move the meeting to Friday."
        )

        result = extract_minutes(transcript)

        self.assertTrue(result["topics"])
        self.assertTrue(result["decisions"])
        self.assertIn(
            "We decided to move the meeting to Friday.",
            result["decisions"],
        )

    def test_extract_action_owner_and_deadline(self):
        transcript = "Priya will prepare the report by Monday."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)
        item = result["action_items"][0]

        self.assertEqual(item["owner"], "Priya")
        self.assertEqual(item["deadline"], "Monday")
        self.assertIn("prepare the report", item["task"])

    def test_missing_owner_and_deadline_are_flagged(self):
        transcript = "The team will prepare the report."

        result = extract_minutes(transcript)

        self.assertIn("review_flags", result)
        self.assertTrue(result["review_flags"])



if __name__ == "__main__":
    unittest.main()
