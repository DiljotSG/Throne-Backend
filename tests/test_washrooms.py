import json
import unittest
from handler import app


class TestWashroomAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get("/washrooms")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_by_id(self):
        response = self.app.get("/washrooms/123")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "washroom: 123")

    def test_reviews(self):
        response = self.app.get("/washrooms/123/reviews")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "reviews for washroom: 123")

    def tearDown(self):
        pass
