#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GLXBob
import unittest
from random import randint, sample
from time import time
import sys


# Unittest
class TestTimer(unittest.TestCase):

    def setUp(self):
        # Before the test start
        self.timer = GLXBob.Timer()
        sys.stdout.write(str(self.shortDescription() + ' ... '))

    def tearDown(self):
        # When the test is finish
        sys.stdout.write('OK\n')
        sys.stdout.flush()

    # Test "fps" attribute
    def test_get_set_fps(self):
        """Test fps attribute with set_fps() and get_fps() method's"""
        random_value = randint(1, 250)
        self.timer.set_fps_max(float(random_value))
        self.timer.set_fps(float(random_value))
        self.assertEqual(float(random_value), self.timer.get_fps())

    def test_raise_typeerror_set_fps(self):
        """Test raise TypeError when set fps with worng type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps, int(random_value))

    # Test "min_fps" attribute
    def test_get_set_min_fps(self):
        """Test min_fps attribute with set_min_fps() and get_min_fps() method's"""
        random_value = randint(1, 250)
        self.timer.set_fps_min(float(random_value))
        self.assertEqual(self.timer.get_fps_min(), float(random_value))

    def test_raise_typeerror_set_min_fps(self):
        """Test raise TypeError when set min_fps with worng type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps_min, int(random_value))

    # Test "max_fps" attribute
    def test_get_set_max_fps(self):
        """Test max_fps attribute with set_max_fps() and get_max_fps() method's"""
        random_value = randint(1, 250)
        self.timer.set_fps_max(float(random_value))
        self.assertEqual(self.timer.get_fps_max(), float(random_value))

    def test_raise_typeerror_set_max_fps(self):
        """Test raise TypeError when set max_fps with worng type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps_max, int(random_value))

    # Test "fps_increment" attribute
    def test_get_set_fps_increment(self):
        """Test fps_increment attribute with set_fps_increment() and get_fps_increment() method's"""
        random_value = randint(1, 250)
        self.timer.set_fps_increment(float(random_value))
        self.assertEqual(self.timer.get_fps_increment(), float(random_value))

    def test_raise_typeerror_set_fps_increment(self):
        """Test raise TypeError when set fps_increment with worng type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps_increment, int(random_value))

    # Test "min_fps_increment" attribute
    def test_get_set_min_fps_increment(self):
        """Test min_fps_increment attribute with set_min_fps_increment() and get_min_fps_increment() method's"""
        random_value = randint(1, 250)
        self.timer.set_fps_min_increment(float(random_value))
        self.assertEqual(self.timer.get_fps_min_increment(), float(random_value))

    def test_raise_typeerror_set_min_fps_increment(self):
        """Test raise TypeError when set min_fps_increment with worng type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps_min_increment, int(random_value))

    # Test "max_fps_increment" attribute
    def test_get_set_max_fps_increment(self):
        """Test max_fps_increment attribute with set_max_fps_increment() and get_min_fps_increment() method's"""
        random_value = float(randint(1, 250))
        self.timer.set_fps_max_increment(random_value)
        self.assertEqual(self.timer.get_fps_max_increment(), random_value)

    def test_raise_typeerror_set_max_fps_increment(self):
        """Test raise TypeError when set fps_max_increment with wrong type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer.set_fps_max_increment, int(random_value))

    # Test get_time()
    def test_get_time_return(self):
        """Test get_time() method"""
        returned_value_1 = self.timer.get_time()
        returned_value_2 = self.timer.get_time()
        self.assertLessEqual(returned_value_1, returned_value_2)

    ########################
    # Test internal method #
    ########################
    # Test "max_frame" attribute
    def test_get_set__max_frame(self):
        """Test max_frame attribute with _set_frame_max() and _get_frame_max() method's"""
        random_value = randint(1, 250)
        self.timer._set_frame_max(int(random_value))
        self.assertEqual(self.timer._get_frame_max(), float(random_value))

    def test_raise_typeerror_set__max_frame(self):
        """Test if _set_frame_max() raise TypeError when use a wrong type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer._set_frame_max, float(random_value))

    # Test "frame" attribute
    def test_get_set__frame(self):
        """Test frame attribute with _set_frame() and _get_frame() method's"""
        random_value = randint(1, 250)
        self.timer._set_frame(int(random_value))
        self.assertEqual(self.timer._get_frame(), float(random_value))

    def test_raise_typeerror_set__frame(self):
        """Test if _set_frame() raise TypeError when use a wrong type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer._set_frame, float(random_value))

    # Test "departure_time" attribute
    def test_get_set__departure_time(self):
        """Test __departure_time attribute with _set_time_departure() and _get_time_departure() method's"""
        tested_value = time()
        self.timer._set_time_departure(tested_value)
        self.assertEqual(self.timer._get_time_departure(), tested_value)

    # Test "fps_memory" attribute
    def test_get_set__fps_memory(self):
        """Test fps_memory attribute with _set_fps_memory() and _get_fps_memory() method's"""
        value_list = sample(range(30), 4)
        self.timer._set_fps_memory(value_list)
        self.assertListEqual(self.timer._get_fps_memory(), value_list)

    def test_raise_typeerror__set_fps_memory(self):
        """Test if _set_fps_memory() raise TypeError when use a wrong type"""
        random_value = randint(1, 250)
        self.assertRaises(TypeError, self.timer._set_fps_memory, float(random_value))

    def test_if_set_fps_memory_return_list(self):
        """Test if _get_fps_memory() return a empty list when _set_fps_memory(None)"""
        value_list = [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0]
        self.timer._set_fps_memory(None)
        self.assertListEqual(self.timer._get_fps_memory(), value_list)

# Run test if call directly
if __name__ == '__main__':
    sys.stdout.write('Galaxie-Bob Unit Test script\n')
    sys.stdout.write('----------------------------\n')
    sys.stdout.flush()
    unittest.main(verbosity=0)
