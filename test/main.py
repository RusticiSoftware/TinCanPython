#!/usr/bin/env python

"""
Discovers and runs all tests in the test module.

All tests must end in '_test.py' to be included in the test. It is
highly recommended that tests be named in the format
'<module_name>_test.py'.
"""
import unittest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('test', pattern='*_test.py', top_level_dir='test/..')
    unittest.TextTestRunner(verbosity=2).run(suite)