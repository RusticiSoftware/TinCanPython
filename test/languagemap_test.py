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
import json
import unittest

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import LanguageMap


class LanguageMapTest(unittest.TestCase):
    def test_InitNoArgs(self):
        lmap = LanguageMap()
        self.assertEqual(lmap, {})
        self.assertIsInstance(lmap, LanguageMap)

    def test_InitEmpty(self):
        lmap = LanguageMap({})
        self.assertEqual(lmap, {})
        self.assertIsInstance(lmap, LanguageMap)

    def test_InitExceptionNotMap(self):
        with self.assertRaises(ValueError):
            LanguageMap('not map')

    def test_InitExceptionBadMap(self):
        with self.assertRaises(ValueError):
            LanguageMap({"bad map"})

    def test_InitExceptionNestedObject(self):
        with self.assertRaises(TypeError):
            LanguageMap({"en-US": {"nested": "object"}})

    def test_InitDict(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        self.mapVerificationHelper(lmap)

    def test_InitLanguageMap(self):
        arg = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        lmap = LanguageMap(arg)
        self.mapVerificationHelper(lmap)

    def test_InitUnpack(self):
        obj = {"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"}
        lmap = LanguageMap(**obj)
        self.mapVerificationHelper(lmap)

    def test_InitUnpackExceptionNestedObject(self):
        obj = {"en-US": {"nested": "object"}}
        with self.assertRaises(TypeError):
            LanguageMap(**obj)

    def test_FromJSON(self):
        lmap = LanguageMap.from_json('{"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"}')
        self.mapVerificationHelper(lmap)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            LanguageMap.from_json('{"bad JSON"}')

    def test_FromJSONExceptionNestedObject(self):
        with self.assertRaises(TypeError):
            LanguageMap.from_json('{"fr-CA": "test", "en-US": {"nested": "object"}}')

    def test_FromJSONEmptyObject(self):
        lmap = LanguageMap.from_json('{}')
        self.assertIsInstance(lmap, LanguageMap)
        self.assertEqual(lmap, {})

    def test_AsVersionEmpty(self):
        lmap = LanguageMap()
        check = lmap.as_version()
        self.assertEqual(check, {})

    def test_AsVersionNotEmpty(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        check = lmap.as_version()
        self.assertEqual(check, {"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})

    def test_ToJSONFromJSON(self):
        json_str = '{"fr-CA": "CA-test", "en-US": "US-test", "fr-FR": "FR-test"}'
        lmap = LanguageMap.from_json(json_str)
        self.mapVerificationHelper(lmap)
        self.assertEqual(json.loads(lmap.to_json()), json.loads(json_str))

    def test_ToJSON(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        # since the map is unordered, it is ok that to_json() changes ordering
        self.assertEqual(json.loads(lmap.to_json()),
                         json.loads('{"fr-CA": "CA-test", "en-US": "US-test", "fr-FR": "FR-test"}'))

    def test_getItemException(self):
        lmap = LanguageMap()
        with self.assertRaises(KeyError):
            _ = lmap['en-Anything']

    def test_setItem(self):
        lmap = LanguageMap()
        lmap['en-US'] = 'US-test'
        lmap['fr-CA'] = 'CA-test'
        lmap['fr-FR'] = 'FR-test'
        self.mapVerificationHelper(lmap)

    def test_setItemException(self):
        lmap = LanguageMap()
        with self.assertRaises(TypeError):
            lmap['en-US'] = {"test": "notstring"}
        self.assertEqual(lmap, {})

    def mapVerificationHelper(self, lmap):
        self.assertIsInstance(lmap, LanguageMap)
        self.assertEqual(len(lmap), 3)
        self.assertIn('en-US', lmap)
        self.assertIn('fr-CA', lmap)
        self.assertIn('fr-FR', lmap)
        self.assertEqual(lmap['en-US'], 'US-test')
        self.assertEqual(lmap['fr-CA'], 'CA-test')
        self.assertEqual(lmap['fr-FR'], 'FR-test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LanguageMapTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
