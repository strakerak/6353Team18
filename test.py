import unittest
from main import app


class MyTestCase(unittest.TestCase):
    def test_loginpage_succeeds(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue('200' in str(response))

    def test_registrationpage_succeeds(self):
        tester = app.test_client(self)
        response = tester.post("/", data=dict(
            username="admin",
            password="password"
        ))
        self.assertTrue('302' in str(response))

    def test_profileget_succeeds(self):
        tester = app.test_client(self)
        response = tester.get("/profile")
        self.assertTrue('200' in str(response))

    def test_profilepost_succeeds(self):
        tester = app.test_client(self)
        response = tester.post("/profile", data=dict(
            fullname="fgsdfgsfgsgsdgrere",
            address1="sfsafskk",
            address2="sdfdgsghh",
            city="Houston",
            state="Texas",
            zipcode=77025

        ))
        self.assertTrue('302' in str(response))

    def test_quotepost_succeeds(self):
        tester = app.test_client(self)
        response = tester.post("/quote", data=dict(
            quantity=12
        ))
        self.assertTrue('302' in str(response))

    def test_histroyget_succeeds(self):
        tester = app.test_client(self)
        response = tester.get("/history")
        self.assertTrue('200' in str(response))

if __name__ == '__main__':
    unittest.main()
