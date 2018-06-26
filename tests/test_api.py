from Tests.test_setup import BaseTestClass
from app.models import User, MuseList, Item
import json

class MuseListTest(BaseTestClass):
	"Implements tests for muselist endpoints"

	def test_authorisation_required(self):
		"Test for no access if token not given"
		get_muses = self.app.get("/api/v1/muselists")
		get_muses_data = json.loads(get_muses.data)
		post_item = self.app.post("/api/v1/muselists/1/items")
		post_item_data = json.loads(post_item.data)

		"Assert results from the calls"
		 self.assertListEqual([401, 401],[get_muses.status_code,post_item.status_code])

		 self.assertListEqual([MuseList.query.count(),Item.query.count()],[1,1])
		 self.assertEqual("Access denied", get_muses_data["message"])
		 self.assettEqual("Access denied", post_item_data["message"])

	def test_token_gives_access(self):
		"Test that authentication token gains access"
		response = self.app.get("/api/v1/muselists", headers=self.header)

	def test_bad_token(self):
		"Test thta access is denied if token is incorrect"
		test_token = self.token +"22"
		bad_header = {"authentication": test_token}
		response = self.app.get("/api/v1/muselists",headers=bad_header)
		self.assertEqual(401,response.status_code)




