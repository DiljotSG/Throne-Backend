import json
import unittest

from handler import app


class TestAPI(unittest.TestCase):
    # Set up for the test cases
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_main_page(self):
        response = self.app.get('/')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    # Clean up after the test cases
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
