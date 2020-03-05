import api
import json
import unittest


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
            "/buildings",
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        expected_data = [
            {
                "best_ratings": {
                    "cleanliness": 3.2,
                    "privacy": 1.2,
                    "smell": 2.7,
                    "toilet_paper_quality": 4.5
                },
                "id": 0,
                "location": {
                    "latitude": 10.2,
                    "longitude": 15.9
                },
                "maps_service_id": 0,
                "overall_rating": 4,
                "title": "Engineering",
                "washroom_count": 0
            },
            {
                "best_ratings": {
                    "cleanliness": 2.2,
                    "privacy": 4.2,
                    "smell": 2.8,
                    "toilet_paper_quality": 4.2
                },
                "id": 1,
                "location": {
                    "latitude": 104,
                    "longitude": 230.5
                },
                "maps_service_id": 1,
                "overall_rating": 3,
                "title": "Science",
                "washroom_count": 0
            }
        ]

        self.assertEqual(response.status_code, 200)
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)
        created_at = data[1].pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)

    def test_by_id(self):
        response = self.app.get("/buildings/1")
        data = json.loads(response.data.decode())
        expected_data = {
            "best_ratings": {
                "cleanliness": 2.2,
                "privacy": 4.2,
                "smell": 2.8,
                "toilet_paper_quality": 4.2
            },
            "id": 1,
            "location": {
                "latitude": 104,
                "longitude": 230.5
            },
            "maps_service_id": 1,
            "overall_rating": 3,
            "title": "Science",
            "washroom_count": 0
        }
        self.assertEqual(response.status_code, 200)
        created_at = data.pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)

    def test_washrooms(self):
        response = self.app.get("/buildings/1/washrooms")
        data = json.loads(response.data.decode())
        expected_data = [
                {
                    "amenities": [
                        "contraception",
                        "lotion"
                    ],
                    "average_ratings": {
                        "cleanliness": 2.2,
                        "privacy": 4.2,
                        "smell": 2.8,
                        "toilet_paper_quality": 4.2
                    },
                    "building_id": 1,
                    "floor": 1,
                    "gender": "men",
                    "urinal_count": 3,
                    "stall_count": 4,
                    "id": 2,
                    'is_favorite': False,
                    "review_count": 1,
                    "location": {
                        "latitude": 114,
                        "longitude": 200.5
                    },
                    "overall_rating": 3,
                    "comment": "Science 1"
                }
            ]
        self.assertEqual(response.status_code, 200)
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)
