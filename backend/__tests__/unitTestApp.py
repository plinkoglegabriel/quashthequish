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
        
    # Mocks for the database connection function
    @patch('app.createDbConnection')
    def testingUsernameExisting(self, createDbFunctionMock):
        # Making database connection using the mocked function
        mockConnection = createDbFunctionMock.return_value
        mockCursor = mockConnection.cursor.return_value
        mockCursor.fetchone.return_value = {'userId': 1} 

        # Simulate an existing user
        response = self.app.post('/check-username', json={'username': 'existingUser'})
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON to assert value, checkin
        json_data = response.get_json()
        self.assertTrue(json_data.get('exists'))

    @patch('app.createDbConnection')
    def testingUsernameCreationOfNewUser(self, createDbFunctionMock):
        # Mocked database connection where new user does not exist
        mockConnection = createDbFunctionMock.return_value
        mockCursor = mockConnection.cursor.return_value
        mockCursor.fetchone.return_value = None  

        # Simulate a new user
        response = self.app.post('/check-username', json={'username': 'newUser'})
        self.assertEqual(response.status_code, 200)

        # Parse JSON and assert value
        json_data = response.get_json()
        self.assertFalse(json_data.get('exists'))

if __name__ == '__main__':
    unittest.main()
