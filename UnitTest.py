#!/usr/bin/env python3

import sys
import asyncio
import unittest
from Client import Client
from Server import Server

class TestServerMethods(unittest.TestCase):

    def setUp(self):
        print('Setting up server...')

    def tearDown(self):
        print('Disconnecting...')

    def test_connection_made(self):
        print('Testing connection')
        self.assertEqual(True, False)

    def test_data_received(self):
        print('Testing message reception')
        self.assertEqual(True, False)

    def test_messageMaker(self):
        print('Testing message delivery')
        self.assertEqual(True, False)

    def test_validateEvent(self):
        print('Testing event selection')
        self.assertEqual(True, False)

    def test_sendToAll(self):
        print('Testing disconection')
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
