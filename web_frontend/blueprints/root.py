from flask import Blueprint, render_template, request, redirect, flash
import speech_recognition as sr
from model_server import translate_server
import json

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
    Translated = translate_server.translate_text(text, url=json.load(open("available_models/conf.json"))[
        "translate_url"])
    return render_template("root.html", text=Translated.src, text_t=Translated.tgt, score=Translated.score)
