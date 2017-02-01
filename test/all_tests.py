import glob
import unittest


def create_test_suite():
    test_file_strings = glob.glob('test/test_*.py')
    module_strings = ['test.' + file_str[5:len(file_str) - 3] for file_str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) for name in module_strings]
    test_suite = unittest.TestSuite(suites)
    return test_suite
