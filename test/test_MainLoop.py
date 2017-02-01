#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from random import randint, sample
from time import time
import sys
import os
# Require when you haven't GLXBob as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
import GLXBob


# Unittest
class TestMainLoop(unittest.TestCase):
    def setUp(self):
        # Before the test start
        self.mainloop = GLXBob.MainLoop()
        sys.stdout.write(str(self.shortDescription() + ' ... '))

    def tearDown(self):
        # When the test is finish
        sys.stdout.write('OK\n')
        sys.stdout.flush()

    # Test "__is_running" attribute
    def test_get_set__be_bast(self):
        """MainLoop: Test '__is_running' attribute with 'Timer.get()' and 'Timer.set()' method's """
        value_tested = True
        self.mainloop._set_is_running(value_tested)
        value_returned = self.mainloop._get_is_running()
        self.assertEqual(value_tested, value_returned)

    def test_is_running(self):
        """MainLoop: Test __is_running attribute with 'Timer.is_running' method's """
        value_tested = True
        self.mainloop._set_is_running(value_tested)
        value_returned = self.mainloop.is_running()
        self.assertEqual(value_tested, value_returned)

    def test_raise_set__be_bast(self):
        """MainLoop: Test raise TypeError when set_is_running() use a wrong type"""
        self.assertRaises(TypeError, self.mainloop._set_is_running, str('Hello World!'))


# Run test if call directly
if __name__ == '__main__':
    sys.stdout.write('Galaxie-Bob Unit Test Timer Class script\n')
    sys.stdout.write('-----------------------------------------\n')
    sys.stdout.flush()
    unittest.main(verbosity=0)
