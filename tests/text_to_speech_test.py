import unittest

import model_server as ms



class TestSoundToText(unittest.TestCase):

    def test_audio_to_text(self):
        """Test to see if the transcribe_audio function returns a string"""
        self.assertIsInstance(ms.transcribe_audio("harvard.wav"), str, msg="Return of transcribe_audio is not string")

    def test_audio_to_text_invalid_file(self):
        """Test to see if the right exception is raised when a non-existing file is send to the  transcribe_audio function"""
        self.assertRaises(FileNotFoundError, ms.transcribe_audio, file="Filethatdoesnotexist.wav")

    def test_audio_to_text_invalid_type(self):
        """Test to see if the right exception is raised when an invalid audio extension e.g. .ogg is send to the transcribe_audio function"""
        self.assertRaises(ValueError, ms.transcribe_audio, file="Lorem.ogg")

if __name__ == '__main__':
    unittest.main()