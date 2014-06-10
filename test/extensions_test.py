#!/usr/bin/env python

from extensions import Extensions
from test_utils import TinCanBaseTestCase


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