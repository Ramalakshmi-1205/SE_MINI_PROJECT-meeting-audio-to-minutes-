

\# Test Execution Report



\## Meeting Audio to Structured Minutes



\*\*Report date:\*\* 5 November 2026



\*\*Testing responsibility:\*\* Test Plan, Validation, and Evidence



\*\*Project branch:\*\* `test/ramalakshmi-clean-validation`



\*\*Base branch:\*\* `upstream/main` (`cbb827f`)



\---



\## 1. Purpose



This report records the automated and manual testing performed on the Meeting Audio to Structured Minutes application.



It documents the test environment, execution results, observed application behavior, requirement traceability, and outstanding validation activities.



Only tests that were actually executed are marked as passed. Tests that have not been completed are explicitly identified as pending or not executed.



\## 2. Test Environment



| Item | Recorded environment |

|---|---|

| Operating system | Windows (`win32`) |

| Python version for current clean-branch verification | 3.11.9 |

| Earlier Python version tested | 3.14.6 (historical old-branch run) |

| pytest | 9.2.0 |

| Test runner | `python -m pytest -v` |

| Browser | Microsoft Edge |

| Application | Streamlit |

| Local application address | `localhost:8501` |

| Test audio | `sample\_meeting.wav` |

| Current test date | 5 November 2026 |



\*\*Environment verification:\*\*



The complete automated test suite was executed successfully on the clean validation branch using Python 3.11.9.



Python 3.11.9 matches the Python version specified by the GitHub Actions workflow.



An earlier execution on Python 3.14.6 was recorded on the previous branch. That historical result is not considered a verification of the current clean branch.



A successful GitHub Actions run has not yet been confirmed.



\## 3. Automated Test Execution Summary



\*\*Command executed:\*\*



```cmd

python -m pytest -v

```



\### Current clean-branch run: Python 3.11.9



| Metric | Result |

|---|---:|

| Tests collected | 33 |

| Passed | 33 |

| Failed | 0 |

| Skipped | 0 |

| Duration | 1.59 seconds |

| Pass rate | 100% |



\*\*Current automated execution result:\*\* All 33 tests passed on the clean validation branch using Python 3.11.9 and pytest 9.2.0.



The 100% pass rate applies only to the 33 automated tests executed. It does not represent complete STP requirement coverage or overall project quality.



\### Earlier historical run: Python 3.14.6



| Metric | Result |

|---|---:|

| Tests collected | 23 |

| Passed | 23 |

| Failed | 0 |

| Skipped | 0 |

| Duration | 0.33 seconds |

| Pass rate | 100% |



This earlier execution was performed on the previous branch and is retained for historical reference only.



\## 4. Automated Test Execution Details



The following test cases passed during the current clean-branch execution.



| Test file | Test case / method | Result |

|---|---|---|

| `test\_audio\_cleanup.py` | `test\_cleanup\_deletes\_temporary\_audio\_file` | PASS |

| `test\_audio\_validator.py` | `test\_corrupted\_audio` | PASS |

| `test\_audio\_validator.py` | `test\_empty\_file` | PASS |

| `test\_audio\_validator.py` | `test\_file\_over\_100\_mb` | PASS |

| `test\_audio\_validator.py` | `test\_supported\_wav` | PASS |

| `test\_audio\_validator.py` | `test\_unsupported\_format` | PASS |

| `test\_integration\_pipeline.py` | `test\_validated\_audio\_to\_structured\_minutes` | PASS |

| `test\_minutes\_editor\_export.py` | `test\_docx\_export\_creates\_readable\_document` | PASS |

| `test\_minutes\_editor\_export.py` | `test\_edited\_action\_item\_is\_preserved\_in\_export` | PASS |

| `test\_minutes\_editor\_export.py` | `test\_edits\_are\_saved` | PASS |

