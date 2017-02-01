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
    def test_get_set__is_running(self):
        """MainLoop: Test '__is_running' attribute with 'MainLoop.get()' and 'MainLoop.set()' method's """
        value_tested = True
        self.mainloop._set_is_running(value_tested)
        value_returned = self.mainloop._get_is_running()
        self.assertEqual(value_tested, value_returned)

    def test_is_running(self):
        """MainLoop: Test '__is_running' value with 'MainLoop.is_running()' method """
        value_tested = True
        self.mainloop._set_is_running(value_tested)
        value_returned = self.mainloop.is_running()
        self.assertEqual(value_tested, value_returned)

    def test_raise_set__be_bast(self):
        """MainLoop: Test raise TypeError when MainLoop._set_is_running() use wrong parameter type"""
        self.assertRaises(TypeError, self.mainloop._set_is_running, str('Hello World!'))

    # Test __timer attribute
    def test_get_set__timer(self):
        """MainLoop: Test '__timer' attribute setting with 'MainLoop.set_timer()' and 'MainLoop.get_timer()'method's """
        mainloop = GLXBob.MainLoop()
        timer = GLXBob.Timer()
        self.assertNotEqual(timer, mainloop.get_timer())

        mainloop.set_timer(timer)
        self.assertEqual(timer, mainloop.get_timer())

    def test_reset__timer(self):
        """MainLoop: Test '__timer' attribute setting with 'MainLoop.set_timer()' None"""
        # We prepare our own mainloop and timer for our tests
        mainloop = GLXBob.MainLoop()
        # Set the timer without parameter, it's suppose to reset the time by create a new one
        mainloop.set_timer()
        # Check Default value
        fps = 60.0
        fps_max = float("inf")
        fps_min = 1.0
        fps_increment = 0.1
        fps_min_increment = 0.1
        fps_max_increment = 10.0
        self.assertEqual(fps, mainloop.get_timer().get_fps())
        self.assertEqual(fps_max, mainloop.get_timer().get_fps_max())
        self.assertEqual(fps_min, mainloop.get_timer().get_fps_min())
        self.assertEqual(fps_increment, mainloop.get_timer().get_fps_increment())
        self.assertEqual(fps_min_increment, mainloop.get_timer().get_fps_min_increment())
        self.assertEqual(fps_max_increment, mainloop.get_timer().get_fps_max_increment())

# Run test if call directly
if __name__ == '__main__':
    sys.stdout.write('Galaxie-Bob Unit Test Timer Class script\n')
    sys.stdout.write('-----------------------------------------\n')
    sys.stdout.flush()
    unittest.main(verbosity=0)
