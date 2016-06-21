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
from tincan import (
    Activity,
    ActivityDefinition,
    InteractionComponentList,
    LanguageMap,
)


class ActivityTest(unittest.TestCase):
    def test_InitEmpty(self):
        activity = Activity()
        self.assertIsNone(activity.id)

    def test_InitExceptionEmptyId(self):
        with self.assertRaises(ValueError):
            activity = Activity(id='')

    def test_Init(self):
        activity = Activity(id='test', definition=ActivityDefinition(), object_type='Activity')
        self.activityVerificationHelper(activity)

    def test_InitAnonDefinition(self):
        # these are arbitrary parameters - the ActivityDefinition is tested in ActivityDefinition_test
        activity = Activity(definition={'name': {'en-US': 'test'}, 'scale': []})
        self.assertIsInstance(activity.definition, ActivityDefinition)
        self.assertEqual(activity.definition.name, {'en-US': 'test'})
        self.assertIsInstance(activity.definition.name, LanguageMap)
        self.assertEqual(activity.definition.scale, [])
        self.assertIsInstance(activity.definition.scale, InteractionComponentList)

    def test_InitUnpack(self):
        obj = {'id': 'test', 'definition': ActivityDefinition(), 'object_type': 'Activity'}
        activity = Activity(**obj)
        self.activityVerificationHelper(activity)

    def test_InitUnpackExceptionEmptyId(self):
        obj = {'id': ''}
        with self.assertRaises(ValueError):
            activity = Activity(**obj)

    def test_FromJSON(self):
        activity = Activity.from_json('{"id": "test", "definition": {}, "object_type": "Activity"}')
        self.activityVerificationHelper(activity)

    def test_FromJSONExcpetionEmptyId(self):
        with self.assertRaises(ValueError):
            activity = Activity.from_json('{"id": ""}')

    def test_FromJSONExceptionEmptyObject(self):
        activity = Activity.from_json('{}')
        self.assertIsInstance(activity, Activity)
        self.assertIsNone(activity.id, None)

    def test_AsVersionEmpty(self):
        activity = Activity()
        activity2 = activity.as_version()
        self.assertEqual(activity2, {"objectType": "Activity"})

    def test_AsVersionNotEmpty(self):
        activity = Activity(id='test')
        activity2 = activity.as_version()
        self.assertEqual(activity2, {'id': 'test', "objectType": "Activity"})

    def test_AsVersion(self):
        activity = Activity(id='test', definition=ActivityDefinition(), object_type='Activity')
        activity2 = activity.as_version()
        self.assertEqual(activity2, {'id': 'test', 'definition': {}, 'objectType': 'Activity'})

    def test_ToJSONFromJSON(self):
        json_str = '{"id": "test", "definition": {}, "object_type": "Activity"}'
        check_str = '{"definition": {}, "id": "test", "objectType": "Activity"}'
        activity = Activity.from_json(json_str)
        self.activityVerificationHelper(activity)
        self.assertEqual(json.loads(activity.to_json()), json.loads(check_str))

    def test_ToJSON(self):
        check_str = '{"definition": {}, "id": "test", "objectType": "Activity"}'
        activity = Activity(**{'id': 'test', 'definition': {}, 'object_type': 'Activity'})
        self.assertEqual(json.loads(activity.to_json()), json.loads(check_str))

    def test_setDefinitionException(self):
        activity = Activity()
        with self.assertRaises(AttributeError):
            activity.definition = {"invalid": "definition"}

    def test_setDefinition(self):
        activity = Activity()
        activity.definition = ActivityDefinition()
        self.assertIsInstance(activity.definition, ActivityDefinition)

    def test_setObjectType(self):
        activity = Activity()
        activity.object_type = 'Activity'
        self.assertEqual(activity.object_type, 'Activity')

    def test_setIdException(self):
        activity = Activity()
        with self.assertRaises(ValueError):
            activity.id = ''

    def test_setId(self):
        activity = Activity()
        activity.id = 'test'
        self.assertEqual(activity.id, 'test')

    def activityVerificationHelper(self, activity):
        self.assertEqual(activity.id, 'test')
        self.assertIsInstance(activity.definition, ActivityDefinition)
        self.assertEqual(activity.object_type, 'Activity')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ActivityTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
