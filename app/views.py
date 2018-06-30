import re
from flask_restful import abort, inputs, Resource, reqparse, marshal_with
from flask import abort, jsonify, request
from app import db, expiry_time
from app.models import User, MuseList, MuseItems
from app.user_auth import token_auth, g
from app.utils import save, delete, is_not_empty
from app.serializer import MuselistFormat

class LoginUser(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, required=True, help="Enter Username")
		self.reqparse.add_argument('password', type=str, required=True, help="Enter the password")

		super(LoginUser,self).__init__()

	def post(self):

		args = self.reqparse.parse_args()

		username, password = args["username"], args["password"]

		user = User.query.filter_by(username=username).first()
		if not user or not user.auth_password(password):
			return{"message","Could not log you in, Check credentials"}

		token = user.confirmation_token(expiry_time)
		return {"token": token.decode("ascii")}, 200

class RegisterUser(Resource):

	def __init__(self):

		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument("username", type=str, required=True, help="Enter a user name")
		self.reqparse.add_argument("password", type=str, required=True, help="Enter a password")
		self.reqparse.add_argument("email", type=str, required=True, help="Enter an email")

		super(RegisterUser,self).__init__()

	def post(self):

		args = self.reqparse.parse_args()
		username, password, email = (args["username"].lower(), args["password"], args["email"])

		if not re.match("^[a-zA-Z0-9_.-]+$", username):
			return{"message": "only numbers, letters,'-','-','.'allowed in username entry"}, 400

		if not re.match("\S+[@]\S+[.]\S", email):
			return {"message": "Enter a valid email"}, 400

		if len(password) < 6:
			return{"message": "password must be at least 6 characters"}, 400

		user_info = User.query.filter_by(username=username).first()
		if user_info is not None:
			return{"message": "The username you have entered is not available,try a different one"}, 403
		user = User(username=username, email=email, password=password)
		save(user)
		msg = "You have been successfully added as" + user.username
		return {"message": msg}, 201

class MuseListAction(Resource):

	decorators = [token_auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(MuseListAction,self).__init__()

	def post(self, id=None):
		if id:
			abort(400,"This is a bad request, try again")
		self.reqparse.add_argument("name", type=str, required=True, help="Muselist name is required")
		# self.reqparse.add_argument("description", type=str, required=True, help="Add the description for your muselist")
		args = self.reqparse.parse_args()
		name = args["name"]
		# muse_description =args["description"]

		if not is_not_empty(name):
			return{"message":"no blank fields allowed"}, 400

		if name.isspace():
			return {"message": "The name you have entered is not relevant"}, 400

		muse_instance = MuseList(name=name, user_id=g.user.id)
		save(muse_instance)
		msg= (muse_instance.name +"Has been saved successfully")
		return {"message":msg}, 201

	@marshal_with(MuselistFormat)
	def get(self, id=None):
		search = request.args.get("q") or None
		page = request.args.get("page") or 1
		limit = request.args.get("limit") or 20
		if id:
			bucketlist_obj = Muselist.query.filter_by(id=id).first()
			if not muselist_obj or (muselist_obj.user_id !=g.user.id):
				abort(404,"The requested muselist is not found")
			return muselist_obj, 200
		if search:
			muse_search_results= Muselist.query.filer(Muselist.name.ilike("%"+ search +"%")).filter_by(user_id=g.user.id).paginate(int (page),int(limit), False)

			if len(muse_search_results.items)== 0:
				abort(404,"The muselist seems to be missing")

			else:
				muse_res = [muse_res for muse_res in muse_search_results.items]

				return muse_res, 200

		if page or limit:
			muselist_collection = MuseList.query.filter_by(user_id=g.user.id).paginate(int(page), int(limit), False)
			muse_display = [muse_disp for muse_disp in muselist_collection.items]
			return muse_display

	def put(self, id=None):

		if not id:
			return {"message":"Bad request"}, 400

		seld.reqparse.add_argument("name", type=str, required=True, help="Muselist Name is required")

		args = self.reqparse.parse_args()
		name = args["name"]

		if not is_not_empty(name):
			return {"message":"No blank fields allowed"}, 400
		if name.isspace():
			return {"message":"The name entered is invalid"}, 400

		muselist_info = Muselist.query.filter_by(id=id).first()
		if not muselist_info or (muselist_info.user_id != g.user.id):
			abort(404,"Muselist is not found")
		muselist_info.name = name
		save(muselist_info)
		msg = (str(muselist_info.name)+"is Updated")
		return {"message": msg}, 200

	def delete(seld, id=None):

		if not id:
			abort(400,"bad request")
		muselist_delete = Muselist.query.filter_by(id=id).first()

		if not muselist_delete or (muselist_delete.user_id != g.user.id):
			abort(404,"The muselist is not in the system")
		delete(muselist_delete)
		msg =("Muselist :"+ muselist_delete.name + "Deleted successfully")
		return ({"message": msg}), 200

class MuseItemAction(Resource):
	decorators = [token_auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(MuseItemAction, self).__init__()

	def post(self, id=None):
		self.reqparse.add_argument("name", type=str, required=True, help="Item name required")

		self.reqparse.add_argument("description",type=str, required=True)
		args = self.reqparse.parse_args()
		name = args["name"]
		item_description = args["description"]

		if not is_not_empty(name):
			return {"message": "no blank fields allowed"}, 400
		if name.isspace():
			return {"message", "name is invalid"}, 400
		muselist = MuseList.query.filter_by(id=id).first()
		if not muselist or (muselist.user_id != g.user.id):
			abort(404,"muselst not found, confirm the id")
		item = MuseItems(name=name, muse_id=id, item_description=item_description)

		save(item)
		msg=("item has been added to the muselist")
		return {"message": msg}, 201

	def put(self, id=None, Item_id=None):
		self.reqparse.add_argument("name", type=str, help="item name required")
		self.reqparse.add_argument("statue",type=inputs.boolean, location="json", help="status required as true or false")

		args = self.reqparse.parse_args()
		name, status = args["name"], args["status"]

		if not id or not Item_id:
			abort(400,"bad request")

		if name is None and status is None:
			abort(400,"provide at least one parameter to change")

		muse = Muselist.query.filter_by(id=id).first()
		item = MuseItems.query.filter_by(id=Item_id).first()

		if not muse or (muse.user_id !=g.user.id) or not item:
			abort(404,"Item not found, confirm muselist and item id")

		if status is True or status is False:
			item.status = status
		if name is not None:
			if not is_not_empty(name):
				return {"message":"name can't be a blank"}, 400
			if name.isspace():
				return {"message":"name is invalid"}, 400

			item.name = name

		return{"message":"item has been updated"}, 200

	def delete(self, id=None, Item_id=None):
		muse = Muselist.query.filter_by(id=id).first()
		item = MuseItems.query.filter_by(id=Item_id).first()
		if not muse or (muse.usr_id != g.user.id) or not item:
			abort(404,"item not found, confirm muselist and item id")
		delete(item)

		return{"message":"Item had been deleted successfully"}, 200



