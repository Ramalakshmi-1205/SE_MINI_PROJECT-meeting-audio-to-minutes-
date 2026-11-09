# Demo Safety Checklist (DEMO-02)

Run through this the day before the demo and again 10 minutes before presenting.

Demo date: ______  Checked by: ______

## Demo recording
- [ ] The audio is a made-up meeting recorded by the team for the demo, not a real class, lab or project meeting.
- [ ] Everyone whose voice is in the recording agreed to it being played.
- [ ] The recording mentions no real phone numbers, emails, addresses, marks or other personal details.
- [ ] It is under 10 minutes and in WAV, MP3 or M4A format.
- [ ] A spare synthetic recording is ready in case the first one fails.

## Laptop and screen
- [ ] Close email, WhatsApp, chats and any browser tabs not needed for the demo.
- [ ] Turn off notifications (Windows: Focus assist / Do not disturb).
- [ ] The file picker opens in a demo folder, not Downloads, Desktop or a folder showing private file names.
- [ ] The terminal running `streamlit run app.py` shows no tokens, passwords or private paths; minimise it while presenting.
- [ ] Browser autofill and saved-password pop-ups are off for the demo profile.

## App behaviour
- [ ] `.streamlit/config.toml` has `showErrorDetails = "none"`, so any unexpected error shows no code or paths.
- [ ] Run the full flow once: validate, transcribe, generate, edit, save, download.
- [ ] Show one error case on purpose (for example an unsupported file) and confirm the message is plain and helpful.
- [ ] Open the downloaded Word file and confirm it contains only the demo content.
- [ ] Delete leftover demo downloads and temporary files afterwards.

## Slides and handouts
- [ ] Screenshots in slides contain no keys, private paths, real names outside the team, or real meeting content.
- [ ] Any CI or test-result screenshot is from a current run, with its date visible.
