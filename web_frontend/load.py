from flask import Flask
import web_frontend.blueprints as blueprints


app = Flask(__name__)

app.register_blueprint(blueprints.root)

if __name__ == "__main__":
    app.run(debug=True)
