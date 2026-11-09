import hashlib
import tempfile
from pathlib import Path

import streamlit as st

from validated_audio import validate_and_save, cleanup_audio
from transcription import TranscriptionAdapter
from minutes_extractor import ActionItem, MinutesDraft
from minutes_editor import MinutesEditor

from app.extraction import extract_minutes
from app.export_minutes import export_minutes


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Meeting Audio to Structured Minutes",
    page_icon="🎙️",
    layout="wide",
)

st.title("Meeting Audio to Structured Minutes")

st.write(
    "Upload a meeting recording to generate a transcript, "
    "review the minutes, and download an editable Word document."
)

st.info(
    "Supported formats: WAV, MP3, M4A. "
    "Maximum file size: 100 MB."
)


# --------------------------------------------------
# Session-state initialization
# --------------------------------------------------

if "validated_audio_path" not in st.session_state:
    st.session_state["validated_audio_path"] = None

if "validated_audio_name" not in st.session_state:
    st.session_state["validated_audio_name"] = None

if "validated_audio_signature" not in st.session_state:
    st.session_state["validated_audio_signature"] = None

if "minutes_draft" not in st.session_state:
    st.session_state["minutes_draft"] = None

if "validated_minutes" not in st.session_state:
    st.session_state["validated_minutes"] = None

if "minutes_review_flags" not in st.session_state:
    st.session_state["minutes_review_flags"] = []


def clear_minutes():
    """Clear results that belong to an earlier transcript."""
    st.session_state["minutes_draft"] = None
    st.session_state["validated_minutes"] = None
    st.session_state["minutes_review_flags"] = []


def remove_temporary_audio():
    """Delete the saved temporary audio file, if present."""
    audio_path = st.session_state.get("validated_audio_path")

    if audio_path:
        try:
            cleanup_audio(
                type(
                    "TemporaryAudio",
                    (),
                    {"path": audio_path},
                )()
            )
        except OSError:
            st.warning(
                "The temporary audio file could not be deleted. "
                "Please remove it manually if it remains on disk."
            )

    st.session_state["validated_audio_path"] = None
    st.session_state["validated_audio_name"] = None
    st.session_state["validated_audio_signature"] = None


def convert_extraction_to_draft(extraction):
    """
    Convert Priya's dictionary-based extraction result into the
    MinutesDraft/ActionItem structures used by the existing editor.
    """
    action_items = []

    for item in extraction.get("action_items", []):
        action_items.append(
            ActionItem(
                task=str(item.get("task") or "Not specified"),
                owner=str(item.get("owner") or "Not specified"),
                deadline=str(item.get("deadline") or "Not specified"),
            )
        )

    return MinutesDraft(
        topics=list(extraction.get("topics", [])),
        decisions=list(extraction.get("decisions", [])),
        action_items=action_items,
        review_flags=list(extraction.get("review_flags", [])),
    )


def validated_minutes_to_export_dict(validated):
    """Convert the editor's validated object to Priya's export format."""
    return {
        "topics": validated.topics,
        "decisions": validated.decisions,
        "action_items": [
            {
                "task": item.task,
                "owner": item.owner,
                "deadline": item.deadline,
            }
            for item in validated.action_items
        ],
    }


# --------------------------------------------------
# Audio upload and validation
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload meeting audio",
    type=["wav", "mp3", "m4a"],
    help="Choose a WAV, MP3, or M4A recording up to 100 MB.",
    max_upload_size=100,
)

