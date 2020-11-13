import unittest

from model_server import translate_server

class TestSoundToText(unittest.TestCase):

    def test_transcription(self):
        s = "Hi I am a test string"
        self.assertEqual(translate_server.translate_text(), 'FOO')


    def test_voice_to_text(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()