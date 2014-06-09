"""
    Copyright 2014 Rustici Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import unittest
from tincan.languagemap import LanguageMap
from tincan.languagemap import LanguageMapTypeError

class TestLanguageMap(unittest.TestCase):

    def test_InitNoArgs(self):
        lmap = LanguageMap()
        self.assertEqual(lmap.get_mapping(), {})
        self.assertIsInstance(lmap, LanguageMap)

    def test_InitEmpty(self):
        lmap = LanguageMap({})
        self.assertEqual(lmap.get_mapping(), {})
        self.assertIsInstance(lmap, LanguageMap)

    def test_InitExceptionNotMap(self):
        with self.assertRaises(LanguageMapTypeError):
            lmap = LanguageMap('not map')

    def test_InitExceptionBadMap(self):
        with self.assertRaises(LanguageMapTypeError):
            lmap = LanguageMap({"bad map"})

    def test_InitExceptionNestedObject(self):
        with self.assertRaises(LanguageMapTypeError):
           lmap = LanguageMap({"en-US": {"nested": "object"}})

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
        with self.assertRaises(LanguageMapTypeError):
            lmap = LanguageMap(**obj)

    def test_InitUnpackMapArg(self):
        obj = {"map": {"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"}}
        lmap = LanguageMap(**obj)
        self.mapVerificationHelper(lmap)

    def test_FromJSON(self):
        lmap = LanguageMap.from_json('{"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"}')
        self.mapVerificationHelper(lmap)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            lmap = LanguageMap.from_json('{"bad JSON"}')

    def test_FromJSONExceptionNestedObject(self):
        with self.assertRaises(LanguageMapTypeError):
            lmap = LanguageMap.from_json('{"fr-CA": "test", "en-US": {"nested": "object"}}')

    def test_FromJSONEmptyObject(self):
        lmap = LanguageMap.from_json('{}')
        self.assertIsInstance(lmap, LanguageMap)
        self.assertEqual(lmap.get_mapping(), {})

    def test_AsVersion(self):
        lmap = LanguageMap()
        check = lmap.as_version()
        self.assertEqual(lmap, check)

    def test_ToJSONFromJSON(self):
        json_str = '{"fr-CA": "CA-test", "en-US": "US-test", "fr-FR": "FR-test"}'
        lmap = LanguageMap.from_json(json_str)
        self.mapVerificationHelper(lmap)
        self.assertEqual(lmap.to_json(), json_str)

    def test_ToJSON(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        # since the map is unordered, it is ok that to_json() changes ordering
        self.assertEqual(lmap.to_json(), '{"fr-CA": "CA-test", "en-US": "US-test", "fr-FR": "FR-test"}')

    def test_getItemException(self):
        lmap = LanguageMap()
        with self.assertRaises(AttributeError):
            lmap['en-Anything']

    def test_setItem(self):
        lmap = LanguageMap()
        lmap['en-US'] = 'US-test'
        lmap['fr-CA'] = 'CA-test'
        lmap['fr-FR'] = 'FR-test'
        self.mapVerificationHelper(lmap)

    def test_setItemException(self):
        lmap = LanguageMap()
        with self.assertRaises(LanguageMapTypeError):
            lmap['en-US'] = {"test": "notstring"}
        self.assertEqual(lmap.get_mapping(), {})

    def test_setMapping(self):
        lmap = LanguageMap({"hy-PH": "test", "ph-HY": "test", "en-AT": "test"})
        lmap.set_mapping({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        self.mapVerificationHelper(lmap)

    def test_setMappingExceptionNoArgs(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        with self.assertRaises(TypeError):
            lmap.set_mapping()
        self.mapVerificationHelper(lmap)

    def test_setMappingEmpty(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        lmap.set_mapping({})
        self.assertEqual(len(lmap.get_mapping()), 0)

    def test_setMappingExceptionNestedObject(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        with self.assertRaises(LanguageMapTypeError):
            lmap.set_mapping({"fr-CA": "test", "en-US": {"nested": "object"}})
        self.mapVerificationHelper(lmap)

    def test_setMappingExceptionBadMap(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        with self.assertRaises(LanguageMapTypeError):
            lmap.set_mapping({"bad map"})
        self.mapVerificationHelper(lmap)

    def test_setMappingExceptionNotMap(self):
        lmap = LanguageMap({"en-US": "US-test", "fr-CA": "CA-test", "fr-FR": "FR-test"})
        with self.assertRaises(LanguageMapTypeError):
            lmap.set_mapping("not a map")
        self.mapVerificationHelper(lmap)

    def mapVerificationHelper(self, lmap):
        self.assertIsInstance(lmap, LanguageMap)
        self.assertEqual(len(lmap.get_mapping()), 3)
        self.assertIn('en-US', lmap.get_mapping())
        self.assertIn('fr-CA', lmap.get_mapping())
        self.assertIn('fr-FR', lmap.get_mapping())
        self.assertEqual(lmap['en-US'], 'US-test')
        self.assertEqual(lmap['fr-CA'], 'CA-test')
        self.assertEqual(lmap['fr-FR'], 'FR-test')

#suite = unittest.TestLoader().loadTestsFromTestCase(TestLanguageMap)
#unittest.TextTestRunner(verbosity=2).run(suite)
