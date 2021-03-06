import re
from flask_restful import abort, inputs, Resource, reqparse, marshal_with
from flask import abort, jsonify, request
from app import db, expiry_time
from app.models import User, Profile
from app.user_auth import token_auth, g
from app.utils import save, delete, is_not_empty
from app.serializer import UserFormat

class LoginUser(Resource):

	def __init__ (self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email_address', type=str, required=True,help = "Enter email email_address")
		self.reqparse.add_argument('password', type=str, required=True, help= "Enter password")

		super(LoginUser, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()

		email_address, password = args["email_address"], args["password"]

		user = User.query.filter_by(email_address=email_address).first()
		if not user or not user.auth_password(password):
			return {"message", "could not log you in, Check your credentials"}

		token = user.confirmation_token(expiry_time)

		return {"token": token.decode("ascii"), "user_id": user.id,"gender":user.gender, "email":user.email_address}, 200
		
class CheckUserEmail(Resource):

	def __init__ (self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email_address', type=str, required=True, help = "Enter email")

		super(CheckUserEmail, self).__init__()

	def post(self):

		args = self.reqparse.parse_args()

		email_address = args["email_address"]

		user = User.query.filter_by(email_address=email_address).first()

		if not user:
			return {"email_availability": "false"}, 200
			
		return {"email_availability":"true"}, 200

class RegisterUser(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument("email_address", type= str, required=True, help="Enter an email")
		self.reqparse.add_argument("password", type= str, required=True, help= "Enter password")
		self.reqparse.add_argument("gender", type=str, required= True, help="Enter your gender")

		super(RegisterUser, self).__init__()


	def post(self):

		args = self.reqparse.parse_args()
		email_address, password, gender = (args["email_address"].lower(), args["password"], args["gender"])

		if not re.match("\S+[@]\S+[.]\S", email_address):
			return{"message": "only numbers, letters,'-','-','.'allowed in email_address entry"}, 400

		if len(password) < 6:
			return{"message": "password must be at least 6 characters"}, 400

		user_info = User.query.filter_by(email_address=email_address).first()
		if user_info is not None:
			return{"message": "The email_address you have entered is not available,try a different one"}, 403
		user = User(email_address=email_address, password=password, gender= gender)

		save(user)
		msg = "You have been successfully added as " + user.email_address

		token = user.confirmation_token(expiry_time)

		return {"token": token.decode("ascii"),"email":user.email_address, "gender": user.gender}, 201


class ProfileActions(Resource):

	def __init__(self):

		self.reqparse = reqparse.RequestParser()
		super(ProfileActions, self).__init__()

	@marshal_with(UserFormat)
	def get(self):
		search = request.args.get("q") or None

		profile_obj = User.query.all()


		# if email:
			
		# 	# .filter_by(email_address= email).first()

		# 	if not profile_obj:
		# 		abort(404, "Data cannot be retrieved at this time")

		# 	return profile_obj, 200

		# if search:
		# 	profile_search_results = User.query.filter(User.email_address.ilike("%"+search+"%"))

		# 	if not profile_search_results or profile_search_results is None:
		# 		abort(404, "Cannot retrieve user")
		
		profile_results= [profile_results for profile_results in profile_obj] 

		return {"profile": profile_results}, 200

		



