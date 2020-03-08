import api
import json
import unittest
from api.response_codes import HttpCodes


class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get(
            "/users",
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        expected_data = {
            "id": 0,
            "profile_picture": "picture",
            "username": "janesmith"
        }
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        created_at = data.pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)

    def test_get_user_by_id(self):
        response = self.app.get("/users/1")
        data = json.loads(response.data.decode())
        expected_data = {
            "id": 1,
            "profile_picture": "picture",
            "username": "johnsmith"
        }
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        created_at = data.pop("created_at", None)
        self.assertNotEqual(created_at, None)
        self.assertEqual(data, expected_data)

    def test_get_users_reviews(self):
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
                "user": {
                    "id": 1,
                    "profile_picture": "picture",
                    "username": "johnsmith"
                },
                "washroom_id": 2
            }
        ]

        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)

        if "user" in data[0]:
            user = data[0]["user"]
            created_at_user = user.pop("created_at", None)
            self.assertNotEqual(created_at_user, None)

        self.assertEqual(data, expected)

    def test_get_reviews(self):
        response = self.app.get("/users/reviews")
        data = json.loads(response.data.decode())
        expected = [
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
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)

        if "user" in data[0]:
            user = data[0]["user"]
            created_at_user = user.pop("created_at", None)
            self.assertNotEqual(created_at_user, None)

        self.assertEqual(data, expected)

    def test_get_favorites(self):
        response = self.app.get("/users/favorites")
        data = json.loads(response.data.decode())
        expected = [
            {
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
                "comment": "Engineering 1",
                "floor": 1,
                "gender": "women",
                "id": 0,
                "is_favorite": True,
                "location": {
                    "latitude": 12.2,
                    "longitude": 17.9
                },
                "overall_rating": 2.9000000000000004,
                "review_count": 0,
                "stall_count": 4,
                "urinal_count": 0
            }
        ]

        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        created_at = data[0].pop("created_at", None)
        self.assertNotEqual(created_at, None)

        self.assertEqual(data, expected)

    def test_post_user_favorites(self):
        data = {
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
            "comment": "Engineering 2",
            "floor": 1,
            "gender": "men",
            "id": 1,
            "is_favorite": True,
            "location": {
                "latitude": 114,
                "longitude": 200.5
            },
            "overall_rating": 3,
            "review_count": 0,
            "stall_count": 4,
            "urinal_count": 3
        }
        response = self.app.post("/users/favorites/", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_201_CREATED)

        returned_data = json.loads(response.data.decode())

        expected_data = [
            {
                'amenities': [
                    'air_dryer',
                    'auto_toilet'
                ],
                'average_ratings': {
                    'cleanliness': 3.2,
                    'privacy': 1.2,
                    'smell': 2.7,
                    'toilet_paper_quality': 4.5
                },
                'building_id': 0,
                'building_title': 'Engineering',
                'comment': 'Engineering 1',
                'floor': 1,
                'gender': 'women',
                'is_favorite': True,
                'location': {
                    'latitude': 12.2,
                    'longitude': 17.9
                },
                'overall_rating': 2.9000000000000004,
                'review_count': 0,
                'stall_count': 4,
                'urinal_count': 0
            },
            {
                'amenities': [
                    'air_dryer',
                    'auto_toilet'
                ],
                'average_ratings': {
                    'cleanliness': 3.2,
                    'privacy': 1.2,
                    'smell': 2.7,
                    'toilet_paper_quality': 4.5
                },
                'building_id': 0,
                'building_title': 'Engineering',
                'comment': 'Engineering 2',
                'floor': 1,
                'gender': 'men',
                'is_favorite': True,
                'location': {
                    'latitude': 114,
                    'longitude': 200.5
                },
                'overall_rating': 3,
                'review_count': 0,
                'stall_count': 4,
                'urinal_count': 3
            }
        ]
        for item in returned_data:
            item.pop("created_at", None)
            item.pop("id", None)
        self.assertEqual(expected_data, returned_data)

    def test_delete_favorites(self):
        # response = self.app.delete("/users/favorites/",
        # json={"washroom_id": 0})
        # self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
        pass

    def test_put_user_preferences(self):
        data = {
            "gender": "women",
            "wheelchair_accessible": True,
            "main_floor_access": False
        }
        response = self.app.put("/users/preferences/", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
