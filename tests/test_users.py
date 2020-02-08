import json
import unittest
import api


class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_by_id(self):
        response = self.app.get("/users/123")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "user: 123")

    def test_reviews(self):
        response = self.app.get("/users/123/reviews")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "reviews from user: 123")

    def test_favorites(self):
        response = self.app.get("/users/123/favorites")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "favorites of user: 123")

    def tearDown(self):
        pass
