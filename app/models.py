from app import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

"""
Class that defines the application's database models and utilized by the ORM
to create a database and its various relationships
"""
class User(db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255),unique=True, nullable=False)
	email = db.Column(db.String(255), nullable=False)
	password_hformat = db.Column(db.String(255), nullable=False)
	muselist = db.relationship('MuseList', backref='user', lazy='dynamic',
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

class MuseList(db.Model):
	__tablename__='muselists'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	items = db.relationship('MuseItems', backref='muselists', lazy='dynamic', cascade='all, delete-orphan')

class MuseItems(db.Model):
	__tablename__= 'items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	status = db.Column(db.Boolean, default=False)
	muse_id = db.Column(db.Integer, db.ForeignKey('muselists.id'),nullable=False)
	item_description = db.Column(db.String(255),nullable=True)


	