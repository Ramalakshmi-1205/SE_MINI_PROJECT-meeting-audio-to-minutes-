import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from transcription import TranscriptionAdapter, TranscriptResult


class TestTranscriptionAdapter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.audio_path = Path(self.temp_dir.name) / "sample.wav"
        self.audio_path.write_bytes(b"fake audio data")

        self.valid_audio = SimpleNamespace(
            valid=True,
            path=str(self.audio_path),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_rejects_unvalidated_audio(self):
        adapter = TranscriptionAdapter()

        invalid_audio = SimpleNamespace(
            valid=False,
            path=str(self.audio_path),
        )

        with self.assertRaises(ValueError):
            adapter.transcribe(invalid_audio)

    def test_rejects_missing_audio_file(self):
        adapter = TranscriptionAdapter()

        missing_audio = SimpleNamespace(
            valid=True,
            path=str(Path(self.temp_dir.name) / "missing.wav"),
        )

        with self.assertRaises(ValueError):
            adapter.transcribe(missing_audio)

    @patch.object(TranscriptionAdapter, "load_model")
    def test_returns_transcript_successfully(self, mock_load_model):
        adapter = TranscriptionAdapter()
        adapter.model = MagicMock()

        adapter.model.transcribe.return_value = (
            [
                SimpleNamespace(text=" Hello everyone. "),
                SimpleNamespace(text=" Today's meeting starts now. "),
                SimpleNamespace(text=" "),
            ],
            SimpleNamespace(duration=12.5),
        )

        result = adapter.transcribe(self.valid_audio)

        self.assertIsInstance(result, TranscriptResult)
        self.assertEqual(
            result.text,
            "Hello everyone. Today's meeting starts now.",
        )
        self.assertEqual(
            result.status,
            "Transcription completed successfully.",
        )
        self.assertEqual(result.duration, 12.5)
        mock_load_model.assert_called_once()

    @patch.object(TranscriptionAdapter, "load_model")
    def test_handles_audio_with_no_recognized_speech(self, mock_load_model):
        adapter = TranscriptionAdapter()
        adapter.model = MagicMock()

        adapter.model.transcribe.return_value = (
            [SimpleNamespace(text=" "), SimpleNamespace(text="")],
            SimpleNamespace(duration=3.0),
        )

        result = adapter.transcribe(self.valid_audio)

        self.assertEqual(result.text, "")
        self.assertEqual(
            result.status,
            "No speech could be recognized.",
        )
        self.assertEqual(result.duration, 3.0)

    @patch.object(TranscriptionAdapter, "load_model")
    def test_handles_transcription_failure(self, mock_load_model):
        adapter = TranscriptionAdapter()
        adapter.model = MagicMock()
        adapter.model.transcribe.side_effect = Exception("Test error")

        with self.assertRaisesRegex(RuntimeError, "Transcription failed"):
            adapter.transcribe(self.valid_audio)


    @patch.dict("sys.modules", {"av": None, "faster_whisper": None})
    def test_handles_missing_transcription_dependencies(self):
        adapter = TranscriptionAdapter()

        with self.assertRaisesRegex(
            RuntimeError,
            "Faster-Whisper or PyAV is not installed correctly",
        ):
            adapter.load_model()



    def test_handles_model_loading_failure(self):
        fake_av = SimpleNamespace(open=MagicMock())

        fake_whisper = SimpleNamespace(
            WhisperModel=MagicMock(
                side_effect=Exception("Model initialization failed")
            )
        )

        with patch.dict(
            "sys.modules",
            {
                "av": fake_av,
                "faster_whisper": fake_whisper,
            },
        ):
            adapter = TranscriptionAdapter()

            with self.assertRaisesRegex(
                RuntimeError,
                "Could not load the transcription model",
            ):
                adapter.load_model()





if __name__ == "__main__":
    unittest.main()