if uploaded_file is not None:
    st.write(f"**File:** {uploaded_file.name}")
    st.write(
        f"**Size:** {uploaded_file.size / (1024 * 1024):.2f} MB"
    )

    # Use filename, size and content digest to identify an upload.
    uploaded_file.seek(0)
    file_digest = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
    uploaded_file.seek(0)

    current_signature = (
        uploaded_file.name,
        uploaded_file.size,
        file_digest,
    )

    previous_signature = st.session_state.get(
        "validated_audio_signature"
    )

    if (
        previous_signature is not None
        and previous_signature != current_signature
    ):
        remove_temporary_audio()
        st.session_state.pop("transcript", None)
        st.session_state.pop("transcription_status", None)
        clear_minutes()

    if st.button("Validate Audio", type="primary"):
        # Remove the previous temporary recording before replacing it.
        remove_temporary_audio()
        st.session_state.pop("transcript", None)
        st.session_state.pop("transcription_status", None)
        clear_minutes()

        try:
            uploaded_file.seek(0)
            result = validate_and_save(uploaded_file)

            if result.valid:
                st.session_state["validated_audio_path"] = result.path
                st.session_state["validated_audio_name"] = uploaded_file.name
                st.session_state["validated_audio_signature"] = (
                    current_signature
                )
                st.success(result.message)
            else:
                st.error(result.message)

        except Exception as exc:
            st.error(
                "Audio validation failed unexpectedly. "
                f"Details: {exc}"
            )

    # --------------------------------------------------
    # Transcription
    # --------------------------------------------------

    if st.button("Transcribe Audio"):
        audio_path = st.session_state.get("validated_audio_path")
        saved_signature = st.session_state.get(
            "validated_audio_signature"
        )

        if saved_signature != current_signature:
            st.warning(
                "The selected recording has changed. "
                "Please validate it again before transcription."
            )

        elif not audio_path or not Path(audio_path).is_file():
            st.warning(
                "Please validate the audio file before transcription."
            )

        else:
            clear_minutes()

            audio = type(
                "AudioForTranscription",
                (),
                {
                    "valid": True,
                    "path": audio_path,
                },
            )()

            try:
                with st.spinner(
                    "Loading the speech model and transcribing audio..."
                ):
                    adapter = TranscriptionAdapter()
                    result = adapter.transcribe(audio)

                st.session_state["transcript"] = result.text
                st.session_state["transcription_status"] = result.status

                if result.text.strip():
                    st.success(result.status)
                else:
                    st.warning(result.status)

            except Exception as exc:
                st.error(
                    "Transcription failed. Check the recording, "
                    "model installation, available memory, and "
                    "internet connection if the model is downloading. "
                    f"Details: {exc}"
                )

    # --------------------------------------------------
    # Transcript review
    # --------------------------------------------------

    if "transcript" in st.session_state:
        st.subheader("Meeting Transcript")

        edited_transcript = st.text_area(
            "Review and edit the transcript",
            value=st.session_state["transcript"],
            height=250,
            key="transcript_editor",
        )

        if edited_transcript != st.session_state["transcript"]:
            st.session_state["transcript"] = edited_transcript
            clear_minutes()

        if st.button("Generate Meeting Minutes"):
            clear_minutes()

            try:
                with st.spinner("Extracting meeting minutes..."):
                    extraction = extract_minutes(
                        st.session_state["transcript"]
                    )
                    draft = convert_extraction_to_draft(extraction)

                st.session_state["minutes_draft"] = draft
                st.session_state["minutes_review_flags"] = (
                    list(extraction.get("review_flags", []))
                )
                st.success("Draft meeting minutes generated.")

            except Exception as exc:
                st.error(
                    "Could not generate meeting minutes. "
                    "Please check the transcript and try again. "
                    f"Details: {exc}"
                )

    # --------------------------------------------------
    # Review and edit meeting minutes
    # --------------------------------------------------

    draft = st.session_state.get("minutes_draft")

    if draft is not None:
        st.subheader("Review Meeting Minutes")

        review_flags = st.session_state.get(
            "minutes_review_flags",
            draft.review_flags,
        )

        if review_flags:
            with st.expander(
                "Items that may need your review",
                expanded=True,
            ):
                for flag in review_flags:
                    st.warning(flag)

        with st.form("minutes_form"):
            title = st.text_input(
                "Meeting title",
                value=st.session_state.get(
                    "meeting_title",
                    "Meeting Minutes",
                ),
            )

            topics_text = st.text_area(
                "Topics discussed (one per line)",
                value="\n".join(draft.topics),
            )

            decisions_text = st.text_area(
                "Decisions made (one per line)",
                value="\n".join(draft.decisions),
            )

            actions_text = st.text_area(
                "Action items (one per line; "
                "use Task | Owner: name | Deadline: date)",
                value="\n".join(
                    f"{item.task} | Owner: {item.owner} | "
                    f"Deadline: {item.deadline}"
                    for item in draft.action_items
                ),
            )

            submitted = st.form_submit_button("Save Edited Minutes")

        if submitted:
            action_items = []
            parsing_errors = []

            for line_number, line in enumerate(
                actions_text.splitlines(),
                start=1,
            ):
                if not line.strip():
                    continue

                parts = line.split("|")
                task = parts[0].strip()

                if not task:
                    parsing_errors.append(
                        f"Action item on line {line_number} has no task."
                    )
                    continue

                owner = "Not specified"
                deadline = "Not specified"

                for part in parts[1:]:
                    part = part.strip()

                    if part.lower().startswith("owner:"):
                        owner = part.split(":", 1)[1].strip()

                    elif part.lower().startswith("deadline:"):
                        deadline = part.split(":", 1)[1].strip()

                action_items.append(
                    ActionItem(
                        task=task,
                        owner=owner or "Not specified",
                        deadline=deadline or "Not specified",
                    )
                )

            if parsing_errors:
                for error in parsing_errors:
                    st.error(error)
            else:
                edits = {
                    "title": title,
                    "topics": topics_text.splitlines(),
                    "decisions": decisions_text.splitlines(),
                    "action_items": action_items,
                }

                try:
                    validated = MinutesEditor.validate_and_update(
                        draft,
                        edits,
                    )

                    st.session_state["validated_minutes"] = validated
                    st.session_state["meeting_title"] = validated.title
                    st.success("Your edited minutes have been saved.")

                except (ValueError, AttributeError, TypeError) as exc:
                    st.error(
                        "The edited minutes could not be saved. "
                        f"Check the fields and try again. Details: {exc}"
                    )

        # --------------------------------------------------
        # Word document export using Priya's exporter
        # --------------------------------------------------

        validated = st.session_state.get("validated_minutes")

        if validated is not None:
            st.subheader("Download Meeting Minutes")

            try:
                export_data = validated_minutes_to_export_dict(validated)

                # Priya's exporter writes to a path, so use a temporary
                # directory and read the generated DOCX bytes for Streamlit.
                with tempfile.TemporaryDirectory() as temp_dir:
                    output_path = Path(temp_dir) / "Meeting_Minutes.docx"

                    export_minutes(
                        export_data,
                        output_path,
                        file_format="docx",
                    )

                    document_bytes = output_path.read_bytes()

                st.download_button(
                    label="Download Minutes as Word Document",
                    data=document_bytes,
                    file_name="Meeting_Minutes.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    key="download_minutes_docx",
                )

            except Exception as exc:
                st.error(
                    "The Word document could not be generated. "
                    "Please save your edited minutes again and retry. "
                    f"Details: {exc}"
                )

else:
    # Clear any previous upload's data when the uploader is empty.
    if st.session_state.get("validated_audio_path"):
        remove_temporary_audio()

    st.session_state.pop("transcript", None)
    st.session_state.pop("transcription_status", None)
    clear_minutes()
