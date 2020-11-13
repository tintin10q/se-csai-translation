from web_frontend import app
import unittest
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
import io
import os

print(os.getcwd())


# ImmutableMultiDict([('audio_file', <FileStorage: 'harvard.wav' ('audio/wav')>)])
# ImmutableMultiDict([('audio_file', FileStorage(io.open("harvard.wav"), "harvard.wav"))])

class TestWebServer(unittest.TestCase):
    # <FileStorage: 'harvard.wav' ('audio/wav')>
    def setUp(self):
        app.testing = True
        app.debug = True
        self.app = app.test_client()

    def test_root_get(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200, "Get of / did not return 200")

    def test_root_post(self):
        print("This is an integration test testing everything together.")
        file = FileStorage(
            stream=open("harvard.wav", "rb", buffering=0),
            filename="harvard.wav",
            content_type="audio/wav",
        )
        data = {"audio_file": file}
        result = self.app.post('/', content_type='multipart/form-data', data=data)
        self.assertEqual(result.status_code, 200, "Post of / did not return 200")


if __name__ == '__main__':
    unittest.main()
