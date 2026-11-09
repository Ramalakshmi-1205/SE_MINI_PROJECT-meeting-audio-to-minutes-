import re


def extract_minutes(transcript):
    """
    Extract discussion topics, decisions, and action items.

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

    sentences = re.split(r'(?<=[.!?])\s+', transcript.strip())

    topics = []
    decisions = []
    action_items = []
    review_flags = []

    decision_keywords = [
        "decided", "approved", "agreed",
        "confirmed", "finalized"
    ]

    action_keywords = [
        "will", "must", "need to",
        "should", "responsible for",
        "assigned to"
    ]

    imperative_verbs = [
        "prepare", "complete", "submit", "review",
        "send", "create", "update", "finish",
        "check", "organize", "schedule", "present",
        "implement", "test", "finalize", "share",
        "write", "design", "develop", "upload"
    ]

    for sentence in sentences:
        text = sentence.strip()

        if not text:
            continue

        lower_text = text.lower()

        # Extract discussion topics.
        if any(word in lower_text for word in [
            "discuss", "regarding", "about",
            "issue", "topic", "update", "review"
        ]):
            topics.append(text)

        # Extract decisions.
        if any(word in lower_text for word in decision_keywords):
            decisions.append(text)

        # Identify action-item statements.
        owner_match = re.search(
            r'^([A-Z][a-z]+)\s+(?:will|must|should|needs?\s+to|need\s+to)\s+',
            text
        )

        imperative_match = re.match(
            r'^(' + '|'.join(imperative_verbs) + r')\b',
            text,
            re.IGNORECASE
        )

        has_action_keyword = any(
            word in lower_text for word in action_keywords
        )

        if owner_match or imperative_match or has_action_keyword:
            owner = None
            deadline = None

            if owner_match:
                owner = owner_match.group(1)

            # Extract simple deadlines such as Monday or Monday 12.
            deadline_match = re.search(
                r'\bby\s+([A-Za-z]+(?:\s+\d{1,2})?)\b',
                text,
                re.IGNORECASE
            )

            if deadline_match:
                deadline = deadline_match.group(1)

            # Remove the identified owner from the task.
            task = text

            if owner_match:
                task = text[owner_match.end():]

            # Remove a recognised deadline from the task.
            task = re.sub(
                r'\s+by\s+[A-Za-z]+(?:\s+\d{1,2})?\b',
                '',
                task,
                flags=re.IGNORECASE
            ).strip().rstrip(".")

            if task:
                action_items.append({
                    "task": task,
                    "owner": owner,
                    "deadline": deadline
                })

                if owner is None:
                    review_flags.append(
                        f"Owner needs review for action item: {task}"
                    )

                if deadline is None:
                    review_flags.append(
                        f"Deadline needs review for action item: {task}"
                    )

    # Remove duplicate topics and decisions.
    topics = list(dict.fromkeys(topics))
    decisions = list(dict.fromkeys(decisions))

    # Remove duplicate action items while retaining different owners
    # or deadlines as separate assignments.
    unique_action_items = []
    seen_action_items = set()

    for item in action_items:
        key = (
            item["task"].strip().casefold(),
            (item["owner"] or "").strip().casefold(),
            (item["deadline"] or "").strip().casefold()
        )

        if key not in seen_action_items:
            seen_action_items.add(key)
            unique_action_items.append(item)

    return {
        "topics": topics,
        "decisions": decisions,
        "action_items": unique_action_items,
        "review_flags": list(dict.fromkeys(review_flags))
    }
