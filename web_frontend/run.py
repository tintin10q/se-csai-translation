from web_frontend import app
from model_server import start_model_server
from threading import Thread

model_server_thread = Thread(target=start_model_server)
model_server_thread.start()
app.run()

