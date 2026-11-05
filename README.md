# Meeting Audio to Structured Meeting Minutes

## Project Overview

Meeting Audio to Structured Meeting Minutes is a Python-based application that converts recorded meeting audio into readable transcripts and structured meeting minutes. It helps users identify discussion topics, decisions, action items, responsible people, and deadlines.

Users can review and edit the transcript and generated minutes before downloading the final document as an editable Microsoft Word file.

## Features

- Upload meeting recordings in WAV, MP3, and M4A formats.
- Validate audio files and reject unsupported, empty, corrupted, or oversized files.
- Transcribe speech using Faster-Whisper.
- Review and edit the generated transcript.
- Extract discussion topics, decisions, and action items.
- Identify owners and deadlines when supported by the transcript.
- Flag missing or ambiguous information for human review.
- Edit structured meeting minutes before export.
- Download the final minutes as an editable DOCX file.

## Technology Stack

- **Language:** Python
- **User Interface:** Streamlit
- **Speech Transcription:** Faster-Whisper
- **Document Export:** python-docx
- **Testing:** pytest and Python unittest-compatible tests

## Requirements

- Windows 11 or a compatible operating system.
- Python 3.11 recommended.
- Internet connection for the initial download of the transcription model.
- Sufficient memory and processing resources for audio transcription.

## Installation

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit application from the project root:

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal.

### Using the Application

1. Upload a supported meeting audio file.
2. Validate the uploaded recording.
3. Transcribe the audio.
4. Review and correct the transcript.
5. Generate the meeting minutes.
6. Review and edit topics, decisions, action items, owners, and deadlines.
7. Save the edited minutes.
8. Download the final minutes as a Word document.

The application may need to download the speech-recognition model during its first transcription.

## Running Tests

Run the complete automated test suite:

```powershell
python -m pytest -v
```

The tests cover audio validation, transcription behavior, minutes extraction, and the original extraction functionality.

## Responsible Information Extraction

The application is intended to assist with meeting documentation. Automatically extracted content should be reviewed before use. Missing or ambiguous owners and deadlines should be confirmed by the user rather than assumed.

## Project Scope

The application processes uploaded recordings. It is intended as a meeting-minutes prototype, not a live meeting recorder. The quality of the transcript and extracted minutes depends on audio clarity and the content of the recording.

## Project Documentation

The repository includes the Software Requirements Specification (SRS), Software Architecture Document (SAD), and Software Test Plan (STP) for the project.
