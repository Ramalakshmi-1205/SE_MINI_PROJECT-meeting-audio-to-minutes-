
import os
import tempfile
import unittest
from types import SimpleNamespace

from validated_audio import cleanup_audio


class TestAudioCleanup(unittest.TestCase):

    def test_cleanup_deletes_temporary_audio_file(self):
        # Create a temporary file for testing.
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(b"test audio data")

        self.assertTrue(os.path.exists(temp_path))

        # Simulate a validated audio object.
        audio = SimpleNamespace(path=temp_path)

        # Run cleanup.
        cleanup_audio(audio)

        # Verify that the file has been deleted.
        self.assertFalse(os.path.exists(temp_path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
