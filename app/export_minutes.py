
from pathlib import Path


def export_minutes(minutes, output_path, file_format=None):
    """
    Export structured meeting minutes to TXT or DOCX.

    Missing values are displayed as "Not specified".
    Supports TXT and DOCX formats.
    """

    output_path = Path(output_path)
    fmt = (file_format or output_path.suffix.lstrip(".")).lower()

    if fmt not in ("txt", "docx"):
        raise ValueError("Supported formats are TXT and DOCX.")

    topics = minutes.get("topics", [])
    decisions = minutes.get("decisions", [])
    action_items = minutes.get("action_items", [])

    lines = ["MEETING MINUTES", ""]

    # Discussion Topics
    lines.append("DISCUSSION TOPICS")

    if topics:
        lines.extend(f"- {item}" for item in topics)
    else:
        lines.append("None recorded.")

    lines.append("")

    # Decisions
    lines.append("DECISIONS")

    if decisions:
        lines.extend(f"- {item}" for item in decisions)
    else:
        lines.append("None recorded.")

    lines.append("")

    # Action Items
    lines.append("ACTION ITEMS")

    if action_items:
        for item in action_items:
            task = item.get("task") or "Not specified"
            owner = item.get("owner") or "Not specified"
            deadline = item.get("deadline") or "Not specified"

            lines.append(f"- Task: {task}")
            lines.append(f"  Owner: {owner}")
            lines.append(f"  Deadline: {deadline}")
    else:
        lines.append("None recorded.")

    # Export as TXT
    if fmt == "txt":
        output_path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    # Export as DOCX
    else:
        try:
            from docx import Document
        except ImportError as exc:
            raise ImportError(
                "Install python-docx using: "
                "python3 -m pip install python-docx"
            ) from exc

        document = Document()

        document.add_heading("Meeting Minutes", level=0)

        # Discussion Topics
        document.add_heading("Discussion Topics", level=1)

        if topics:
            for item in topics:
                document.add_paragraph(
                    str(item),
                    style="List Bullet"
                )
        else:
            document.add_paragraph("None recorded.")

        # Decisions
        document.add_heading("Decisions", level=1)

        if decisions:
            for item in decisions:
                document.add_paragraph(
                    str(item),
                    style="List Bullet"
                )
        else:
            document.add_paragraph("None recorded.")

        # Action Items
        document.add_heading("Action Items", level=1)

        if action_items:
            for item in action_items:
                task = item.get("task") or "Not specified"
                owner = item.get("owner") or "Not specified"
                deadline = item.get("deadline") or "Not specified"

                document.add_paragraph(f"Task: {task}")
                document.add_paragraph(f"Owner: {owner}")
                document.add_paragraph(f"Deadline: {deadline}")
        else:
            document.add_paragraph("None recorded.")

        document.save(str(output_path))

    return str(output_path)
