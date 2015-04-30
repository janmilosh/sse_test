from flask import Flask, render_template
from flask.ext.cors import CORS

from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    CORS(app, allow_headers='Content-Type')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
