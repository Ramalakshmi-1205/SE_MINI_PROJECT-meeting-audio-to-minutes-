# Security and Privacy Review

Date / commit: 2026-11-09 / `main` @ `3ae4f0f` (msaanvi4/SE_MINI_PROJECT-meeting-audio-to-minutes-)
Reviewer: Rhea
Scope: Integrated Streamlit app on `main`: `app.py`, `audio_validator.py`, `validated_audio.py`, `transcription.py`, `minutes_editor.py`, `app/extraction.py`, `app/export_minutes.py`; `requirements.txt`, `.gitignore`, `.github/workflows/main.yml`, `TEST_EXECUTION_REPORT.md`, `evidence/`. Requirements checked: SRS MM-SR-001 to MM-SR-005, SAD temporary-file rules, STP TC-SEC-01 to TC-SEC-05.

All checks used synthetic audio bytes and made-up transcripts. No real recordings, transcripts or credentials were used or are recorded here. This review executes the security cases that `TEST_EXECUTION_REPORT.md` (5 Nov) lists as not executed.

## Checks performed

- **Recording/sample data handling:** No audio files are tracked. Test fixtures and the committed transcript screenshot use made-up content. Temporary audio copies have random names and owner-only permissions, but a copy stayed on disk after transcription (F-01, confirmed with a live AppTest run). `.gitignore` excluded only `sample_meeting.wav`, not audio files in general (F-09).
- **Secrets and logs:** No credentials in tracked files (grep for key, token, secret, password and common key prefixes). `.env` and `.streamlit/secrets.toml` are git-ignored. The workflow uses `contents: read` and no secrets. No `print` or `logging` in app modules; a marker sentence from a synthetic transcript did not appear in captured console or log output.
- **Input/error handling:** Extension, empty, 100 MB and file-signature checks run before processing. Five error messages appended raw exception text, which showed a file path on screen in testing (F-04). No Streamlit config, so uncaught errors would show tracebacks (F-03). Export failed on control characters (F-02).
- **Session isolation:** Two Streamlit AppTest sessions: session B saw none of session A's transcript, minutes or audio path. All meeting data is held in `st.session_state`.
- **Dependencies:** `pip-audit -r requirements.txt`: no known vulnerabilities (streamlit 1.67.0, faster-whisper 1.2.1, av 18.1.0, python-docx 1.2.0, pytest 9.2.0 resolved on 2026-11-09). Two packages are unpinned (F-06).
- **CI/static analysis:** `python -m pytest`: 33 passed on `main` (Python 3.11). The workflow finds the tests on `main`; no current Actions run is linked (F-07). No analyzer is configured. SonarCloud is not required by the SRS or STP and was not set up; awaiting course confirmation.
- **External transcription:** Not applicable. Faster-Whisper runs locally on CPU; the only network use is the one-time model download. No meeting data leaves the machine.

## STP security test results

| Case | Requirement | Result | Evidence |
|---|---|---|---|
| TC-SEC-01 | MM-SR-001 | N/A | All processing is local; no remote service configured. |
| TC-SEC-02 | MM-SR-002 | Pass | Repository scan found no credentials; secret files are git-ignored. |
| TC-SEC-03 | MM-SR-003 | Pass | Session B could not see session A's transcript, minutes or audio path (AppTest). |
| TC-SEC-04 | MM-SR-004 | Pass | No logging in app modules; synthetic transcript marker absent from captured output. |
| TC-SEC-05 | MM-SR-005 | Pass | Validator tests cover unsupported, empty, oversized and corrupted files. Signature check is basic (F-05). |

## Findings

- **Finding ID / issue:** F-01 Temporary audio stays on disk after transcription (Medium)
  - Expected and actual behavior: Expected the temp copy to be deleted once its transcript exists. Actually it was deleted only when the file was removed, replaced or re-validated, and never if the tab was closed.
  - Owner: Saanvi (integration, `app.py`, `validated_audio.py`)
  - Status and verification evidence: Fix proposed (`suggest-saanvi-F01-F04.patch`): delete after transcription; remove this app's copies older than 2 hours on each Validate click. Tests in `test_app_security.py` and `test_stale_audio_cleanup.py`. Awaiting owner review.

