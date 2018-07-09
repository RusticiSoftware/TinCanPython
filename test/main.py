# Copyright 2014 Rustici Software
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Discovers and runs all tests in the test module.

All tests must end in '_test.py' to be included in the test. It is
highly recommended that tests be named in the format
'<module_name>_test.py'.
"""
import unittest
import sys
import os
from os.path import dirname, join as path_join


def add_tincan_to_path(dirpath):
    tincan_path = path_join(dirpath, 'tincan')
    if os.path.isdir(tincan_path) and dirpath not in sys.path:
        sys.path.append(dirpath)
        return True
    return False


def check_tincan_importability():
    try:
        import tincan
    except ImportError as e:
        tincan = None
        raise ImportError(
            "Could not import tincan."
            "\n\n"
            "This probably means that the test directory is not a "
            "sibling directory of tincan. Move test and tincan into "
            "the same folder and try again."
            "\n\n" + e.message
        )


def locate_package(pkg):
    this_file = os.path.abspath(__file__)
    path = this_file
    while not os.path.isdir(os.path.join(path, pkg)):
        path = dirname(path)
        if not path or dirname(path) == path:
            return False
    return path


def setup_tincan_path():
    tincan_pardir = locate_package('tincan')
    if tincan_pardir and tincan_pardir not in sys.path:
        #
        # using sys.path.insert in this manner is considered a little evil,
        # see http://stackoverflow.com/questions/10095037/why-use-sys-path-appendpath-instead-of-sys-path-insert1-path
        # but this is better than using the sys.path.append as before
        # as that was catching the system installed version, if virtualenv
        # is ever implemented for the test suite then this can go away
        #
        print("Adding %s to PYTHONPATH" % repr(tincan_pardir))
        sys.path.insert(1, tincan_pardir)
    check_tincan_importability()


if __name__ == '__main__':
    setup_tincan_path()

    loader = unittest.TestLoader()
    test_pardir = locate_package('test')
    test_dir = os.path.join(test_pardir, 'test')
    suite = loader.discover(test_dir, pattern='*_test.py')
    ret = not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    sys.exit(ret)
