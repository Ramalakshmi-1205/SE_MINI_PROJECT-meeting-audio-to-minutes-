
import re


def extract_minutes(transcript):
    """
    Extract discussion topics, decisions, and action items
    from a meeting transcript.

    Missing or uncertain action-item details are flagged
    for human review rather than being invented.
    """

    if not isinstance(transcript, str) or not transcript.strip():
        return {
            "topics": [],
            "decisions": [],
            "action_items": [],
            "review_flags": [
                "No transcript was provided. Please review the audio transcription."
            ],
        }

    sentences = re.split(r"(?<=[.!?])\s+", transcript.strip())

    topics = []
    decisions = []
    action_items = []
    review_flags = []

    decision_keywords = [
        "decided",
        "approved",
        "agreed",
        "confirmed",
        "finalized",
    ]

    action_patterns = [
        r"\bwill\s+\w+",
        r"\bmust\s+\w+",
        r"\bneeds?\s+to\s+\w+",
        r"\bshould\s+\w+",
        r"\bresponsible\s+for\b",
        r"\bassigned\s+to\b",
    ]

    for sentence in sentences:
        text = sentence.strip()

        if not text:
            continue

        lower_text = text.lower()

        # Extract discussion topics.
        topic_keywords = [
            "discuss",
            "regarding",
            "about",
            "issue",
            "topic",
            "update",
            "review",
        ]

        if any(word in lower_text for word in topic_keywords):
            topics.append(text)

        # Extract decisions.
        if any(word in lower_text for word in decision_keywords):
            decisions.append(text)

        # Extract action items.
        if any(
            re.search(pattern, lower_text)
            for pattern in action_patterns
        ):
            owner = None
            deadline = None

            # Identify an owner when a name explicitly precedes
            # an action verb.
            owner_match = re.search(
                r"^([A-Z][a-z]+)\s+(?:will|must|should|needs?\s+to|need\s+to)\s+",
                text,
            )

            if owner_match:
                owner = owner_match.group(1)

            # Identify simple deadlines such as "by Monday"
            # or "by Monday 12".
            deadline_match = re.search(
                r"\bby\s+([A-Za-z]+(?:\s+\d{1,2})?)\b",
                text,
                re.IGNORECASE,
            )

            if deadline_match:
                deadline = deadline_match.group(1)

            task = text

            if owner_match:
                task = text[owner_match.end():]

            # Remove a recognised deadline from the task description.
            task = re.sub(
                r"\s+by\s+[A-Za-z]+(?:\s+\d{1,2})?\b",
                "",
                task,
                flags=re.IGNORECASE,
            ).strip().rstrip(".")

            action_items.append({
                "task": task,
                "owner": owner,
                "deadline": deadline,
            })

            # Flag missing information for human review.
            if owner is None:
                review_flags.append(
                    f"Owner needs review for action item: {task}"
                )

            if deadline is None:
                review_flags.append(
                    f"Deadline needs review for action item: {task}"
                )

    return {
        "topics": list(dict.fromkeys(topics)),
        "decisions": list(dict.fromkeys(decisions)),
        "action_items": action_items,
        "review_flags": list(dict.fromkeys(review_flags)),
    }
