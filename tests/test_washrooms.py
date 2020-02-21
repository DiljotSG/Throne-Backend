import api
import json
import unittest


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
        expected_data = {
            "amenities": [
                "Air Dryer",
                "Automatic Toilet"
            ],
            "average_ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 2.7,
                "toilet_paper_quality": 4.5
            },
            "building_id": 0,
            "floor": 1,
            "gender": "women",
            "id": 0,
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "overall_rating": 4,
            "title": "Engineering 1"
        }

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        data[0].pop("created_at", None)
        self.assertEqual(data[0], expected_data)

    def test_by_id(self):
        response = self.app.get("/washrooms/0")
        data = json.loads(response.data.decode())
        expected_data = {
            "amenities": [
                "Air Dryer",
                "Automatic Toilet"
            ],
            "average_ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 2.7,
                "toilet_paper_quality": 4.5
            },
            "building_id": 0,
            "floor": 1,
            "gender": "women",
            "id": 0,
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "overall_rating": 4,
            "title": "Engineering 1"
        }
        self.assertEqual(response.status_code, 200)
        data.pop("created_at", None)
        self.assertEqual(data, expected_data)

    def test_reviews(self):
        response = self.app.get("/washrooms/0/reviews")
        data = json.loads(response.data.decode())
        expected_data = [
            {
                "comment": "yay",
                "id": 0,
                "rating": {
                    "cleanliness": 3.2,
                    "privacy": 1.2,
                    "smell": 2.7,
                    "toilet_paper_quality": 4.5
                },
                "upvote_count": 5,
                "user_id": 0,
                "washroom_id": 0
            }
        ]
        self.assertEqual(response.status_code, 200)
        data[0].pop("created_at", None)
        self.assertEqual(data, expected_data)
