import api
import json
import unittest
from api.response_codes import HttpCodes


class TestBuildingsAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_get_root(self):
        response = self.app.get(
            "/buildings",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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
                    "latitude": 49.809364318847656,
                    "longitude": -97.1344985961914
                },
                "maps_service_id": 0,
                "overall_rating": 4,
                "title": "Engineering",
                "washroom_count": 0
                # This is 0 because we add to stubs directly using the stub
                # The logic for updating washroom count is in the store
                # New washrooms will adjust this count, but it won't include
                # The original washrooms added through the stub init file.
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
                    "latitude": 49.810203552246094,
                    "longitude": -97.13143920898438
                },
                "maps_service_id": 1,
                "overall_rating": 3,
                "title": "Science",
                "washroom_count": 0
            }
        ]

        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)
        created_at = data[1].pop("created_at", None)
        self.assertIsNotNone(created_at)

        self.assertEqual(data, expected_data)

    def test_get_by_id(self):
        response = self.app.get("/buildings/1")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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
                "latitude": 49.810203552246094,
                "longitude": -97.13143920898438
            },
            "maps_service_id": 1,
            "overall_rating": 3,
            "title": "Science",
            "washroom_count": 0
        }

        created_at = data.pop("created_at", None)
        self.assertIsNotNone(created_at)

        self.assertEqual(data, expected_data)

    def test_get_by_id_error(self):
        # Non existant building
        response = self.app.get("/buildings/32")
        self.assertEqual(response.status_code, HttpCodes.HTTP_400_BAD_REQUEST)

    def test_get_with_query(self):
        response = self.app.get(
            "/buildings?latitude=49.81050491333008&longitude" +
            "=-97.13350677490234&radius=2&max_results=1&" +
            "amenities=contraceptives,auto_dryer"
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        # Test it returns list of max_results size
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 1)

    def test_get_washrooms(self):
        response = self.app.get("/buildings/1/washrooms")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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
                    "building_title": "Science",
                    "building_id": 1,
                    "floor": 1,
                    "gender": "men",
                    "urinal_count": 3,
                    "stall_count": 4,
                    "id": 2,
                    'is_favorite': False,
                    "review_count": 0,
                    # This is 0 because we add to stubs directly using the stub
                    # The logic for updating review count is in the store
                    # New reviews will adjust this count, but it won't include
                    # The original reviews added through the stub init file.
                    "location": {
                        "latitude": 49.810203552246094,
                        "longitude": -97.13143920898438
                    },
                    "overall_rating": 3,
                    "comment": "Science 1"
                }
            ]
        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)

        self.assertEqual(data, expected_data)

    def test_get_washrooms_empty(self):
        # Non existant building
        response = self.app.get("/buildings/32/washrooms")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data = json.loads(response.data.decode())
        self.assertEqual(data, [])
