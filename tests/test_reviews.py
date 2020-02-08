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
        response = self.app.get("/reviews/123")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "review: 123")

    def tearDown(self):
        pass
