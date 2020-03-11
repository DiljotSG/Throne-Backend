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

    def test_get_root(self):
        response = self.app.get(
            "/users",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        data = json.loads(response.data.decode())
        expected_data = {
            "id": 0,
            "profile_picture": "picture",
            "username": "janesmith"
        }

        # Check it has a created at field
        created_at = data.pop("created_at", None)
        self.assertIsNotNone(created_at)

        # Check it has the correct data
        self.assertEqual(data, expected_data)

    def test_get_user_by_id(self):
        response = self.app.get("/users/1")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        data = json.loads(response.data.decode())
        expected_data = {
            "id": 1,
            "profile_picture": "picture",
            "username": "johnsmith"
        }

        # Check it has a created at field
        created_at = data.pop("created_at", None)
        self.assertIsNotNone(created_at)

        # Check it has the correct data
        self.assertEqual(data, expected_data)

    def test_get_users_reviews(self):
        response = self.app.get("/users/1/reviews")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        data = json.loads(response.data.decode())
        expected_data = [
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

        # Check it has a created at field
        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)

        # Remove created at field
        if "user" in data[0]:
            user = data[0]["user"]
            created_at_user = user.pop("created_at", None)
            self.assertIsNotNone(created_at_user)

        # Check it has the correct data
        self.assertEqual(data, expected_data)

    def test_get_reviews(self):
        response = self.app.get("/users/reviews")
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

        # Check it has a created at field
        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)

        # Remove created at field
        if "user" in data[0]:
            user = data[0]["user"]
            created_at_user = user.pop("created_at", None)
            self.assertIsNotNone(created_at_user)

        # Check it has the correct data
        self.assertEqual(data, expected_data)

    def test_get_reviews_equiv(self):
        # These are equivalent endpoints
        # Test that they give the same data
        response_one = self.app.get("/users/0/reviews")
        self.assertEqual(response_one.status_code, HttpCodes.HTTP_200_OK)
        data_one = json.loads(response_one.data.decode())

        response_two = self.app.get("/users/reviews")
        self.assertEqual(response_two.status_code, HttpCodes.HTTP_200_OK)
        data_two = json.loads(response_two.data.decode())

        self.assertEqual(data_one, data_two)

    def test_get_favorites(self):
        response = self.app.get("/users/favorites")
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

        data = json.loads(response.data.decode())
        expected_data = [
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

        # Check it has a created at field
        created_at = data[0].pop("created_at", None)
        self.assertIsNotNone(created_at)

        # Check that the favorite list has the correct data
        for item in data:
            if "is_favorite" in item:
                self.assertTrue(item["is_favorite"])

        # Check it has the correct data
        self.assertEqual(data, expected_data)

    def test_post_user_favorites(self):
        # We can post with both parameter types, so test both
        data_one = {
            "id": 1,
        }
        data_two = {
            "washroom_id": 1,
        }

        response_one = self.app.post("/users/favorites", json=data_one)
        response_two = self.app.post("/users/favorites", json=data_two)
        self.assertEqual(response_one.status_code, HttpCodes.HTTP_201_CREATED)
        self.assertEqual(response_two.status_code, HttpCodes.HTTP_201_CREATED)

        returned_data_one = json.loads(response_one.data.decode())
        returned_data_two = json.loads(response_two.data.decode())

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

        # Remove all the created_at fields
        for item in returned_data_one:
            created_at = item.pop("created_at", None)
            self.assertIsNotNone(created_at)
            the_id = item.pop("id", None)
            self.assertIsNotNone(the_id)
        for item in returned_data_two:
            created_at = item.pop("created_at", None)
            self.assertIsNotNone(created_at)
            the_id = item.pop("id", None)
            self.assertIsNotNone(the_id)

        # Check that the favorite list has the correct data
        for item in returned_data_one:
            if "is_favorite" in item:
                self.assertTrue(item["is_favorite"])
        for item in returned_data_two:
            if "is_favorite" in item:
                self.assertTrue(item["is_favorite"])

        # Check it has the correct data
        self.assertEqual(expected_data, returned_data_one)
        self.assertEqual(expected_data, returned_data_two)

    def test_delete_favorite(self):
        data = {
            "id": 2,
        }
        response = self.app.post("/users/favorites", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_201_CREATED)
        response = self.app.delete(
            "/users/favorites",
            json={"washroom_id": 2}
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_204_NO_CONTENT)
        response = self.app.delete(
            "/users/favorites",
            json={"washroom_id": 2}
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_404_NOT_FOUND)

    def test_delete_favorite_error(self):
        response = self.app.delete(
            "/users/favorites",
            json={"washroom_id": 1}
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_404_NOT_FOUND)

    def test_put_user_preferences(self):
        data = {
            "gender": "women",
            "wheelchair_accessible": True,
            "main_floor_access": False
        }
        response = self.app.put("/users/preferences", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)

    def test_put_user_preferences_error(self):
        data = {
            "hi": "diljot",
            "hello": "james",
        }
        response = self.app.put("/users/preferences", json=data)
        self.assertEqual(response.status_code, HttpCodes.HTTP_400_BAD_REQUEST)
