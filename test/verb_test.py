#    Copyright 2014 Rustici Software
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
from tincan.verb import Verb
from tincan.languagemap import LanguageMap, LanguageMapTypeError

class TestVerb(unittest.TestCase):

    def test_InitEmpty(self):
        verb = Verb()
        self.assertIsNone(verb.get_id())
        self.assertIsNone(verb.get_display())

    def test_InitExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            verb = Verb('')

    def test_InitId(self):
        verb = Verb('test')
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_InitExceptionBadId(self):
        with self.assertRaises(ValueError):
            verb = Verb(id={})

    def test_InitDisplay(self):
        verb = Verb(display={"en-US": "test"})
        self.assertIsNone(verb.get_id())
        self.displayVerificationHelper(verb.get_display())

    def test_InitEmptyDisplay(self):
        verb = Verb('test', {})
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_InitAnonDisplay(self):
        verb = Verb('test', {"en-US": "test"})
        self.assertEqual(verb.get_id(), 'test')
        self.displayVerificationHelper(verb.get_display())

    def test_InitLanguageMapDisplay(self):
        verb = Verb('test', LanguageMap({"en-US": "test"}))
        self.assertEqual(verb.get_id(), 'test')
        self.displayVerificationHelper(verb.get_display())

    def test_InitEmptyLanguageMapDisplay(self):
        verb = Verb('test', LanguageMap({}))
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_InitUnpackDisplay(self):
        obj = {"display": {"en-US": "test"}}
        verb = Verb(**obj)
        self.displayVerificationHelper(verb.get_display())

    def test_InitUnpack(self):
        obj = {"id": "test", "display": {"en-US": "test"}}
        verb = Verb(**obj)
        self.assertEqual(verb.get_id(), 'test')
        self.displayVerificationHelper(verb.get_display())

    def test_InitExceptionUnpackEmptyId(self):
        obj = {"id": ""}
        with self.assertRaises(ValueError):
            verb = Verb(**obj)

    def test_InitExceptionUnpackBadId(self):
        obj = {"id": {}}
        with self.assertRaises(ValueError):
            verb = Verb(**obj)

    def test_InitExceptionUnpackFlatDisplay(self):
        obj = {"id": "test", "display": "test"}
        with self.assertRaises(LanguageMapTypeError):
            verb = Verb(**obj)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            verb = Verb.from_json('{"bad JSON"}')

    def test_FromJSONExceptionBadId(self):
        with self.assertRaises(ValueError):
            verb = Verb.from_json('{"id": {}}')

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(TypeError):
            verb = Verb.from_json('{"test": "invalid property"}')

    """ An exception is best here to keep client code from thinking its doing \
    something its not when instantiating a Verb """

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(TypeError):
            verb = Verb.from_json('{"test": "invalid property", "id": \
            "valid property"}')

    def test_FromJSONEmptyObject(self):
        verb = Verb.from_json('{}')
        self.assertIsNone(verb.get_id())
        self.assertIsNone(verb.get_display())

    def test_FromJSONExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            verb = Verb.from_json('{"id":"''"}')

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            verb = Verb.from_json('')

    def test_FromJSONId(self):
        verb = Verb.from_json('{"id": "test"}')
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_FromJSONExceptionFlatDisplay(self):
        with self.assertRaises(LanguageMapTypeError):
            verb = Verb.from_json('{"id": "test", "display": "flatdisplay"}')

    def test_FromJSON(self):
        verb = Verb.from_json('{"id": "test", "display": {"en-US": "test"}}')
        self.assertEqual(verb.get_id(), 'test')
        self.displayVerificationHelper(verb.get_display())

    def test_AsVersion(self):
        verb = Verb()
        verb2 = verb.as_version("1.0.0")
        self.assertEqual(verb2, verb)

    def test_ToJSONFromJSON(self):
        json_str = '{"id": "test", "display": {"en-US": "test"}}'
        verb = Verb.from_json(json_str)
        self.assertEqual(verb.get_id(), 'test')
        self.displayVerificationHelper(verb.get_display())
        self.assertEqual(verb.to_json(), json_str)

    def test_ToJSON(self):
        verb = Verb(**{"id": "test", "display": {"en-US": "test"}})
        self.assertEqual(verb.to_json(), '{"id": "test", "display": {"en-US": "test"}}')

    def test_ToJSONIgnoreNoneDisplay(self):
        verb = Verb('test')
        self.assertEqual(verb.to_json(), '{"id": "test"}')

    def test_ToJSONIgnoreNoneId(self):
        verb = Verb(display={"en-US": "test"})
        self.assertEqual(verb.to_json(), '{"display": {"en-US": "test"}}')

    def test_ToJSONEmpty(self):
        verb = Verb()
        self.assertEqual(verb.to_json(), '{}')

    def test_setId(self):
        verb = Verb('test')
        verb.set_id('newId')
        self.assertEqual(verb.get_id(), 'newId')
        self.assertIsNone(verb.get_display())

    def test_setIdExceptionEmptyString(self):
        verb = Verb('test')
        with self.assertRaises(ValueError):
            verb.set_id('')
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_setIdExceptionNotString(self):
        verb = Verb('test')
        with self.assertRaises(ValueError):
            verb.set_id({"not": "string"})
        self.assertEqual(verb.get_id(), 'test')
        self.assertIsNone(verb.get_display())

    def test_setDisplay(self):
        verb = Verb(display=LanguageMap({"fr-CA": "not test"}))
        verb.set_display({"en-US": "test"})
        self.assertIsNone(verb.get_id())
        self.displayVerificationHelper(verb.get_display())

    def test_setDisplayExceptionNestedObject(self):
        verb = Verb(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(LanguageMapTypeError):
            verb.set_display({"fr-CA": {"nested": "object"}})
        self.displayVerificationHelper(verb.get_display())

    def test_setDisplayExceptionBadMap(self):
        verb = Verb(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(LanguageMapTypeError):
            verb.set_display({"bad map"})
        self.displayVerificationHelper(verb.get_display())

    def displayVerificationHelper(self, display):
        self.assertIsInstance(display, LanguageMap)
        self.assertEqual(len(vars(display)), 1)
        self.assertIn('en-US', vars(display))
        self.assertEqual(display['en-US'], 'test')

#suite = unittest.TestLoader().loadTestsFromTestCase(TestVerb)
#unittest.TextTestRunner(verbosity=2).run(suite)
