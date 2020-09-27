from flask import Flask
from flask_cors import CORS # disable cross-reference prevention, in order to make requests from browser
app = Flask(__name__)
CORS(app)
from app.api import blueprint
app.register_blueprint(blueprint, url_prefix='/api')