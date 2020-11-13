import re
import requests
import json
from sacremoses import MosesTokenizer, MosesDetokenizer
import speech_recognition as sr
import os
from available_models import get_valid_model_ids as get_valid_model_ids

mt_en = MosesTokenizer(lang='en')
mt_nl = MosesDetokenizer(lang='nl')


class TranslatedObject:
    """Return object of translate_text"""
    def __init__(self, src, tgt, score):
        self.src = src
        self.tgt = tgt
        self.score = score




class ModelIDNotFoundException(Exception):
    """Exception raised when model id is not found.

    Attributes:
        model_id -- the model id that was not found
        found_model_ids -- model ids that where found
        message -- the models that where found
    """

    def __init__(self, model_id, found_model_ids:list) -> None:
        self.model_id = model_id
        self.found_model_ids = found_model_ids
        self.message = f"Model id {self.model_id} was not found in the config file. The ids that where found are {found_model_ids}"
        super().__init__(self.message)


def translate_text(text: str, url: str, model_id) -> TranslatedObject:
    """Translates a text with the url of a translation server. The url is the url that comes up when you start the
    translation model"""
    assert type(text) == str, "Text has to be of type string"
    assert type(url) == str, "Url has to be of type string"

    model_ids = get_valid_model_ids()
    if model_id not in model_ids:
        raise ModelIDNotFoundException(model_id, model_ids)
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


def transcribe_audio(file, audio_engine="sphinx") -> str:
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
