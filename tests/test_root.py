import api
import unittest
from api.response_codes import HttpCodes


class TestRoot(unittest.TestCase):
    def setUp(self):
        app = api.create()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_root(self):
        response = self.app.get(
            "/",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, HttpCodes.HTTP_200_OK)
