import json
import unittest
import api


class TestWashroomAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get(
            "/washrooms",
            follow_redirects=True)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_by_id(self):
        response = self.app.get("/washrooms/1")
        data = json.loads(response.data.decode())
        expected = {
            "amenities_id": 1,
            "average_rating_id": 1,
            "building_id": 1,
            "created_at": data["created_at"],
            "floor": 1,
            "gender": "male",
            "id": 1,
            "location": {"latitude": 114, "longitude": 200.5},
            "overall_rating": 3,
            "title": "Science1"
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_reviews(self):
        response = self.app.get("/washrooms/0/reviews")
        data = json.loads(response.data.decode())
        expected = [
            {
                "comment": "yay",
                "created_at": data[0]["created_at"],
                "id": 0,
                "ratings": [],
                "upvote_count": 5,
                "washroom_id": 0
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def tearDown(self):
        pass
