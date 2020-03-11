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

    def test_get_root(self):
        response = self.app.get(
            "/washrooms",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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

        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)

        self.assertEqual(data[0], expected_data)

    def test_post_washroom(self):
        data = {
            "amenities": [
                "air_dryer",
                "auto_toilet"
            ],
            "building_id": 0,
            "floor": 1,
            "gender": "women",
            "urinal_count": 0,
            "stall_count": 4,
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "comment": "Engineering 1"
        }

        response = self.app.post(
            "/washrooms",
            json=data
        )
        self.assertEqual(
            response.status_code,
            HttpCodes.HTTP_201_CREATED
        )

        returned_data = json.loads(response.data.decode())

        data["average_ratings"] = {
            'cleanliness': 0,
            'privacy': 0,
            'smell': 0,
            'toilet_paper_quality': 0
        }
        data["building_title"] = "Engineering"
        data["is_favorite"] = False
        data["review_count"] = 0
        data["overall_rating"] = 0

        created_at = returned_data.pop("created_at", None)
        self.assertIsNotNone(created_at)

        the_id = returned_data.pop("id", None)
        self.assertIsNotNone(the_id)

        self.assertEqual(data, returned_data)

        # Test washroom count increases
        response = self.app.get("/buildings/{}".format(data["building_id"]))
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data = json.loads(response.data.decode())

        self.assertEqual(data["washroom_count"], 1)

    def test_post_washroom_unprocessable_entity_error(self):
        # Invalid building ID
        data = {
            "amenities": [
                "air_dryer",
                "auto_toilet"
            ],
            "building_id": 10,
            "floor": 1,
            "gender": "women",
            "urinal_count": 0,
            "stall_count": 4,
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "comment": "Engineering 1"
        }

        response = self.app.post(
            "/washrooms",
            json=data
        )

        self.assertEqual(
            response.status_code,
            HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_post_washroom_bad_request_error(self):
        # Missing floor
        data = {
            "amenities": [
                "air_dryer",
                "auto_toilet"
            ],
            "building_id": 0,
            "gender": "women",
            "urinal_count": 0,
            "stall_count": 4,
            "location": {
                "latitude": 12.2,
                "longitude": 17.9
            },
            "comment": "Engineering 1"
        }

        response = self.app.post(
            "/washrooms",
            json=data
        )

        self.assertEqual(
            response.status_code,
            HttpCodes.HTTP_400_BAD_REQUEST
        )

    def test_get_by_id(self):
        response = self.app.get("/washrooms/0")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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

        created_at = data.pop("created_at", None)
        self.assertIsNotNone(created_at)

        self.assertEqual(data, expected_data)

    def test_get_by_id_error(self):
        # Non existant washroom
        response = self.app.get("/washrooms/32")
        self.assertEqual(response.status_code, HttpCodes.HTTP_400_BAD_REQUEST)

    def test_get_with_query(self):
        response = self.app.get(
            "/washrooms?latitude=49.81050491333008&longitude" +
            "=-97.13350677490234&radius=2&max_results=1&" +
            "amenities=contraceptives,auto_dryer"
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        # Test it returns list of max_results size
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 1)

    def test_get_reviews(self):
        response = self.app.get("/washrooms/0/reviews")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

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

        for item in data:
            item.pop("created_at", None)
            if "user" in item:
                user = item["user"]
                created_at_user = user.pop("created_at", None)
                self.assertIsNotNone(created_at_user)

        self.assertEqual(data, expected_data)

    def test_get_reviews_empty(self):
        # Non existant washroom
        response = self.app.get("/washrooms/32/reviews")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data = json.loads(response.data.decode())
        self.assertEqual(data, [])

    def test_post_reviews(self):
        data = {
            "comment": "yay",
            "ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 3.7,
                "toilet_paper_quality": 1.5
            }
        }
        response = self.app.post("/washrooms/0/reviews", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_201_CREATED)
        returned_data = json.loads(response.data.decode())

        data["upvote_count"] = 0
        data["washroom_id"] = 0
        result = returned_data.pop("created_at", None)
        self.assertIsNotNone(result)

        result = returned_data.pop("user", None)
        self.assertIsNotNone(result)

        result = returned_data.pop("id", None)
        self.assertIsNotNone(result)

        self.assertEqual(data, returned_data)

        # Test review count increases
        response = self.app.get("/washrooms/{}".format(data["washroom_id"]))
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data = json.loads(response.data.decode())

        self.assertEqual(data["review_count"], 2)

    def test_post_empty_comment_reviews(self):
        data = {
            "ratings": {
                "cleanliness": 4.2,
                "privacy": 4.4,
                "smell": 4.5,
                "toilet_paper_quality": 4.5
            }
        }
        response = self.app.post("/washrooms/0/reviews", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_201_CREATED)
        returned_data = json.loads(response.data.decode())

        data["upvote_count"] = 0
        data["washroom_id"] = 0
        data["comment"] = ""
        result = returned_data.pop("created_at", None)
        self.assertIsNotNone(result)

        result = returned_data.pop("user", None)
        self.assertIsNotNone(result)

        result = returned_data.pop("id", None)
        self.assertIsNotNone(result)

        self.assertEqual(data, returned_data)

        # Test review count increases
        response = self.app.get("/washrooms/{}".format(data["washroom_id"]))
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        data = json.loads(response.data.decode())

        self.assertEqual(data["review_count"], 1)

    def test_post_reviews_error(self):
        data = {
            "comment": "testing",
            "ratings": {
                "cleanliness": 3.2,
                "privacy": 1.2,
                "smell": 3.7,
                "toilet_paper_quality": 1.5
            }
        }

        # Non existant washroom
        response = self.app.post("/washrooms/10/reviews", json=data)
        self.assertEqual(
            response.status_code,
            HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY
        )
