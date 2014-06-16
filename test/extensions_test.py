#!/usr/bin/env python

from tincan.extensions import Extensions
from test_utils import TinCanBaseTestCase
import unittest

class ExtensionsTest(TinCanBaseTestCase):
    def test_serialize_deserialize(self):
        ext = Extensions()
        ext['http://example.com/string'] = 'extensionValue'
        ext['http://example.com/int'] = 10
        ext['http://example.com/double'] = 1.897

        #ext['http://example.com/object'] = get_agent('Random', 'mbox', 'mailto:random@example.com')

        self.assertSerializeDeserialize(ext)

    def test_serialize_deserialize_init(self):
        data = {
            'http://example.com/string': 'extensionValue',
            'http://example.com/int': 10,
            'http://example.com/double': 1.897,
            # 'http://example.com/object': get_agent('Random', 'mbox', 'mailto:random@example.com'),
        }

        ext = Extensions(data=data)
        self.assertSerializeDeserialize(ext)

    def test_read_write(self):
        ext = Extensions()
        self.assertEqual(len(ext), 0, 'Empty Extensions inited as non-empty!')

        ext['http://example.com/int'] = 10
        self.assertIn('http://example.com/int', ext, 'Could not add item to Extensions!')
        self.assertEqual(10, ext['http://example.com/int'])
        self.assertEqual(len(ext), 1, 'Extensions is the wrong size!')

        ext['http://example.com/int'] += 5
        self.assertEqual(15, ext['http://example.com/int'], 'Could not modify item in Extensions!')

        del ext['http://example.com/int']
        self.assertNotIn('http://example.com/int', ext, 'Could not delete item from Extensions!')
        self.assertEqual(len(ext), 0, 'Could not empty the Extensions object!')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ExtensionsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

