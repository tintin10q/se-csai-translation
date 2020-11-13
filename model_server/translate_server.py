import re
import requests
import json
from sacremoses import MosesTokenizer, MosesDetokenizer
import speech_recognition as sr

mt_en = MosesTokenizer(lang='en')
mt_nl = MosesDetokenizer(lang='nl')


class TranslatedObject:
    def __init__(self, src, tgt, score):
        self.src = src
        self.tgt = tgt
        self.score = score


def translate_text(text: str, url: str, model_id=100) -> TranslatedObject:
    """Translates a text with the url of a translation server. The url is the url that comes up when you start the
    translation model"""
    assert type(text) == str, "Text has to be of type string"
    assert type(url) == str, "Url has to be of type string"
    # text = re.sub(r"([?.!,:;¿])", r" \1 ", text)
    # text = re.sub(r'[" "]+', " ", text)
    text = mt_en.tokenize(text, return_str=True)
    url = f"{url}/translator/translate"
    headers = {"Content-Type": "application/json"}
    data = [{"src": text, "id": model_id}]
    response = requests.post(url, json=data, headers=headers)
    translation = response.text
    jsn = json.loads(translation)

    tokens = jsn[0][0]['tgt']
    input_text = jsn[0][0]['src']
    score = jsn[0][0]['pred_score']
    # text = re.sub(r" ([?.!,:،؛؟¿])", r"\1", text)
    # text = mt_nl.detokenize(tokens)
    text = tokens
    return TranslatedObject(input_text, text, score)


r = sr.Recognizer()


def translate_audio(file, audio_engine="sphinx"):
    """Turn audio into text, auido_engine can be sphinx or google"""
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    if audio_engine == "sphinx":
        text = r.recognize_sphinx(audio)
    elif audio_engine == "google":
        text = r.recognize_google(audio)
    else:
        text = r.recognize_sphinx(audio)
    return text
