
import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class ActionItem:
    task: str
    owner: str = "Not specified"
    deadline: str = "Not specified"


@dataclass
class MinutesDraft:
    topics: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    review_flags: List[str] = field(default_factory=list)


class MinutesExtractor:
    """Extract meeting topics, decisions, action items, and review flags."""

    ACTION_CUES = (
        "will",
        "must",
        "should",
        "need to",
        "needs to",
        "has to",
        "have to",
        "assigned to",
        "responsible for",
        "action item",
        "follow up",
        "follow-up",
        "complete",
        "finish",
        "prepare",
        "submit",
        "send",
        "create",
        "review",
        "update",
        "check",
        "schedule",
        "contact",
        "share",
        "deliver",
        "implement",
        "fix",
        "test",
        "organize",
        "organise",
    )

    DECISION_CUES = (
        "decided",
        "decision",
        "agreed",
        "approved",
        "will proceed",
        "we chose",
        "selected",
        "confirmed",
        "resolved",
    )

    TOPIC_CUES = (
        "discussed",
        "discussion",
        "topic",
        "agenda",
        "talked about",
        "reviewed",
        "covered",
        "update on",
    )

    # Recognizes deadlines with or without prepositions.
    DEADLINE_PATTERN = re.compile(
        r"\b(?:"
        r"(?:by|before|on|due\s+on|due\s+by)\s+"
        r"(?:today|tomorrow|tonight|"
        r"(?:next\s+)?(?:Monday|Tuesday|Wednesday|Thursday|"
        r"Friday|Saturday|Sunday|week|month)|"
        r"\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)(?:\s+\d{4})?|"
        r"\d{4}-\d{2}-\d{2})"
        r"|"
        r"(?:today|tomorrow|tonight|"
        r"(?:next\s+)?(?:Monday|Tuesday|Wednesday|Thursday|"
        r"Friday|Saturday|Sunday|week|month))"
        r"|"
        r"\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)(?:\s+\d{4})?"
        r"|"
        r"\d{4}-\d{2}-\d{2}"
        r")\b",
        re.IGNORECASE,
    )

    @staticmethod
    def _split_sentences(transcript: str) -> List[str]:
        """Split a transcript into sentence-like units."""
        if not transcript or not transcript.strip():
            return []

        parts = re.split(r"(?<=[.!?])\s+|\n+", transcript.strip())
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _clean_sentence(sentence: str) -> str:
        """Remove surrounding whitespace and punctuation."""
        return sentence.strip().strip(" \t\r\n.;")

    @staticmethod
    def _find_owner(sentence: str) -> str:
        """Extract a likely person name associated with an action."""
        patterns = [
            r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
            r"(?:will|must|should|needs to|need to|has to|have to)\b",
            r"\bassigned to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
            r"\bresponsible for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, sentence)
            if match:
                return match.group(1).strip()

        return "Not specified"

    @staticmethod
    def _find_deadline(sentence: str) -> str:
        """Extract a deadline without words like 'by' or 'before'."""
        match = MinutesExtractor.DEADLINE_PATTERN.search(sentence)

        if not match:
            return "Not specified"

        deadline = match.group(0).strip()

        deadline = re.sub(
            r"^(?:by|before|on|due\s+on|due\s+by)\s+",
            "",
            deadline,
            flags=re.IGNORECASE,
        )

        return deadline

    @classmethod
    def _is_action_sentence(cls, sentence: str) -> bool:
        """
        Identify action items without treating every decision as an action.

        A decision-only sentence such as:
        'The team agreed to review the final design next Monday'
        remains a decision, not an assigned action item.

        Explicit personal commitments and assignments can still be actions.
        """
        lower = sentence.lower()

        # Explicitly assigned or personally committed actions.
        explicit_commitment = re.search(
            r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+"
            r"(?:will|must|should|needs to|need to|has to|have to)\b",
            sentence,
        )

        explicit_assignment = (
            "assigned to" in lower
            or "responsible for" in lower
            or "action item" in lower
            or "follow up" in lower
            or "follow-up" in lower
        )

        if explicit_commitment or explicit_assignment:
            return True

        # Decision language alone should not create an action item.
        decision_starters = (
            "the team agreed",
            "we agreed",
            "it was agreed",
            "the team decided",
            "we decided",
            "it was decided",
            "the team approved",
            "we approved",
        )

        if lower.startswith(decision_starters):
            return False

        # Avoid converting generic agreement/approval into an action
        # unless the sentence also contains a clear assignment.
        if any(cue in lower for cue in cls.DECISION_CUES):
            if not explicit_assignment:
                return False

        return any(cue in lower for cue in cls.ACTION_CUES)

    @classmethod
    def extract(cls, transcript: str) -> MinutesDraft:
        """Extract topics, decisions, action items, and review flags."""
        result = MinutesDraft()

        if not transcript or not transcript.strip():
            result.review_flags.append(
                "Transcript is empty; review the source audio."
            )
            return result

        for sentence in cls._split_sentences(transcript):
            cleaned = cls._clean_sentence(sentence)

            if not cleaned:
                continue

            lower_sentence = cleaned.lower()

            # Extract topics.
            if any(cue in lower_sentence for cue in cls.TOPIC_CUES):
                if cleaned not in result.topics:
                    result.topics.append(cleaned)

            # Extract explicit decisions.
            is_decision = any(
                cue in lower_sentence for cue in cls.DECISION_CUES
            )

            if is_decision and cleaned not in result.decisions:
                result.decisions.append(cleaned)

            # Extract genuine action items separately.
            if cls._is_action_sentence(cleaned):
                owner = cls._find_owner(cleaned)
                deadline = cls._find_deadline(cleaned)

                duplicate = any(
                    item.task.lower() == cleaned.lower()
                    and item.owner.lower() == owner.lower()
                    and item.deadline.lower() == deadline.lower()
                    for item in result.action_items
                )

                if not duplicate:
                    result.action_items.append(
                        ActionItem(
                            task=cleaned,
                            owner=owner,
                            deadline=deadline,
                        )
                    )

        # Add review flags for missing information.
        if not result.topics:
            result.review_flags.append(
                "No clear topics were identified; review the transcript."
            )

        if not result.decisions:
            result.review_flags.append(
                "No explicit decisions were identified; confirm whether any were made."
            )

        if not result.action_items:
            result.review_flags.append(
                "No clear action items were identified; review the transcript."
            )

        for item in result.action_items:
            if item.owner == "Not specified":
                result.review_flags.append(
                    f"Action item needs an owner: {item.task}"
                )

            if item.deadline == "Not specified":
                result.review_flags.append(
                    f"Action item needs a deadline: {item.task}"
                )

        return result
