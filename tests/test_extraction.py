import unittest

from app.extraction import extract_minutes


class TestExtractMinutes(unittest.TestCase):

    def test_empty_transcript(self):
        result = extract_minutes("")

        self.assertEqual(result["topics"], [])
        self.assertEqual(result["decisions"], [])
        self.assertEqual(result["action_items"], [])
        self.assertTrue(result["review_flags"])

    def test_non_string_transcript(self):
        result = extract_minutes(None)

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

        item = result["action_items"][0]
        self.assertIsNone(item["owner"])
        self.assertIsNone(item["deadline"])

    def test_missing_owner(self):
        transcript = "The team will prepare the report by Monday."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)
        item = result["action_items"][0]

        self.assertIsNone(item["owner"])
        self.assertEqual(item["deadline"], "Monday")
        self.assertTrue(any(
            "Owner needs review" in flag
            for flag in result["review_flags"]
        ))

    def test_missing_deadline(self):
        transcript = "Priya will prepare the report."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)
        item = result["action_items"][0]

        self.assertEqual(item["owner"], "Priya")
        self.assertIsNone(item["deadline"])
        self.assertTrue(any(
            "Deadline needs review" in flag
            for flag in result["review_flags"]
        ))

    def test_duplicate_topics_and_decisions(self):
        transcript = (
            "We discussed the project timeline. "
            "We discussed the project timeline. "
            "We decided to move the meeting. "
            "We decided to move the meeting."
        )

        result = extract_minutes(transcript)

        self.assertEqual(len(result["topics"]), 1)
        self.assertEqual(len(result["decisions"]), 1)

    def test_duplicate_action_items(self):
        transcript = (
            "Priya will prepare the report. "
            "Priya will prepare the report."
        )

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)

    def test_imperative_action_item(self):
        transcript = "Prepare the presentation by Tuesday."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)
        item = result["action_items"][0]

        self.assertEqual(item["task"], "Prepare the presentation")
        self.assertIsNone(item["owner"])
        self.assertEqual(item["deadline"], "Tuesday")

    def test_multiple_action_items(self):
        transcript = (
            "Priya will prepare the report by Monday. "
            "Ravi will review the presentation by Tuesday."
        )

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 2)

    def test_discussion_not_misclassified_as_decision(self):
        transcript = (
            "We discussed the project budget. "
            "The team talked about the launch schedule."
        )

        result = extract_minutes(transcript)

        self.assertEqual(result["decisions"], [])

    def test_unrelated_sentence_not_topic(self):
        transcript = "The weather is pleasant today."

        result = extract_minutes(transcript)

        self.assertEqual(result["topics"], [])

    def test_deadline_with_month_and_day(self):
        transcript = "Priya will submit the report by November 12."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)
        self.assertEqual(
            result["action_items"][0]["deadline"],
            "November 12"
        )

    def test_same_task_with_different_owners(self):
        transcript = (
            "Priya will prepare the report. "
            "Ravi will prepare the report."
        )

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 2)


if __name__ == "__main__":
    unittest.main()
