


from model_server import translate_server

text = translate_server.translate_text("Hi I am Quinten", url="http://DESKTOP-NBG1D5R:5000", model_id=2)
print(text.tgt)