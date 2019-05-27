import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'check_point_rules'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SSL_DISABLE = True

	@staticmethod
	def init_app(app):
		pass

class Development(Config):

	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir,'data-dev.db')

class ProductionConfig(Config):
	
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class HerokuConfig(ProductionConfig):

    # config heroku dep
	@classmethod
	def init_app(cls , app):
		ProductionConfig.init_app(app)
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)
		SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

	@classmethod
	def init_app(cls, app):
		# proxy servers 
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)

configset = {
	"Development": Development,
	"Production": ProductionConfig,
	"default": Development
}

expiry_time = 40000