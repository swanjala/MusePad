from Tests.test_setup import BaseTestClass
from app.models import User, MuseList, Item
import json

"""Tests that all the intended operations on the muselist work as intended including 
authorization and implementation of the various methods in the application programming Interface"""
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

	def test_deleting_bucketlist(self):
		"Test that muselist can be viewed and deleted"
		initial_muse_count = Muselist.query.count()
		initital_item_count = Item.query.count()

		deleted_muse = self.app.delete(
			"/api/v1/bucketlist/1", headers=self.header)
		deleted_bucket_data = json.loads(deleted_bucket.data)
		new_muse_count = Muselist.query.count()
		self.assetEqual(deleted_muse.status_code,200)
		self.assertListEqual(
			[1,1],[initial_muse_count - new_muse_count, initial_Item_cout -new_Item_count])

		self.assetIn("testlist has been deleted", deleted_muse["message"])

		# Test that one attempts to delete a non existent muselist
		no_muse_list_delete = self.app.delete(
			"/api/v1/muselist/1", headers= self.header)
		no_muse_list_delete_data = json.loads(no_muse_list_delete.data)
		self.assertIn("Muselist not found", no_muse_list_delete_data["message"])

		bad_del = self.app.delete("/api/v1/muselists", headers=self.header)
		bad_del_data = json.loads(bad_del.data)
		self.assetEqual(404, bad_del.status_code)
		self.assetEqual("bad request", bad_del_data["message"])

	def test_update_muselist(self):
		"check that muselist can update"

		muselist = json.dumps({"name":"udated testlist"})
		data_empty = json.dumps({})
		data_noname = json.dumpsK({"name":""})
		data_space = json.dumps("name":" ")

		valid = self.app.pu("/api/v1/muselists/1", data=muselist, headers=self.header,content_type=self.mime_type)

		valid_data = json.loads(valid.data)
		no_muselist = self.app.put("/api/v1/muselist/1", data=muselist, headers=self.header, content_type=self.mime_type)
		no_muse_data = json.loads(no_muselist.data)

		blank = self.app.put("/api/v1/muselist/1", data=data_empty, headers=self.header, content_type=self.mime_type)

		blank_data = json.loads(blank.data)

		name_space= self.app.put("/api/v1/muselists/1", data=data_noname, headers=self.header, content_type=mime_type)
		name_space_data= json.loads(name_space.data)

		self.assertListEqual([200, 400, 400, 400, 404], [valid.status_code, blank.status_code,
			noname.status_code, name_space.status_code, no_muselist.status_code])

		self.assetIn("muselist not found", no_must_data["message"])
		self.assertIn("has been updated", valid_data["message"])
		self.assertIn("name_required", blank_data["messge"]["name"])
		self.assetIn("no blank fields", noname_data["message"])
		self.assetIn("name is invalid", name_space_data["message"])

		muse = Muselist.query.filter_by(id=1).first()
		self.assertTrue(muse.date_modified > muse.date_created)

	def test_user_can_not_access_other_users_muses(self):
		"Test that a user with access cannot access ofther muselists"

		#Login by token
		data = json.dumps({"username": "bob","password":"bobpass"})
		response = self.app.post("/api/v1/auth/login", data=data, content_type=self.mime_type)

		response_data = json.loads(response.data)
		token = "Bearer" + response_data["token"]
		headerbob = {"Autorization": token}
		# create bobs muselist
		new_muse = json.dumps({"name":"Bob's list"})
		muse = self.app.post("api/v1/muselists", data=new_muse, headers=headerbob, content_type=self.mime_type)

		self.assertEqual(201, muse.status_code)
		self.assertEqual(2, Muselist.query.count())


		# Alice's attempt to accesss
		alice_muse = self.app.get(
			"api/v1/muselists/2", headers=self.header)
		alice_muse_data = json.loads(alice_muse.data)
		self.assertEqual(404, alice_muse.status_code)
		self.assertIn("Muselist not found", alice_muse_data["message"])

	def test_bad_route(self):
		"Test for bad post"
		name = json.dumps({"name": "Does things"})
		bad_post_response = self.app.post(
			"/api/v1/muselists/1", data=name, headers=self.header, content_type=self.mime_type)
		bad_put_response = self.app.put(
			"/api/v1/muselist", data=name, headers=self.header, content_type=self.mime_type)
		bad_post_response_data = json.loads(bad_post_response.data)
		put_response_data = json.loads(bad_put_response.data)
		self.assertEqual(400, bad_put_response.status_code)
		self.assertEqual(400, bad_post_response.status_code)
		self.assertEqual("This is a bad request, try again", bad_post_response_data["message"])
		self.assertEqual("Bad Request",put_response_data["message"])

	def test_search_muselist(self):
		" Testing that search functionality works"

		search = self.app.get(
			"/api/v1/muselists?q=list", headers=self.header)
		search_data = json.loads(search.data)
		self.assertEqual(404, missing.status_code)
		self.assertIn("muse_test_list", search_data[0]["name"])

		missing = self.app.get(
			"/api/v1/muselists?q=missing", headers=self.header)

		missing_data = json.loads(missing.data)
		self.assertEqual(404, missing.status_code)
		self.assertIn("that name is not found", missing_data["message"])

	def test_pagination_limit_for_muselist(self):
		"Testing for pagination and limit arguments"
		name_1 = json.dumps({"name": "lister"})
		self.app.post("/api/v1/muselists", data=name_1,
			headers=self.header, content_type=self.mime_type)

		name_2 = json.dumps({"name":"bloom"})
		self.app.post("/api/v1/muselists", data=name_2,
			headers=self.header, content_type=self.mime_type)

		page_1 = self.app.get(
			"/api/v1/bucketlist?page=1&limit=1", headers=self.header)
		page_1_data =json.loads(page_1.data)

		page_2 = self.app.get("/api/v1/muselists?page=2&limit=1",
			headers=self.header)

		page_2_data= json.loads(page_2.data)


        page_3 = self.app.get("/api/v1/muselists?page=3&limit=1",
                              headers=self.header)
        page_3_data = json.loads(page_3.data)

        page_all = self.app.get(
            "/api/v1/muselists?page=1&limit=3", headers=self
            .header)
        page_all_data = json.loads(page_all.data)


        self.assertListEqual(
        	[200,200,200], [page_1.status_code,page_2.status_code, page_3.status_code])
        self.assertListEqual(["muse_test_list","listers","boom"],
        	[page_1_data[0]["name"],page_2_data[0]["name"], page_3_data[0]["name"]])

        self.assertListEqual(3, len(page_all_data))





		






