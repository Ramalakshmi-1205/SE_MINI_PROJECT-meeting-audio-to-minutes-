# Pull Request Security and Quality Checklist

Use this for every PR into `main` (REVIEW-01). Copy the list into a PR review comment and tick what you checked. Share findings with the author; the feature owner fixes their own module.

PR: #___  Author: ______  Module: ______  Reviewer: ______  Date: ______

## Secrets and private data
- [ ] No API keys, tokens or passwords in the diff, including config files, workflow files and test output.
- [ ] No real meeting audio, transcripts or minutes added. Test data is synthetic (made-up bytes or sentences).
- [ ] No new `.wav`, `.mp3`, `.m4a`, `.docx` output or `.env` files committed by accident.
- [ ] Screenshots or logs attached to the PR show no keys, private file paths or meeting content.

## Data handling
- [ ] Uploaded audio is copied only through `validate_and_save()`, and every new temp file is deleted when no longer needed.
- [ ] Transcripts and minutes stay in `st.session_state`; nothing is written to shared files or global variables.
- [ ] No `print()` or `logging` of audio, transcripts, minutes or file paths (MM-SR-004).

## Errors and inputs
- [ ] New failure paths show a plain message to the user, never `str(exc)` from an unknown exception or a traceback.
- [ ] New inputs are checked for missing, empty, oversized or malformed values (MM-SR-005).
- [ ] Every new error path has a test.

## Dependencies
- [ ] Any new package is imported by the code, listed in `requirements.txt` with a tested range, and explained in the PR description.
- [ ] `pip-audit -r requirements.txt` reports no known vulnerabilities.

## Tests and CI
- [ ] `python -m pytest` passes locally; record the count: ___ passed.
- [ ] The GitHub Actions run on this PR is green. Link: ______
- [ ] README or test records updated if the test count or commands changed.

## Outcome
- [ ] Approved
- [ ] Changes requested. Findings filed as issues: ______
