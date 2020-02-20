import api
import json
import unittest


class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_by_id(self):
        response = self.app.get("/reviews/1")
        data = json.loads(response.data.decode())
        expected_data = {
            "comment": "boo",
            "id": 1,
            "rating": {
                "cleanliness": 2.2,
                "privacy": 4.2,
                "smell": 2.8,
                "toilet_paper_quality": 4.2
            },
            "upvote_count": 10,
            "washroom_id": 1
        }
        self.assertEqual(response.status_code, 200)
        data.pop("created_at", None)
        self.assertEqual(data, expected_data)
