from flask_httpauth import HTTPTokenAuth
from flask import jsonify, g

from app.models import User

token_auth= HTTPTokenAuth("Bearer")

@token_auth.verify_token
def verify_token(token):
	user_active_id = User.confirm_token(token)
	if user_active_id:
		g.user = User.query.filter_by(id=user_active_id).first()
		return True

	return False

@token_auth.error_handler

def auth_error():
	return jsonify({"message":"Access not Allowed, Invalid token"}), 401
	