import json
import unittest
import api


class TestBuildingsAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get(
            "/buildings?location=12",
            follow_redirects=True)
        data = json.loads(response.data.decode())
        expected = [
            {
                "best_ratings": [],
                "created_at":data[0]["created_at"],
                "id": 0,
                "location":{"latitude": 10.2, "longitude": 15.9},
                "maps_service_id": 0,
                "overall_rating": 4,
                "title": "Engineering"
            },
            {
                "best_ratings": [],
                "created_at":data[1]["created_at"],
                "id": 1,
                "location":{"latitude": 104, "longitude": 230.5},
                "maps_service_id": 1,
                "overall_rating": 3,
                "title": "Science"
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_by_id(self):
        response = self.app.get("/buildings/1")
        data = json.loads(response.data.decode())
        expected = {
            "best_ratings": [],
            "created_at": data["created_at"],
            "id": 1,
            "location": {"latitude": 104, "longitude": 230.5},
            "maps_service_id": 1,
            "overall_rating": 3,
            "title": "Science"
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def test_washrooms(self):
        response = self.app.get("/buildings/1/washrooms")
        data = json.loads(response.data.decode())
        expected = [
            {
                "amenities_id": 1,
                "average_rating_id": 1,
                "building_id": 1,
                "created_at": data[0]["created_at"],
                "floor": 1,
                "gender": "men",
                "id": 2,
                "location": {"latitude": 114, "longitude": 200.5},
                "overall_rating": 3,
                "title": "Science 1"
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def tearDown(self):
        pass
