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
        response = self.app.get("/users/1")
        data = json.loads(response.data.decode())
        expected = {
            "username": "johnsmith",
            "created_at": data["created_at"],
            "id": 1,
            "preference_id": 1,
            "profile_picture": "picture",
            "settings": None
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_reviews(self):
        response = self.app.get("/users/1/reviews")
        data = json.loads(response.data.decode())
        expected = [
            {
                "comment": "boo",
                "created_at": data[0]["created_at"],
                "id": 1,
                "ratings": [],
                "upvote_count": 10,
                "washroom_id": 1
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_favorites(self):
        response = self.app.get("/users/1/favorites")
        data = json.loads(response.data.decode())
        expected = [
            {
                "id": 1,
                "user_id": 1,
                "washroom_id": 1
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def tearDown(self):
        pass
