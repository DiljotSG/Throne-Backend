import api
import json
import unittest
from api.response_codes import HttpCodes


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
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        expected_data = {
            "amenities": [
                "air_dryer",
                "auto_toilet"
            ],
            "average_ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 3.7,
                "toilet_paper_quality": 1.5
            },
            "building_id": 0,
            "building_title": "Engineering",
            "floor": 1,
            "gender": "women",
            "urinal_count": 0,
            "stall_count": 4,
            "id": 0,
            "is_favorite": True,
            "review_count": 1,
            # This is 0 because we add to stubs directly using the stub classes
            # The logic for updating review count is in the store classes
            # New reviews will adjust this count, but it won't include
            # The original reviews added through the stub init file.
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "overall_rating": 2.4000000000000004,
            "comment": "Engineering 1"
        }

        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        self.assertTrue(isinstance(data, list))
        data[0].pop("created_at", None)
        self.assertEqual(data[0], expected_data)

    def test_get_by_id(self):
        response = self.app.get("/washrooms/0")
        data = json.loads(response.data.decode())
        expected_data = {
            "amenities": [
                "air_dryer",
                "auto_toilet"
            ],
            "average_ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 2.7,
                "toilet_paper_quality": 4.5
            },
            "building_id": 0,
            "building_title": "Engineering",
            "floor": 1,
            "gender": "women",
            "urinal_count": 0,
            "stall_count": 4,
            "id": 0,
            "is_favorite": True,
            "review_count": 0,
            # This is 0 because we add to stubs directly using the stub classes
            # The logic for updating review count is in the store classes
            # New reviews will adjust this count, but it won't include
            # The original reviews added through the stub init file.
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "overall_rating": 2.9000000000000004,
            "comment": "Engineering 1"
        }
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data.pop("created_at", None)
        self.assertEqual(data, expected_data)

    def test_get_reviews(self):
        response = self.app.get("/washrooms/0/reviews")
        data = json.loads(response.data.decode())
        expected_data = [
            {
                "comment": "yay",
                "id": 0,
                "ratings": {
                    "cleanliness": 3.2,
                    "privacy": 1.2,
                    "smell": 2.7,
                    "toilet_paper_quality": 4.5
                },
                "upvote_count": 5,
                "user": {
                    "id": 0,
                    "profile_picture": "picture",
                    "username": "janesmith"
                },
                "washroom_id": 0
            }
        ]
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        for item in data:
            item.pop("created_at", None)
            if "user" in item:
                user = item["user"]
                created_at_user = user.pop("created_at", None)
                self.assertNotEqual(created_at_user, None)

        self.assertEqual(data, expected_data)

    def test_post_reviews(self):
        data = {
            "comment": "testing",
            "ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 3.7,
                "toilet_paper_quality": 1.5
            }
        }
        response = self.app.post("/washrooms/0/reviews/", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_201_CREATED)

    def test_delete_reviews(self):
        pass
