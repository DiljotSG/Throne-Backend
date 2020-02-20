import json
import unittest
import api


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
        expected = {
            "comment": "boo",
            "created_at": data["created_at"],
            "id": 1,
            "ratings": [],
            "upvote_count": 10,
            "washroom_id": 1
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected)

    def tearDown(self):
        pass
