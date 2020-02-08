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


class TestReviewAPI(unittest.TestCase):
    def setUp(self):
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


class TestBuildingsAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get("/buildings?location=12")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "building at location = 12")

    def test_by_id(self):
        response = self.app.get("/buildings/123")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "building: 123")

    def test_washrooms(self):
        response = self.app.get("/buildings/123/washrooms")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "washrooms in building: 123")

    def tearDown(self):
        pass


class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_by_id(self):
        response = self.app.get("/users/123")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "user: 123")

    def test_reviews(self):
        response = self.app.get("/users/123/reviews")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "reviews from user: 123")

    def test_favorites(self):
        response = self.app.get("/users/123/favorites")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data["msg"]), "favorites of user: 123")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
