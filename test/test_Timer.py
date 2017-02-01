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

    def test_if_set_fps_memory_return_empty_list_when_param_is_none(self):
        """Test if _get_fps_memory() return a empty list() when _set_fps_memory(None)"""
        # our empty list
        value_list = list()
        # we set the None value
        self.timer._set_fps_memory(None)
        # compare if list are equal
        self.assertListEqual(self.timer._get_fps_memory(), value_list)

    def test_if_fps_memory_list_have_a_adaptive_size(self):
        """Test: if by play with set _set_frame_max the get_fps_memory() return list have the good size"""
        # generate a number it will represent the size of the list
        value_random = int(randint(8, 250))
        # generate a list it have random_value as length
        value_list = sample(range(251), value_random)
        # reset the list of the timer
        self.timer._set_fps_memory(None)
        # allow the large list to be store
        self.timer._set_frame_max(value_random)
        # push all the generated list inside the fps_memory_list
        for value in value_list:
            # we use push method
            self.timer._push_fps_memory(value)
        # check list len
        len_1 = len(value_list)
        len_2 = len(self.timer._get_fps_memory())
        # it should be equal
        self.assertEqual(len_1, len_2)

    # Test the __be_fast attribute
    def test_get_set__be_bast(self):
        """Test if __be_bast have the get and set methods it work"""
        value_tested = True
        self.timer._set_be_fast(value_tested)
        value_returned = self.timer._get_be_fast()
        self.assertEqual(value_tested, value_returned)

    def test_raise_set__be_bast(self):
        """Test raise TypeError when _set_be_fast() use a wrong type"""
        self.assertRaises(TypeError, self.timer._set_be_fast, str('Hello World!'))

    # Test the __be_fast_multiplicator attribute
    def test_get_set_be_fast_multiplicator(self):
        """Test if __be_fast_multiplicator have the get and set methods it work"""
        value_random = int(randint(1, 250))
        self.timer._set_be_fast_multiplicator(value_random)
        self.assertEqual(self.timer._get_be_fast_multiplicator(), value_random)

    def test_raise_set_be_fast_multiplicator(self):
        """Test raise TypeError when _set_be_fast_multiplicator() use a wrong type"""
        self.assertRaises(TypeError, self.timer._set_be_fast_multiplicator, str('Hello World!'))

# Run test if call directly
if __name__ == '__main__':
    sys.stdout.write('Galaxie-Bob Unit Test Timer Class script\n')
    sys.stdout.write('-----------------------------------------\n')
    sys.stdout.flush()
    unittest.main(verbosity=0)