| `test\_minutes\_extractor.py` | `test\_empty\_transcript` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_action\_item` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_deadline` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_decision` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_multiple\_action\_items` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_owner` | PASS |

| `test\_minutes\_extractor.py` | `test\_extract\_topic` | PASS |

| `test\_minutes\_extractor.py` | `test\_missing\_owner\_and\_deadline` | PASS |

| `test\_transcription.py` | `test\_handles\_audio\_with\_no\_recognized\_speech` | PASS |

| `test\_transcription.py` | `test\_handles\_transcription\_failure` | PASS |

| `test\_transcription.py` | `test\_rejects\_missing\_audio\_file` | PASS |

| `test\_transcription.py` | `test\_rejects\_unvalidated\_audio` | PASS |

| `test\_transcription.py` | `test\_returns\_transcript\_successfully` | PASS |

| `tests/test\_export\_minutes.py` | `test\_docx\_keeps\_each\_task\_with\_its\_owner\_and\_deadline` | PASS |

| `tests/test\_export\_minutes.py` | `test\_empty\_sections\_are\_shown\_in\_docx` | PASS |

| `tests/test\_export\_minutes.py` | `test\_invalid\_output\_folder\_raises\_file\_error` | PASS |

| `tests/test\_export\_minutes.py` | `test\_missing\_owner\_and\_deadline\_are\_shown` | PASS |

| `tests/test\_export\_minutes.py` | `test\_unicode\_text\_is\_preserved` | PASS |

| `tests/test\_export\_minutes.py` | `test\_unsupported\_format\_raises\_value\_error` | PASS |

| `tests/test\_extraction.py` | `test\_empty\_transcript` | PASS |

| `tests/test\_extraction.py` | `test\_extract\_action\_owner\_and\_deadline` | PASS |

| `tests/test\_extraction.py` | `test\_extract\_topics\_and\_decisions` | PASS |

| `tests/test\_extraction.py` | `test\_missing\_owner\_and\_deadline\_are\_flagged` | PASS |



\### Integration Test Scope Limitation



The test `test\_validated\_audio\_to\_structured\_minutes` validates a WAV-like input and passes a simulated transcript to the minutes extractor.



It does not invoke the actual Whisper model.



Actual transcription was separately exercised during the manual application demonstration using `sample\_meeting.wav`.



\## 5. Manual Test Execution



The application was started locally using Streamlit and opened in Microsoft Edge at `localhost:8501`.



| Manual test | Procedure and observed result | Status |

|---|---|---|

| Valid audio upload | Uploaded `sample\_meeting.wav`, shown as approximately 0.48 MB. | PASS |

| Transcript display | Transcript appeared in the Meeting Transcript text area. | PASS |

| Topic extraction | Project deadline topic appeared in generated minutes. | PASS |

| Decision extraction | Decision to review the final design next Monday appeared. | PASS |

| Action item extraction | Priya's report-preparation action item appeared. | PASS |

| Owner and deadline | Owner displayed as Priya; deadline displayed as Friday. | PASS |

| Edit and save | Changed title to "Project Planning Meeting", added "Project report preparation", and received the confirmation message "Your edited minutes have been saved." | PASS |

| DOCX export | Exported Word document opened successfully and contained the edited title, topic, decision, task, owner, and deadline. | PASS |

| Corrupted audio rejection | Uploaded a text file saved with a `.wav` extension. Application displayed "The file appears corrupted or is not a valid audio file." | PASS |

| Prevent transcription before validation | Clicking Transcribe Audio before validating the selected file displayed "Please validate the currently selected file first." | PASS |

| Actual audio transcription | After restoring and validating `sample\_meeting.wav`, transcription worked correctly according to the manual demonstration. | PASS (user-confirmed) |



\## 6. STP-to-SRS Traceability and Execution Status



"Partially verified" means some relevant behavior was tested, but the complete test-case scope was not executed.



| STP test case | Requirement area | Execution status | Evidence / limitation |

|---|---|---|---|

| TC-AUD-01 | MM-F-001 supported audio upload | Partially verified | WAV upload demonstrated; MP3 and M4A not manually demonstrated. |

| TC-AUD-02 | MM-F-002 / MM-SR-005 invalid audio and file boundaries | Partially verified | Automated corrupted, empty, unsupported and over-100-MB tests passed; manual corrupted WAV rejected. Full boundary combinations not independently demonstrated in UI. |

| TC-TR-01 | MM-F-003 transcription | Partially verified | Transcription adapter unit tests passed; actual sample-audio transcription confirmed manually. |

| TC-TR-02 | MM-F-004 transcript/status visibility | Partially verified | Transcript displayed in UI; all status and edge conditions not separately exercised. |

| TC-EXT-01 | MM-F-005 topic extraction | Partially verified | Topic extraction unit test and manual sample demonstrated. |

| TC-EXT-02 | MM-F-006 decision extraction | Partially verified | Decision extraction unit test and manual sample demonstrated. |

| TC-EXT-03 | MM-F-007 multiple action items | Partially verified | Multiple-action-item unit test passed; manual sample showed one action item. |

| TC-EXT-04 | MM-F-008 owner extraction | Partially verified | Owner unit test and manual owner value demonstrated. |

| TC-EXT-05 | MM-F-009 deadline extraction | Partially verified | Deadline unit test and manual deadline value demonstrated. |

| TC-EXT-06 | MM-F-010 missing/ambiguous owner or deadline | Partially verified | Automated missing-owner/deadline test passed; broader ambiguity cases not manually tested. |

| TC-MIN-01 | MM-F-011 structured minutes | Partially verified | Topics, decisions and action items displayed in separate sections. |

| TC-EDIT-01 | MM-F-012 editing | Verified for demonstrated flow | Automated editing tests and manual save flow passed. |

| TC-EXP-01 | MM-F-013 editable DOCX export | Verified for demonstrated flow | Automated DOCX export tests passed; exported DOCX opened and displayed structured content. |

| TC-EXP-02 | MM-F-014 task-owner-deadline mapping | Verified for demonstrated flow | Automated export test and manual export retained task, owner and deadline. |

| TC-ERR-01 | MM-F-015 meaningful error handling | Partially verified | Corrupted-file and unvalidated-transcription messages observed; other error paths not fully tested. |

| TC-PERF-01 | MM-NF-001 performance | NOT EXECUTED | No timed performance test recorded. |

| TC-UX-01 | MM-NF-002 usability | Partially verified | Basic upload-to-export flow completed; formal first-time-user evaluation not performed. |

| TC-REL-01 | MM-NF-003 reliability/recovery | Partially verified | Invalid input was rejected and app remained usable; broader recovery scenarios not tested. |

| TC-MAINT-01 | MM-NF-004 maintainability/testability | Partially verified | Automated unit tests exist and passed; no formal maintainability assessment performed. |

| TC-COMP-01 | MM-NF-005 compatibility | NOT EXECUTED | Demonstrated in one Windows/Edge environment only; full compatibility matrix not tested. |

| TC-SEC-01 | MM-SR-001 secure transport | NOT EXECUTED / architecture confirmation pending | Local demonstration does not verify remote HTTPS/TLS behavior. |

| TC-SEC-02 | MM-SR-002 secret handling | NOT EXECUTED | No dedicated secrets scan or repository audit recorded. |

| TC-SEC-03 | MM-SR-003 session isolation | NOT EXECUTED | Multi-session isolation not tested. |

| TC-SEC-04 | MM-SR-004 privacy-safe logging | NOT EXECUTED | Logs were not audited for sensitive content. |

| TC-SEC-05 | MM-SR-005 file validation boundaries | Partially verified | Automated file validation tests passed; further file-boundary/security testing remains. |



\## 7. Observations and Issues to Report



\### OBS-01: File-size information mismatch



\*\*Observation:\*\* The application information banner states a maximum file size of 100 MB, while the Streamlit upload control displayed "200MB per file".



\*\*Impact:\*\* Users may receive inconsistent information about the supported upload limit.



\*\*Status:\*\* Observed; requires confirmation of the intended limit by the feature owner and alignment of the UI text/configuration.



\### OBS-02: Previous transcript remained visible after invalid file selection



\*\*Observation:\*\* After selecting an invalid audio file, the previous transcript remained visible in the transcript area.



\*\*Impact:\*\* A user could potentially mistake an earlier transcript for the result of the currently selected file.



\*\*Status:\*\* Needs investigation. This is a potential stale-state issue, not a confirmed defect until reproduced and reviewed by the feature owner.



\### OBS-03: Python version verification



\*\*Observation:\*\* Earlier local testing was performed using Python 3.14.6 on the previous branch.



\*\*Additional verification:\*\* The complete 33-test suite was subsequently executed successfully on the clean validation branch using Python 3.11.9.



\*\*Status:\*\* Local Python 3.11 verification completed. GitHub Actions execution remains to be confirmed.



\## 8. Tests and Activities Still Pending



The following activities should be completed before claiming full validation:



1\. Confirm a successful GitHub Actions run for the clean pull request.

2\. Execute remaining performance tests.

3\. Execute remaining security and session-isolation tests.

4\. Complete the compatibility test matrix.

5\. Verify MP3 and M4A uploads if they are in the supported scope.

6\. Resolve the file-size mismatch by setting max_upload_size=100 in app.py and verifying the 100 MB upload limit under US-03.

7\. Reproduce and investigate the stale-transcript observation.

8\. Perform a final privacy review of the nine manual-testing screenshots.

9\. Ensure no private audio or sensitive information is included in submitted evidence.



\### Evidence included in the clean branch



The following nine screenshots were captured during manual testing on the previous branch, restored to the clean validation branch, and verified to be present in its `evidence/` folder.



1\. `01\_automated\_tests.png`

2\. `02\_python311\_test\_results.png`

3\. `03\_valid\_audio\_validation.png`

4\. `04\_successful\_transcription.png`

5\. `05\_extracted\_meeting\_minutes.png`

6\. `06\_edited\_minutes.png`

7\. `07\_docx\_export.png`

8\. `08\_invalid\_audio\_validation.png`

9\. `09\_validation\_required\_message.png`



All nine screenshot files have been verified in the clean branch. Their contents should receive a final privacy review before submission.



\## 9. Overall Conclusion



The complete automated test suite consisting of 33 tests passed successfully on the clean validation branch using Python 3.11.9 and pytest 9.2.0.



The manual demonstration verified the main sample workflow, including audio upload, transcript display, structured minutes generation, editing, saving, and DOCX export.



Invalid audio was rejected, and transcription was blocked until validation.



The integration test validates audio input and structured extraction using a simulated transcript. Actual audio transcription was separately demonstrated manually.



These results demonstrate successful execution of the automated tests and documented manual scenarios. They do not establish that every STP requirement has passed.



Performance, security, full compatibility, MP3/M4A verification, and GitHub Actions validation remain pending. The 100 MB file-size mismatch has been resolved and verified under US-03. The possible stale-transcript behavior still requires investigation.



The report should be updated again after the pending activities are completed.

## 10. US-03: Streamlit 100 MB Upload Limit Verification

**Date:** 7 November 2026

**Branch:** `fix/ramalakshmi-upload-limit`

**Base branch:** `upstream/main` (`3ae4f0f`)

### Code change

Added `max_upload_size=100` to the `st.file_uploader()` configuration in `app.py`, aligning the Streamlit uploader limit with the existing 100 MB validator and user-facing message.

### Manual verification

| Test | Input | Expected result | Actual result |
|---|---|---|---|
| Valid upload | `sample_meeting.wav` (0.48 MB) | File accepted | Passed |
| Oversized upload | `upload_over_100mb.wav` (101 MB) | File rejected | Passed |

The oversized file displayed the Streamlit message: `File must be 100.0MB or smaller.`

### Automated verification

Command: `python -m pytest -v`

- Python: 3.11.9
- Pytest: 9.2.0
- Tests collected: 33
- Passed: 33
- Failed: 0
- Skipped: 0
- Execution time: 1.18 seconds

### Result

The US-03 upload-size correction passed both manual upload checks and the complete automated test suite. The change is ready for pull request review.
