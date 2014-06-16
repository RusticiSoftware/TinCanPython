#!/usr/bin/env python

import unittest
from test_utils import TinCanBaseTestCase
from tincan.version import Version
from tincan.about import About


class AboutTest(TinCanBaseTestCase):

    def test_defaults(self):
        a = About()
        self.assertEqual(a.version, Version.latest)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AboutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

