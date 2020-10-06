
import speech_recognition as sr
from flask import Flask, render_template, request

app = Flask(__name__)

r = sr.Recognizer()

@app.route('/', methods=['POST'])
def hello_world():
    file = request.files['audio']
    audiofile = sr.AudioFile(file)
    with audiofile as source:
        audio = r.record(source)
        text = r.recognize_google(audio_data=audio, language='english') # This will not work in production
    return text

@app.route('/', methods=['GET'])
def hello_world_post():
    return render_template('root.html')


if __name__ == '__name__':
    app.run()