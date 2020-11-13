import unittest

import model_server as ms



class TestSoundToText(unittest.TestCase):

    def test_audio_to_text(self):
        self.assertIsInstance(ms.transcribe_audio("harvard.wav"), str, msg="Return of transcribe_audio is not string")

    def test_audio_to_text_invalid_file(self):
        self.assertRaises(FileNotFoundError, ms.transcribe_audio, file="harvardd.wav")

    def test_audio_to_text_invalid_type(self):
        self.assertRaises(ValueError, ms.transcribe_audio, file="Lorem.ogg")

if __name__ == '__main__':
    unittest.main()