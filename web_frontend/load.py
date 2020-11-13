from flask import Flask
import web_frontend.blueprints as blueprints
from model_server.start_model_server import start_model_server
import threading

model_server_thread = threading.Thread(target=start_model_server)

app = Flask(__name__)
app.register_blueprint(blueprints.root)

if __name__ == "__main__":
    model_server_thread.start()
    app.run(debug=True)
