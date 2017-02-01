#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import test.all_tests
import sys

sys.stdout.write('Galaxie-Bob Unit Test script\n')
sys.stdout.write('----------------------------\n')
sys.stdout.flush()

testSuite = test.all_tests.create_test_suite()
text_runner = unittest.TextTestRunner(verbosity=0).run(testSuite)
