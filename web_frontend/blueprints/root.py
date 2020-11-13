from flask import Blueprint, render_template, request, redirect, flash
import speech_recognition as sr
from model_server import translate_server
import json

root_blueprint = Blueprint('root', __name__)


@root_blueprint.route("/", methods=["GET"])
def root_get():
    return render_template("root.html")





@root_blueprint.route("/", methods=["POST"])
def root_post():
    file = request.files['audio_file']
    text = translate_server.translate_audio(file, "sphinx")
    translated = translate_server.translate_text(text, url=json.load(open("available_models/conf.json"))[
        "translate_url"], model_id=100)
    return render_template("root.html", text=translated.src, text_t=translated.tgt, score=translated.score)
