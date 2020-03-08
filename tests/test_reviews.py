import api
import json
import unittest
from api.response_codes import HttpCodes


class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_get_by_id(self):
        response = self.app.get("/reviews/1")
        data = json.loads(response.data.decode())
        expected_data = {
            "comment": "boo",
            "id": 1,
            "ratings": {
                "cleanliness": 2.2,
                "privacy": 4.2,
                "smell": 2.8,
                "toilet_paper_quality": 4.2
            },
            "upvote_count": 10,
            "user": {
                "id": 1,
                "profile_picture": "picture",
                "username": "johnsmith"
            },
            "washroom_id": 2
        }
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        created_at = data.pop("created_at", None)
        self.assertNotEqual(created_at, None)

        if "user" in data:
            user = data["user"]
            created_at_user = user.pop("created_at", None)
            self.assertNotEqual(created_at_user, None)

        self.assertEqual(data, expected_data)

    def test_put_reviews(self):
        data = {
            "comment": "yay",
            "ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 2.7,
                "toilet_paper_quality": 4.5
            },
        }
        response = self.app.put("/reviews/0", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        returned_data = json.loads(response.data.decode())

        data["upvote_count"] = 5
        data["washroom_id"] = 0
        returned_data.pop("created_at", None)
        returned_data.pop("user", None)
        returned_data.pop("id", None)
        self.assertEqual(data, returned_data)

        response = self.app.put("/reviews/1", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_403_FORBIDDEN)

    def test_delete_reviews(self):
        response = self.app.delete("/reviews/0")
        self.assertEqual(
            response.status_code,
            HttpCodes.HTTP_501_NOT_IMPLEMENTED
        )
