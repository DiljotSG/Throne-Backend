import api
import json
import unittest


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
        expected_data = {
            "id": 1,
            "preferences": {
                "gender": "men",
                "main_floor_access": True,
                "wheelchair_accessible": False
            },
            "profile_picture": "picture",
            "username": "johnsmith"
        }
        self.assertEqual(response.status_code, 200)
        created_at = data.pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)

    def test_reviews(self):
        response = self.app.get("/users/1/reviews")
        data = json.loads(response.data.decode())
        expected = [
            {
                "comment": "boo",
                "id": 1,
                "ratings": {
                    "cleanliness": 2.2,
                    "privacy": 4.2,
                    "smell": 2.8,
                    "toilet_paper_quality": 4.2
                },
                "upvote_count": 10,
                "user_id": 1,
                "washroom_id": 2
            }
        ]
        self.assertEqual(response.status_code, 200)
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)
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
