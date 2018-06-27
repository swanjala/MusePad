from app import db
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

class User(db.Model):
	__tablename__: 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255),unique=True, nullable=False)
	email = db.Column(db.Column(db.String[255], nullable=False))
	muserlist = db.relationsihp('Muselist'. backref='user', lazy='dynanic',
								cascade='all,delete-orphan')

	@property
	def password(self):
		raise AttributeError('password is hashed and cannot be read')

	@password.setter
	def password(self, password):
		self.password_hformat = generate_password_hash(password)

	def auth_password(self, password):
		return check_password_hash(self.password_hformat, password)

	def confirmation_token(self, expiration=4000):
		serial = Serializer(current_app.config['SECRET_KEY'], expiration)
		return serial.dumps({'id': self.id})

	@staticmethod
	def confirm_token(token):
		serial = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = serial.loads(token)
		except:
			return False
		return data["id"]

class Muselist(db.Model):
	__tablename__='muselists'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255),nullable=False)
	date_created = db.Column(db.DataTime, nullable=False, default=datetime.utcnow)
	date_modified = db.Column(db.datetime, default=datetime.utcnow, onupdate=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	items = db.relationsihp('Item', backref='muselist', lazy='dynamic', cascade='all, delete-orphan')
	muse_description = db.Column(db.String(255),nullable=True)

class Item(db.Model):
	__tablename__= 'items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.datetime, nullable=False, default=datetime.utcnow)
	status = db.Column(db.Boolean, default=False)

	muse_id = db.Column(db.Integer, db.ForeignKey('muserlist.id'),nullable=False)
	item_description = db.Column(db.String(255),nullable=True)


	