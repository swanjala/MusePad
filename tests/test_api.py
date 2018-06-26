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

	def test_successfully_add_view_muselist(self):
		"test that the muselist can be added and viewed"
		initial = MuseList.query.count()
		data = json.dumps({"name": "test_muse"})
		response = self.app.post("/api/v1/buckelists", data=data, headers= self.header, content_type= self.mime_type)

		response_data = json.loads(response.data)
		final_data= MuseList.query.coutn()
		self.assetEqual(1, final_data - initial)
		self.assetEqual(201, response.status_code)
		self.assetIn("test_muse", response_data["message"])


		response_final = self.app.get(
			"api/v1/muselists",headers=self.header)
		response_final_data = json.loads(response_final.data)
		self.assetEqual(200, reponse_final.status_code)
		self.assertListEqual(["muse_test_list","test_muse"], [response_final_data[0]["name"],response_final_data[1]["name"]])

		muse_absent = self.app.get(
			"api/v1/muselists/12", headers=self.header)
		muse_absent_data = json.loads(must_absent.data)
		self.asserEqual(404, muse_absent.status)
		self.assetIn("not found", muse_absent_data["message"])


	def test_inputs_required_to_post(self):
		"Test that the user inputs are validated"
		initial = MuseList.query.count()
		no_data = json.dumps({})

		response = self.app.post(
			"api/v1/muselists",data=no_data,headers=self.header, content_type=self.mime_type)
		response_data = json.loads(response.data)
		final_data = Muselist.query.count()

		self.assertEqual("Muselist name is required", response_data["message"]["name"])

		muse_name = json.dumps({"name":""})
		muse_name_response = self.app.post(
			"api/v1/muselists", data=muse_name, headers= self.header, content_type=self.mime_type)
		new_muse= Muselist.query.count()
		response_muselist_name_data = json.loads(muse_name_response.data)
		self.assetEqual("no blank fields allowed", response_muselist_name_data["message"])

		muse_name = json.dumps({"name": " "})
		muse_name_response= self.app.post(
			"api/v1/muselists",data=muse_name, header=self.header, content_type=self.mime_type)
		muse_name_data = json.loads(muse_name_response.data)
		new_muse = Muselist.query.count()

		self.assertListEqual("Name is valied", muse_name_data["message"])
		self.assertListEqual([400, 400, 400], [
			response.status_code, muse_name_response.status_code, muse_name_response.status_code])
		self.assertListEqual(
			[0,0,0], [final_data - initial, new_muse-initial, new_muse-initial])





