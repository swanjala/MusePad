from flask_restful import fields

#Conversion of modal attributes to fields

Itemformat = {"id": fields.Integer,
			  "name": fields.String,
			  "date_created": fields.DateTime(dt_format = "rfc822"),
			  "date_modified": fields.DateTime(dt_format="rfc822"),
			  "done": fields.Boolean(attribute="status"),
			  "muse_id": fields.Integer,
			  "item_description": fields.String
			  }

MuselistFormat = {"id": fields.Integer,
				  "name": fields.String,
				  "items": fields.List(fields.Nested(Itemformat)),
				  "date_created": fields.DateTime(),
				  "creator": fields.String(attribute="user.username")
				  }