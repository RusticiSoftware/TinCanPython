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
from tincan import InteractionComponent, LanguageMap


class InteractionComponentTest(unittest.TestCase):
    def test_InitEmpty(self):
        icomp = InteractionComponent()
        self.assertIsNone(icomp.id)
        self.assertNotIn('description', vars(icomp))

    def test_InitExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            InteractionComponent(id='')

    def test_InitId(self):
        icomp = InteractionComponent(id='test')
        self.assertEqual(icomp.id, 'test')
        self.assertNotIn('description', vars(icomp))

    def test_InitDescription(self):
        icomp = InteractionComponent(description={"en-US": "test"})
        self.assertIsNone(icomp.id)
        self.descriptionVerificationHelper(icomp.description)

    def test_InitEmptyDescription(self):
        icomp = InteractionComponent(id='test', description={})
        self.assertEqual(icomp.id, 'test')
        self.assertIsInstance(icomp.description, LanguageMap)
        self.assertEqual(len(vars(icomp.description)), 0)

    def test_InitAnonDescription(self):
        icomp = InteractionComponent(id='test', description={"en-US": "test"})
        self.assertEqual(icomp.id, 'test')
        self.descriptionVerificationHelper(icomp.description)

    def test_InitLanguageMapDescription(self):
        icomp = InteractionComponent(id='test', description=LanguageMap({"en-US": "test"}))
        self.assertEqual(icomp.id, 'test')
        self.descriptionVerificationHelper(icomp.description)

    def test_InitEmptyLanguageMapDescription(self):
        icomp = InteractionComponent(id='test', description=LanguageMap({}))
        self.assertEqual(icomp.id, 'test')
        self.assertIsInstance(icomp.description, LanguageMap)
        self.assertEqual(len(vars(icomp.description)), 0)

    def test_InitUnpackDescription(self):
        obj = {"description": {"en-US": "test"}}
        icomp = InteractionComponent(**obj)
        self.descriptionVerificationHelper(icomp.description)

    def test_InitUnpack(self):
        obj = {"id": "test", "description": {"en-US": "test"}}
        icomp = InteractionComponent(**obj)
        self.assertEqual(icomp.id, 'test')
        self.descriptionVerificationHelper(icomp.description)

    def test_InitExceptionUnpackEmptyId(self):
        obj = {"id": ""}
        with self.assertRaises(ValueError):
            InteractionComponent(**obj)

    def test_InitExceptionUnpackFlatDescription(self):
        obj = {"id": "test", "description": "test"}
        with self.assertRaises(ValueError):
            InteractionComponent(**obj)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            InteractionComponent.from_json('{"bad JSON"}')

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            InteractionComponent.from_json('{"test": "invalid property"}')

    """ An exception is best here to keep client code from thinking its doing \
    something its not when instantiating a InteractionComponent """

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            InteractionComponent.from_json('{"test": "invalid property", "id": \
            "valid property"}')

    def test_FromJSONEmptyObject(self):
        icomp = InteractionComponent.from_json('{}')
        self.assertIsNone(icomp.id)
        self.assertNotIn('description', vars(icomp))

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            InteractionComponent.from_json('')

    def test_FromJSONId(self):
        icomp = InteractionComponent.from_json('{"id": "test"}')
        self.assertEqual(icomp.id, 'test')
        self.assertNotIn('description', vars(icomp))

    def test_FromJSONExceptionFlatDescription(self):
        with self.assertRaises(ValueError):
            InteractionComponent.from_json('{"id": "test", "description": "flatdescription"}')

    def test_FromJSON(self):
        icomp = InteractionComponent.from_json('{"id": "test", "description": {"en-US": "test"}}')
        self.assertEqual(icomp.id, 'test')
        self.descriptionVerificationHelper(icomp.description)

    def test_AsVersionEmpty(self):
        icomp = InteractionComponent()
        icomp2 = icomp.as_version("1.0.0")
        self.assertEqual(icomp2, {})

    def test_AsVersionNotEmpty(self):
        icomp = InteractionComponent(**{'id': 'test'})
        icomp2 = icomp.as_version()
        self.assertEqual(icomp2, {'id': 'test'})

    def test_ToJSONFromJSON(self):
        json_str = '{"id": "test", "description": {"en-US": "test"}}'
        icomp = InteractionComponent.from_json(json_str)
        self.assertEqual(icomp.id, 'test')
        self.descriptionVerificationHelper(icomp.description)
        self.assertEqual(json.loads(icomp.to_json()), json.loads(json_str))

    def test_ToJSON(self):
        icomp = InteractionComponent(**{"id": "test", "description": {"en-US": "test"}})
        self.assertEqual(json.loads(icomp.to_json()), json.loads('{"id": "test", "description": {"en-US": "test"}}'))

    def test_ToJSONIgnoreNoneDescription(self):
        icomp = InteractionComponent(id='test')
        self.assertEqual(icomp.to_json(), '{"id": "test"}')

    def test_ToJSONIgnoreNoneId(self):
        icomp = InteractionComponent(description={"en-US": "test"})
        self.assertEqual(icomp.to_json(), '{"description": {"en-US": "test"}}')

    def test_ToJSONEmpty(self):
        icomp = InteractionComponent()
        self.assertEqual(icomp.to_json(), '{}')

    def descriptionVerificationHelper(self, description):
        self.assertIsInstance(description, LanguageMap)
        self.assertEqual(len(description), 1)
        self.assertIn('en-US', description)
        self.assertEqual(description['en-US'], 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InteractionComponentTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
