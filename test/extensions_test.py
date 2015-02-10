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

import unittest

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import Extensions
from test_utils import TinCanBaseTestCase


class ExtensionsTest(TinCanBaseTestCase):
    def test_serialize_deserialize(self):
        ext = Extensions()
        ext['http://example.com/string'] = 'extensionValue'
        ext['http://example.com/int'] = 10
        ext['http://example.com/double'] = 1.897

        # ext['http://example.com/object'] = get_agent('Random', 'mbox', 'mailto:random@example.com')

        self.assertSerializeDeserialize(ext)

    def test_serialize_deserialize_init(self):
        data = {
            'http://example.com/string': 'extensionValue',
            'http://example.com/int': 10,
            'http://example.com/double': 1.897,
            # 'http://example.com/object': get_agent('Random', 'mbox', 'mailto:random@example.com'),
        }

        ext = Extensions(data)
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
