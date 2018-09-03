import sys
import asyncio
import unittest

class TestServerMethods(unittest.TestCase):

    def setUp(self):
        print('Setting up server...')

    def tearDown(self):
        print('Disconnecting...')

    def testConnection(self):
        print('Testing connection')
        self.assertEqual(True, False)

    def testReceiveMessage(self):
        print('Testing message reception')
        self.assertEqual(True, False)

    def testSendMessage(self):
        print('Testing message delivery')
        self.assertEqual(True, False)

    def testSelectEvent(self):
        print('Testing event selection')
        self.assertEqual(True, False)

    def testDisconection(self):
        print('Testing disconection')
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