- **Finding ID / issue:** F-02 Word export fails when text contains a control character (Medium)
  - Expected and actual behavior: Expected invalid characters to be removed and the download to work. Actually python-docx raised `ValueError` for NUL, vertical tab and similar characters.
  - Owner: Priyanka (export, `app/export_minutes.py`)
  - Status and verification evidence: Fix proposed (`suggest-priyanka-F02.patch`). Tests in `tests/test_export_control_characters.py`. Awaiting owner review.

- **Finding ID / issue:** F-03 Uncaught errors would show full tracebacks in the browser (Low)
  - Expected and actual behavior: Expected no code or paths on screen. Actually there was no `.streamlit/config.toml`, and Streamlit's default `showErrorDetails` is `"full"`.
  - Owner: Rhea
  - Status and verification evidence: Fixed: `.streamlit/config.toml` sets `showErrorDetails = "none"` and `maxUploadSize = 100`. Test `test_project_config.py` passes. Verify on the PR's CI run.

- **Finding ID / issue:** F-04 Error messages show raw exception text (Medium)
  - Expected and actual behavior: Expected plain messages. Actually validation, transcription, generation, save and export errors appended `Details: {exc}`; in testing the page showed `Details: [Errno 13] Permission denied: '/home/student/private/meeting.wav'`.
  - Owner: Saanvi (integration, `app.py`)
  - Status and verification evidence: Fix proposed in `suggest-saanvi-F01-F04.patch`. Known user-facing messages (adapter and editor) are still shown. Tests in `test_app_security.py`. Awaiting owner review.

- **Finding ID / issue:** F-05 Audio signature check accepts some non-audio files (Low)
  - Expected and actual behavior: Expected non-audio files to be rejected at validation. Actually a renamed MP4 video passes as `.m4a`, and two MP3 sync bytes followed by junk pass as `.mp3`. Both fail later at transcription with a safe message.
  - Owner: Saanvi (audio pipeline)
  - Status and verification evidence: Open. Team to decide: add a decode check, or accept as a documented limitation (SRS asks for basic readability).

- **Finding ID / issue:** F-06 Some dependencies are unpinned (Low)
  - Expected and actual behavior: Expected tested versions or ranges. Actually `streamlit` and `python-docx` have no version, and `pytest` (test-only) is in the runtime list.
  - Owner: Saanvi (integration)
  - Status and verification evidence: Open. Suggest `streamlit>=1.67,<2` and `python-docx>=1.2,<2`. pip-audit is clean.

- **Finding ID / issue:** F-07 No current CI result is recorded (Low)
  - Expected and actual behavior: Expected a linked, passing GitHub Actions run for `main`. The test report lists GitHub Actions validation as pending.
  - Owner: Saanvi (workflow) with Ramalakshmi (records)
  - Status and verification evidence: Open. Link the run from the security-review PR here.

- **Finding ID / issue:** F-08 Test report is out of date (Low)
  - Expected and actual behavior: Expected the report to match current results. Actually it lists TC-SEC-01 to 04 as not executed and its screenshot shows 23 tests; `main` now has 33. The test screenshot also shows a local Windows user folder path.
  - Owner: Ramalakshmi (validation records)
  - Status and verification evidence: Open. Use the TC-SEC results above and a current pytest count; crop local paths from new screenshots.

- **Finding ID / issue:** F-09 Audio files were not git-ignored in general (Low)
  - Expected and actual behavior: Expected every recording format to be ignored so a private meeting cannot be committed by accident. Actually only `sample_meeting.wav` was ignored.
  - Owner: Rhea
  - Status and verification evidence: Fixed: `.gitignore` ignores `*.wav`, `*.mp3`, `*.m4a`, `*.ogg`, `*.opus`. Test `test_project_config.py` passes.

## Limitations / accepted risks

- Rhea's frontend branch (`member4-frontend-ui` on her fork) is not merged into `main` and was reviewed separately; its fixes are kept on that branch.
- GitHub Actions run history was not inspected; no CI result is claimed in this note.
- Session isolation and log checks used Streamlit AppTest, not two live browsers. Repeat TC-SEC-03 in Chrome on Windows 11 before the demo.
- No real recordings, transcripts or credentials were used or recorded in this note.
