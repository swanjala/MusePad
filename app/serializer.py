from flask_restful import fields


UserFormat = {"id": fields.Integer,
			  "email_address":fields.String,
			  "gender": fields.String 
			  }