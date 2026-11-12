
import os
import tempfile
import unittest
from types import SimpleNamespace

from validated_audio import cleanup_audio


class TestAudioCleanup(unittest.TestCase):

    def test_cleanup_deletes_temporary_audio_file(self):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(b"test audio data")

        audio = SimpleNamespace(path=temp_path)

        cleanup_audio(audio)

        self.assertFalse(os.path.exists(temp_path))

    def test_cleanup_handles_already_deleted_file(self):
        audio = SimpleNamespace(path="nonexistent_audio_file.wav")

        cleanup_audio(audio)

        self.assertFalse(os.path.exists(audio.path))

    def test_cleanup_handles_missing_path(self):
        audio = SimpleNamespace(path=None)

        cleanup_audio(audio)

        self.assertIsNone(audio.path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
