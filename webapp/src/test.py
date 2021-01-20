import unittest
from app import app

class TestIndex(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_index_post_statuscode(self):
        tester = app.test_client(self)
        response = tester.post("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_post_content(self):
        tester = app.test_client(self)
        response = tester.post("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

class TestAPI(unittest.TestCase):
    def test_api_statuscode(self):
        tester = app.test_client(self)
        response = tester.get("/api_search")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_api_content(self):
        tester = app.test_client(self)
        response = tester.get("/api_search")
        self.assertEqual(response.content_type, "application/json")

    def test_api_data_statuscode(self):
        tester = app.test_client(self)
        response = tester.get("/api_search?data=hi")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_apiID_content(self):
        tester = app.test_client(self)
        response = tester.get("/api_search?data=hi")
        self.assertEqual(response.content_type, "application/json")

class TestDeletion(unittest.TestCase):
    def test_del_statuscode(self):
        tester = app.test_client(self)
        response = tester.get("/del")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_del_content(self):
        tester = app.test_client(self)
        response = tester.get("/del")
        self.assertEqual(response.content_type, "application/json")

    def test_del_data_statuscode(self):
        tester = app.test_client(self)
        response = tester.get("/del?id=1600")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_delid_content(self):
        tester = app.test_client(self)
        response = tester.get("/del?id=1600")
        self.assertEqual(response.content_type, "application/json")

if __name__ == "__main__":
    unittest.main()
