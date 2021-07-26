import unittest
import requests

"""
Run first in Python Terminal:
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
"""


class TestMain(unittest.TestCase):
    def setup(self):
        print("About to test a function")

    def test_status(self):
        """
        GIVEN a Status Code
        WHEN checking if the endpoint is reached when the flask app is running
        THEN verify the status code is correct ( 200 ).
        """
        test_status = 200
        req = requests.get("http://127.0.0.1:5000/house/1")
        status_code = req.status_code
        self.assertEqual(status_code, test_status)

    def test_has_body(self):
        """
        GIVEN a Status Code
        WHEN checking if the response has a body when the flask app is running
        THEN verify the body is not empty.
        """
        req = requests.get("http://127.0.0.1:5000/house/1")
        body = req.json()
        self.assertIsNotNone(body)

    def test_endpoint(self):
        """
        GIVEN an house Id to retrieve
        WHEN checking the response
        THEN verify that the Id retrieved is correct
        """
        req = requests.get("http://127.0.0.1:5000/house/5")
        id = req.json()["Id"]
        self.assertEqual(id, 5)

    def test_id_is_a_num(self):
        """
        GIVEN a n house Id to retrieve
        WHEN checking the response
        THEN verify that the Id retrieved is a type integer
        """
        req = requests.get("http://127.0.0.1:5000/house/123")
        id = req.json()["Id"]
        self.assertTrue(int(id))

    def teardown(self):
        print("Cleaning up")


if __name__ == "__main__":
    unittest.main()
