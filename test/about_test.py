#!/usr/bin/env python

import unittest
from test_utils import TinCanBaseTestCase
from tincan.version import Version
from tincan.about import About


class AboutTest(TinCanBaseTestCase):

    def test_defaults(self):
        a = About()
        self.assertEqual(a.version, Version.latest)

    def test_serialize_deserialize(self):
        a = About(version='1.0.0', extensions={
            'extension-a': 'http://www.example.com/ext/a',
            'extension-b': 'http://www.example.com/ext/b',
        })

        self.assertEqual(a.version, '1.0.0')
        self.assertIn('extension-a', a.extensions)
        self.assertIn('extension-b', a.extensions)

        self.assertSerializeDeserialize(a)

    def test_serialize_deserialize_init(self):
        data = {
            'version': '1.0.0',
            'extensions': {
                'extension-a': 'http://www.example.com/ext/a',
                'extension-b': 'http://www.example.com/ext/b',
            },
        }

        a = About(data)

        self.assertEqual(a.version, '1.0.0')
        self.assertIn('extension-a', a.extensions)
        self.assertIn('extension-b', a.extensions)

        self.assertSerializeDeserialize(a)

    def test_bad_property_init(self):
        with self.assertRaises(AttributeError):
            About(bad_name=2)

        with self.assertRaises(AttributeError):
            About({'bad_name': 2})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AboutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

