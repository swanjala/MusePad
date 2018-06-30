from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS 

from config import configset, expiry_time

api_blue_print = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blue_print)
db = SQLAlchemy()

def create_app(config_set):
	app = Flask(__name__)
	app.config.from_object(configset[config_set])
	configset[config_set].init_app(app)

	db.init_app(app)
	app.register_blueprint(api_blue_print)

	CORS(app)

	return app
