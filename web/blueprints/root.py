from flask import Blueprint, render_template, request, redirect, flash
import speech_recognition as sr

root_blueprint = Blueprint('root', __name__)


@root_blueprint.route("/", methods=["GET"])
def root_get():
    return render_template("root.html")

r = sr.Recognizer()

@root_blueprint.route("/", methods=["POST"])
def root_post():
    file = request.files['audio_file']
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    text = r.recognize_google(audio)
    # translate text with model
    return text
