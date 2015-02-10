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
from test_utils import TinCanBaseTestCase
from tincan import Version, About


class AboutTest(TinCanBaseTestCase):
    def test_defaults(self):
        a = About()
        self.assertEqual(a.version, [Version.latest])

    def test_serialize_deserialize(self):
        a = About(version=['1.0.1', '1.0.0'], extensions={
            'extension-a': 'http://www.example.com/ext/a',
            'extension-b': 'http://www.example.com/ext/b',
        })

        self.assertEqual(a.version, ['1.0.1', '1.0.0'])
        self.assertIn('extension-a', a.extensions)
        self.assertIn('extension-b', a.extensions)

        self.assertSerializeDeserialize(a)

    def test_serialize_deserialize_init(self):
        data = {
            'version': ['1.0.0'],
            'extensions': {
                'extension-a': 'http://www.example.com/ext/a',
                'extension-b': 'http://www.example.com/ext/b',
            },
        }

        a = About(data)

        self.assertEqual(a.version, ['1.0.0'])
        self.assertIn('extension-a', a.extensions)
        self.assertIn('extension-b', a.extensions)

        self.assertSerializeDeserialize(a)

    def test_bad_property_init(self):
        with self.assertRaises(AttributeError):
            About(bad_name=2)

        with self.assertRaises(AttributeError):
            About({'bad_name': 2})

    def test_bad_version_init(self):
        About(version='1.0.1')
        About(version=['1.0.1'])
        About(version=['1.0.1', '1.0.0'])

        with self.assertRaises(ValueError):
            About(version='bad version')

        with self.assertRaises(ValueError):
            About(version=['bad version'])

        with self.assertRaises(ValueError):
            About(version=['1.0.1', 'bad version'])

        with self.assertRaises(ValueError):
            About(version=['1.0.1', 'bad version'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AboutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
