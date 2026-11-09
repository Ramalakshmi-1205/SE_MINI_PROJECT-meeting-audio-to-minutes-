"""Security review checks on project configuration (F-03, F-09)."""

import tomllib
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def test_uncaught_errors_do_not_show_tracebacks():
    with open(PROJECT_DIR / ".streamlit" / "config.toml", "rb") as file:
        config = tomllib.load(file)

    assert config["client"]["showErrorDetails"] == "none"
    assert config["server"]["maxUploadSize"] == 100


def test_meeting_audio_files_are_never_committed():
    ignored = (PROJECT_DIR / ".gitignore").read_text().splitlines()

    for pattern in ("*.wav", "*.mp3", "*.m4a"):
        assert pattern in ignored, f"{pattern} missing from .gitignore"
