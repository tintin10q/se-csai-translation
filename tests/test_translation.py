import unittest
import threading
import model_server as ms
import available_models
import time
import requests

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path[:-5])


class TestTranslation(unittest.TestCase):
    model_server_thread = threading.Thread(target=ms.start_model_server)
    print("Starting model server")
    model_server_thread.start()
    # Wait 3 seconds to start model server
    time.sleep(3)

    def setUp(self):
        self.model_server_url = available_models.get_conf()["translate_url"]
        self.model_ids = available_models.get_valid_model_ids()
        self.translation_text = "Hi I am a test string. How are you today?"

    def test_translation_output_type(self):
        print("This is an integration test. Testing getting valid model ids and trying to translate with each id found.")
        for model_id in self.model_ids:
            translation = ms.translate_text(self.translation_text, self.model_server_url, model_id)
            self.assertIsInstance(translation, ms.TranslatedObject, "Function does not return translation object")

    def test_translation_output_types(self):
        for model_id in self.model_ids:
            translation = ms.translate_text(self.translation_text, self.model_server_url, model_id)
            self.assertIsInstance(translation.tgt, str, "Translation object does not have tgt that is a string")
            self.assertIsInstance(translation.src, str, "Translation object does not have src that is a string")
            self.assertIsInstance(translation.score, float, "Translation object does not have score that is an int")

    def test_non_existing_id(self):
        non_existing_id = 1
        while non_existing_id in self.model_ids:
            non_existing_id += 1
        self.assertRaises(ms.ModelIDNotFoundException, ms.translate_text, text=self.translation_text, url=self.model_server_url, model_id=non_existing_id)

    def test_non_valid_url(self):
        for model_id in self.model_ids:
            self.assertRaises(requests.exceptions.ConnectionError, ms.translate_text, text=self.translation_text, url="https://0.0.0.0", model_id=model_id)

    def test_translation_string_length(self):
        for model_id in self.model_ids:
            self.assertGreater(len(ms.translate_text(self.translation_text, self.model_server_url, model_id).tgt), 0, "Return of translation has 0 characters")
            self.assertGreater(len(ms.translate_text(self.translation_text, self.model_server_url, model_id).tgt), 1, "Return of translation has only 1 character")

    def test_translation_from_audio_file(self):
        print("This is a integration test testing if the audio to text and translation work together")

        for model_id in self.model_ids:
            text = ms.transcribe_audio("harvard.wav")
            translate_object = ms.translate_text(text, self.model_server_url, model_id)
            self.assertIsInstance(translate_object, ms.TranslatedObject, "Return of translation has 0 characters")


if __name__ == '__main__':
    unittest.main()
    TestTranslation.model_server_thread.join()
