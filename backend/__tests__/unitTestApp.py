# Importing libraries
import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

# Test class that contains unit test functions, testing functions in the app.py file
class FlaskAppTestCase(unittest.TestCase):

    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Mocks for the database connection and urlAnalyser functions
    @patch('app.createDbConnection')  
    @patch('app.urlAnalyser')     

    # Testing the urlAnalyser function for a safe URL
    def testingSafeUrl(self, urlAnalyserFunctionMock, createDbFunctionMock):
        # Mocking the urlAnalyser function to return a 'safe' result
        urlAnalyserFunctionMock.return_value = {'result': 'safe'}


        with self.app as client:
            # Logged in user is simulated (set cookie)
            client.set_cookie(key='username', value='testuser')
            # Simulate a POST request to the validate function
            response = client.post('/validate', json={'url': 'https://safe.com'})

        # Check the response status code and that the result is 'safe'
        self.assertEqual(response.status_code, 200)
        self.assertIn('safe', response.get_data(as_text=True))

    # Mocks for the database connection and urlAnalyser functions
    @patch('app.createDbConnection')
    @patch('app.urlAnalyser')
    # Testing the urlAnalyser function for a bad URL
    def testingBadUrl(self, urlAnalyserFunctionMock, createDbFunctionMock):
        # Mocking the urlAnalyser function to return a 'bad' result
        urlAnalyserFunctionMock.return_value = {'result': 'bad'}

        with self.app as client:
            # Logged in user is simulated (set cookie)
            client.set_cookie(key='username', value='testuser')
            # Simulate a POST request to the validate function
            response = client.post('/validate', json={'url':'http://malicious.com'})

        # Check the response status code and that the result is 'bad'
        self.assertEqual(response.status_code, 200)
        self.assertIn('bad', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
