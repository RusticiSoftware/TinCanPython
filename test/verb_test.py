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
from tincan import Verb, LanguageMap


class VerbTest(unittest.TestCase):
    def test_InitEmpty(self):
        verb = Verb()
        self.assertIsNone(verb.id)

    def test_InitExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            Verb(id='')

    def test_InitId(self):
        verb = Verb(id='test')
        self.assertEqual(verb.id, 'test')

    def test_InitDisplay(self):
        verb = Verb(display={"en-US": "test"})
        self.assertIsNone(verb.id)
        self.displayVerificationHelper(verb.display)

    def test_InitAnonDisplay(self):
        verb = Verb(id='test', display={"en-US": "test"})
        self.assertEqual(verb.id, 'test')
        self.displayVerificationHelper(verb.display)

    def test_InitLanguageMapDisplay(self):
        verb = Verb(id='test', display=LanguageMap({"en-US": "test"}))
        self.assertEqual(verb.id, 'test')
        self.displayVerificationHelper(verb.display)

    def test_InitUnpackDisplay(self):
        obj = {"display": {"en-US": "test"}}
        verb = Verb(**obj)
        self.displayVerificationHelper(verb.display)

    def test_InitUnpack(self):
        obj = {"id": "test", "display": {"en-US": "test"}}
        verb = Verb(**obj)
        self.assertEqual(verb.id, 'test')
        self.displayVerificationHelper(verb.display)

    def test_InitExceptionUnpackEmptyId(self):
        obj = {"id": ""}
        with self.assertRaises(ValueError):
            Verb(**obj)

    def test_InitExceptionUnpackFlatDisplay(self):
        obj = {"id": "test", "display": "test"}
        with self.assertRaises(ValueError):
            Verb(**obj)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            Verb.from_json('{"bad JSON"}')

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            Verb.from_json('{"test": "invalid property"}')

    """ An exception is best here to keep client code from thinking its doing \
    something its not when instantiating a Verb """

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            Verb.from_json('{"test": "invalid property", "id": \
            "valid property"}')

    def test_FromJSONEmptyObject(self):
        verb = Verb.from_json('{}')
        self.assertIsNone(verb.id)

    def test_FromJSONExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            Verb.from_json('{"id":"''"}')

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            Verb.from_json('')

    def test_FromJSONId(self):
        verb = Verb.from_json('{"id": "test"}')
        self.assertEqual(verb.id, 'test')

    def test_FromJSONExceptionFlatDisplay(self):
        with self.assertRaises(ValueError):
            Verb.from_json('{"id": "test", "display": "flatdisplay"}')

    def test_FromJSON(self):
        verb = Verb.from_json('{"id": "test", "display": {"en-US": "test"}}')
        self.assertEqual(verb.id, 'test')
        self.displayVerificationHelper(verb.display)

    def test_AsVersionEmpty(self):
        verb = Verb()
        verb2 = verb.as_version()
        self.assertEqual(verb2, {})

    def test_AsVersionNotEmpty(self):
        verb = Verb(id='test')
        verb2 = verb.as_version()
        self.assertEqual(verb2, {'id': 'test'})

    def test_AsVersion(self):
        verb = Verb(id='test', display={'en-US': 'test'})
        verb2 = verb.as_version()
        self.assertEqual(verb2, {'id': 'test', 'display': {'en-US': 'test'}})

    def test_AsVersionIgnoreNone(self):
        verb = Verb(display={'en-US': 'test'})
        verb2 = verb.as_version()
        self.assertEqual(verb2, {'display': {'en-US': 'test'}})

    def test_ToJSONFromJSON(self):
        json_str = '{"id": "test", "display": {"en-US": "test"}}'
        verb = Verb.from_json(json_str)
        self.assertEqual(verb.id, 'test')
        self.displayVerificationHelper(verb.display)
        self.assertEqual(json.loads(verb.to_json()), json.loads(json_str))

    def test_ToJSON(self):
        verb = Verb(**{"id": "test", "display": {"en-US": "test"}})
        self.assertEqual(json.loads(verb.to_json()), json.loads('{"id": "test", "display": {"en-US": "test"}}'))

    def test_ToJSONIgnoreNoneId(self):
        verb = Verb(display={"en-US": "test"})
        self.assertEqual(json.loads(verb.to_json()), json.loads('{"display": {"en-US": "test"}}'))

    def test_ToJSONEmpty(self):
        verb = Verb()
        self.assertEqual(verb.to_json(), '{}')

    def test_setId(self):
        verb = Verb(id='test')
        verb.id = 'newId'
        self.assertEqual(verb.id, 'newId')

    def test_setIdExceptionEmptyString(self):
        verb = Verb(id='test')
        with self.assertRaises(ValueError):
            verb.id = ''
        self.assertEqual(verb.id, 'test')

    def test_setDisplay(self):
        verb = Verb(display=LanguageMap({"fr-CA": "not test"}))
        verb.display = {"en-US": "test"}
        self.assertIsNone(verb.id)
        self.displayVerificationHelper(verb.display)

    def test_setDisplayExceptionNestedObject(self):
        verb = Verb(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(TypeError):
            verb.display = {"fr-CA": {"nested": "object"}}
        self.displayVerificationHelper(verb.display)

    def test_setDisplayExceptionBadMap(self):
        verb = Verb(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(ValueError):
            verb.display = {"bad map"}
        self.displayVerificationHelper(verb.display)

    def displayVerificationHelper(self, display):
        self.assertIsInstance(display, LanguageMap)
        self.assertEqual(len(display), 1)
        self.assertIn('en-US', display)
        self.assertEqual(display['en-US'], 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(VerbTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
