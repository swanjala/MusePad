from app import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class User(db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	email_address = db.Column(db.String(255), unique=True, nullable=False)
	password_hformat = db.Column(db.String(255), nullable= False)
	gender = db.Column(db.String(255), nullable=False)
	profile = db.relationship('Profile', backref='user', lazy='dynamic', 
								cascade='all,delete-orphan')

	@property
	def password(self):
		raise AttributeError('password is hashed and cannot be read')

	@password.setter
	def password(self, password):
		self.password_hformat = generate_password_hash(password)

	def auth_password(self, password):
		return check_password_hash(self.password_hformat, password)

	def confirmation_token(self,  expiration=4000):
		serial = Serializer(current_app.config['SECRET_KEY'], expiration)
		return serial.dumps({'id': self.id})

	@staticmethod
	def confirm_token(token):
		serial = Serializer(current_app.config['SECRET_KEY'])
		try:
			data= serial.loads(token)
		except:
			return False
		return data["id"]

class Profile(db.Model):
	__tablename__= 'profile'
	id =db.Column(db.Integer, primary_key=True)
	emailAddress = db.Column(db.String(255), nullable=False)
	gender = db.Column(db.String(255), nullable=False)
	user_id= db.Column(db.Integer,db.ForeignKey('users.id'), nullable= False)

	

