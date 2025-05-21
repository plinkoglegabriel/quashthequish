# Importing libraries
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from detectionAlgorithm import urlAnalyser
# Test class that contains unit test functions, testing the urlAnalyser function
class TestURLAnalyser(unittest.TestCase):
    # Testing for correct result given no HTTPS protocol (asserts bad)
    def testingNoHttpsUrl(self):
        result = urlAnalyser("http://noHttpsExample.com")
        self.assertEqual(result['result'], 'bad')

    # Testing for correct result given with a regular/typical safe URL (asserts safe)
    def testingSafeUrl(self):
        result = urlAnalyser("https://google.com")
        self.assertEqual(result['result'], 'safe')

    # Testing for correct result given a URL that is typosquatting (asserts bad)
    def testingTypoSquattingUrl(self):
        result = urlAnalyser("https://paypai.com")  
        self.assertEqual(result['result'], 'bad')

    # Testing for correct result given a URL that it contains a ip address (asserts bad)
    def testingIpAddressUrl(self):
        result = urlAnalyser("http://192.168.0.1")
        self.assertEqual(result['result'], 'bad')

if __name__ == '__main__':
    unittest.main()
