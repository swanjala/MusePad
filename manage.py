import os
from app import create_app, db, api
from app.models import User, Profile 
from app.view import LoginUser, RegisterUser, ProfileActions
from flask_script import Server, Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask import jsonify


api.add_resource(LoginUser, "/auth/login", endpoint="token")
api.add_resource(RegisterUser, "/auth/register", endpoint="register")
api.add_resource(ProfileActions,"/profile", "/profile", endpoint="profile")


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
	return 'Welcome to Myworkout API'

@app.errorhandler(500)
def server_error(e):
	return jsonify(error=500, message=str(e)), 500

@app.errorhandler(404)
def server_error(e):
	return jsonify(error=404, message=str(e)+ "Access error"), 404

def make_shell_context():
	return dict(app=app, db=db, User=User, Profile= Profile)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command 
def dropdb():
	
	if prompt_bool("CAUTION: Operation deletes data permanently"):
		db.drop_all()
		print("All data deleted")

if __name__ == "__main__":
	manager.run()

else:
	print("Could not start the appliction"+__name__)


