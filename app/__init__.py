from flask import Flask

app = Flask(__name__)
from app.api import blueprint
app.register_blueprint(blueprint, url_prefix='/api')

from app import routes