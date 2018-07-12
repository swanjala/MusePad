import os
from app import create_app, db, api
from app.models import User, MuseList, MuseItems
from app.views import LoginUser, RegisterUser, MuseListAction, MuseItemAction
from flask_script import Server, Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask import jsonify
import coverage

"""Class that manages the applications base operations, from running to database operations 
and definition of view navigation before application runtime"""

COV = coverage.coverage(
	branch=True,
	include='app/*',
	omit=[
	'app/models.py',
	'app/__init__py',
	'app/utils.py',
	]
)
COV.start()

"""
Add the application API enpoints
"""

api.add_resource(LoginUser,"/auth/login", endpoint="token")
api.add_resource(RegisterUser,"/auth/register", endpoint="register")
api.add_resource(MuseListAction, "/muselists","/muselists/<id>", endpoint="muselist")
api.add_resource(MuseItemAction, "/muselists/<id>/items", "/muselists/<id>/items/<Item_id>", endpoint="items")

# Instanciate the application
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Initializing hte member class

manager = Manager(app)

# Initializing the migrate class
migrate = Migrate(app, db)

@app.route('/')
def index():
	return 'Welcome to musepad API'

@app.errorhandler(500)
def server_error(e):
	return jsonify(error=500, message=str(e)), 500

@app.errorhandler(404)
def server_error(e):
	return jsonify(error=404, message=str(e)+"Access error"), 404

def make_shell_context():
	return dict(app=app, db=db, User=User, MuseList=MuseList, Item = Item)

#Adding the command to the manager

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TestTestRunner(verbosity=2).run(tests)

	COV.stop()
	COV.save()
	print('Covarage summary from the tests')
	COV.report()
	COV.html_report()
	COV.erase()
	return 0


@manager.command
def dropdb():

	if prompt_bool("This operation will delete your data irreversably, are you sure you want to preceed"):
		db.drop_all()
		print("All the data has been deleted")

if __name__ == "__main__":
	manager.run()

else:
	print("The application is not able to run"+__name__)