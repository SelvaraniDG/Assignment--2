# importing module
from app import app
import unittest


class CountryCapitalTestCase(unittest.TestCase):

    # testing index page response
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # testing correct country capital returning
    def test_country_capital(self):
        tester = app.test_client(self)
        response = tester.get('/capital/India', content_type='html/text')
        self.assertTrue(b'New Delhi' in response.data)

    # testing country capital from post method and redirect check
    def test_post_country_redirect(self):
        tester = app.test_client(self)
        response = tester.post(
            '/capital', json={"country": "Germany"}, follow_redirects=True)
        self.assertIn(b'Berlin', response.data)

    # testing incorrect country name
    def test_incorrect_country(self):
        tester = app.test_client(self)
        response = tester.get('/capital/Andaman', content_type='html/text')
        self.assertEqual(response.status_code, 404)


# test case entry point
if __name__ == '__main__':
    unittest.main()
