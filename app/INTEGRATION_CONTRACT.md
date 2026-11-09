
# Integration Contract — Meeting Audio to Structured Minutes

## 1. Purpose

This document defines the interface between the transcript extraction module and the meeting minutes export module.

The integration layer will be maintained separately by the project lead.

## 2. Transcript Input

The extraction module accepts a plain Python string.

Function:

    extract_minutes(transcript)

Example:

    transcript = """
    We discussed the project timeline.
    The team decided to use Python.
    Priya will complete testing by Friday.
    """

Speaker names, when available, remain part of the transcript text.

Separate timestamp and speaker structures are not currently used.

## 3. Extraction Output

The function returns a Python dictionary with three main fields:

- topics
- decisions
- action_items

Each action item contains:

- task: description of the task
- owner: responsible person's name, or None
- deadline: stated deadline, or None

Duplicate action items are removed during extraction.

Action-item detection supports common action keywords and imperative verbs.

## 4. Sample Output

For the sample transcript above, the expected output is:

    {
        "topics": [
            "We discussed the project timeline."
        ],
        "decisions": [
            "The team decided to use Python."
        ],
        "action_items": [
            {
                "task": "complete testing",
                "owner": "Priya",
                "deadline": "Friday"
            }
        ]
    }

## 5. Missing Information

The extraction module uses None when an owner or deadline is not identified.

Example:

    {
        "task": "prepare the report",
        "owner": None,
        "deadline": None
    }

The module must not invent missing owners or deadlines.

The current output does not contain a separate review_flags field.

## 6. Export Module

The export module accepts the structured minutes dictionary and an output path.

Function:

    export_minutes(minutes, output_path, file_format=None)

Supported formats:

- TXT
- DOCX

Example:

    export_minutes(minutes, "meeting_minutes.docx")

The format can be inferred from the output file extension.

## 7. Export Behaviour

The exporter generates the following sections:

1. Meeting Minutes
2. Discussion Topics
3. Decisions
4. Action Items

Missing action-item values are displayed as:

- Missing task: Not specified
- Missing owner: Not specified
- Missing deadline: Not specified

Empty sections are displayed as "None recorded."

The DOCX output is editable.

## 8. Module Responsibilities

| Module | Responsibility |
|---|---|
| app/extraction.py | Extract topics, decisions and action items |
| app/export_minutes.py | Export structured minutes to TXT or DOCX |
| Integration/orchestration layer | Connect transcript input, extraction and export |

## 9. Current Limitations

- Extraction is rule-based and uses keywords and regular expressions.
- Complex or ambiguous ownership may not be identified correctly.
- Deadline recognition is limited to supported text patterns.
- Action-item detection supports common imperative verbs but may not recognize unusual wording.
- Duplicate action items are removed during extraction.
- Missing values are represented using None in the extraction output.
- Human review is required to verify generated minutes.

## 10. Integration Notes

- The orchestration layer should pass the transcript as a plain Python string.
- The extraction output should be passed directly to the exporter.
- The agreed dictionary structure should not be changed without coordination with the project lead.
- Integration testing should initially use a deterministic fake transcript.
- The integration layer is responsible for handling application-level success and empty-extraction messages.
