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

if __name__ == '__main__':
    from main import setup_tincan_path
    setup_tincan_path()
from tincan.activity_definition import ActivityDefinition
from tincan.language_map import LanguageMap
from tincan.interaction_component_list import InteractionComponentList
from tincan.interaction_component import InteractionComponent


class ActivityDefinitionTest(unittest.TestCase):

    def test_InitEmpty(self):
        adef = ActivityDefinition()
        self.assertEqual(vars(adef), {})
        self.assertIsInstance(adef, ActivityDefinition)

    def test_InitAll(self):
        adef = ActivityDefinition({
            'name': {'en-US': 'test'},
            'description': {'en-US': 'test'},
            'type': 'test',
            'more_info': 'test',
            'interaction_type': 'choice',
            'correct_responses_pattern': ['test'],
            'choices': InteractionComponentList(),
            'scale': InteractionComponentList(),
            'source': InteractionComponentList(),
            'target':InteractionComponentList(),
            'steps': InteractionComponentList(),
            'extensions': {'test': 'test'}
        })
        self.definitionVerificationHelper(adef)

    def test_InitExceptionType(self):
        with self.assertRaises(ValueError):
            adef = ActivityDefinition(type='')

    def test_InitExceptionMoreInfo(self):
        with self.assertRaises(ValueError):
            adef = ActivityDefinition(more_info='')

    def test_InitExceptionInteractionType(self):
        with self.assertRaises(ValueError):
            adef = ActivityDefinition(interaction_type='notvalidinteraction')

    def test_InitExceptionCorrectResponsesPattern(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(correct_responses_pattern='notlist')

    def test_InitExceptionChoices(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(choices='notlist')

    def test_InitExceptionChoicesNotComponentList(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(choices=['not component'])

    def test_InitExceptionScale(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(scale='notlist')

    def test_InitExceptionScaleNotComponentList(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(scale=['not component'])

    def test_InitExceptionSource(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(source='notlist')

    def test_InitExceptionSourceNotComponentList(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(source=['not component'])

    def test_InitExceptionTarget(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(target='notlist')

    def test_InitExceptionTargetNotComponentList(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(target=['not component'])

    def test_InitExceptionSteps(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(steps='notlist')

    def test_InitExceptionStepsNotComponentList(self):
        with self.assertRaises(TypeError):
            adef = ActivityDefinition(steps=['not component'])

    def test_InitUnpack(self):
        obj = {
            'name': {'en-US': 'test'},
            'description': {'en-US': 'test'},
            'type': 'test',
            'more_info': 'test',
            'interaction_type': 'choice',
            'correct_responses_pattern': ['test'],
            'choices': InteractionComponentList(),
            'scale': InteractionComponentList(),
            'source': InteractionComponentList(),
            'target':InteractionComponentList(),
            'steps': InteractionComponentList(),
            'extensions': {'test': 'test'}
        }
        adef = ActivityDefinition(**obj)
        self.definitionVerificationHelper(adef)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            adef = ActivityDefinition.from_json('{"bad JSON"}')

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            adef = ActivityDefinition.from_json('{"test": "invalid property"}')

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            adef = ActivityDefinition.from_json('{"test": "invalid property", "id": \
            "valid property"}')

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            adef = ActivityDefinition.from_json('')

    def test_FromJSON(self):
        json_str = '{"name":{"en-US":"test"},\
            "description":{"en-US":"test"},\
            "type":"test",\
            "more_info":"test",\
            "interaction_type":"choice",\
            "correct_responses_pattern": ["test"],\
            "choices": [], "scale": [], "source": [], "target": [], "steps": [],\
            "extensions": {"test": "test"}}'
        adef = ActivityDefinition.from_json(json_str)
        self.definitionVerificationHelper(adef)

    def test_AsVersionEmpty(self):
        adef = ActivityDefinition()
        adef2 = adef.as_version()
        self.assertEqual(adef2, {})

    def test_AsVersion(self):
        adef = ActivityDefinition({
            'description': {'en-US': 'test'},
            'name': {'en-US': 'test'},
            'type': 'test',
            'more_info': 'test',
            'interaction_type': 'choice',
            'correct_responses_pattern': ['test'],
            'choices': InteractionComponentList(),
            'scale': InteractionComponentList(),
            'source': InteractionComponentList(),
            'target': InteractionComponentList(),
            'steps': InteractionComponentList(),
            'extensions': {'test': 'test'}
        })
        adef2 = adef.as_version()
        self.assertEqual(adef2, {
            "name": {"en-US": "test"},
            "correctResponsesPattern": ["test"],
            "scale": [],
            "description": {"en-US": "test"},
            "choices": [],
            "source": [],
            "steps": [],
            "moreInfo": "test",
            "extensions": {"test": "test"},
            "interactionType": "choice",
            "target": [],
            "type": "test",
        })

    def test_AsVersionIgnoreNone(self):
        adef = ActivityDefinition({
            'description': {'en-US': 'test'},
            'more_info': None
        })
        self.assertEqual(adef.description, {'en-US': 'test'})
        self.assertIsNone(adef.more_info)
        adef2 = adef.as_version()
        self.assertEqual(adef2, {'description': {'en-US': 'test'}})

    def test_ToJSONFromJSON(self):
        json_str = '{"correct_responses_pattern": ["test"], "scale": [], "description": {"en-US": "test"}, "choices": [], "source": [], "steps": [], "more_info": "test", "target": [], "extensions": {"test": "test"}, "interaction_type": "choice", "type": "test", "name": {"en-US": "test"}}'
        check_str = '{"correctResponsesPattern": ["test"], "target": [], "name": {"en-US": "test"}, "interactionType": "choice", "choices": [], "source": [], "scale": [], "steps": [], "extensions": {"test": "test"}, "moreInfo": "test", "type": "test", "description": {"en-US": "test"}}'
        adef = ActivityDefinition.from_json(json_str)
        self.definitionVerificationHelper(adef)
        self.assertEqual(adef.to_json(), check_str)

    def test_ToJSONIgnoreNone(self):
        adef = ActivityDefinition({
            'description': {'en-US': 'test'},
            'more_info': None
        })
        self.assertEqual(adef.to_json(), '{"description": {"en-US": "test"}}')

    def test_ToJSONEmpty(self):
        adef = ActivityDefinition()
        self.assertEqual(adef.to_json(), '{}')

    def definitionVerificationHelper(self, definition):
        check_map = LanguageMap({'en-US': 'test'})
        check_string = 'test'
        self.assertIsInstance(definition.name, LanguageMap)
        self.assertEqual(definition.name, check_map)
        self.assertIsInstance(definition.description, LanguageMap)
        self.assertEqual(definition.description, check_map)
        self.assertEqual(definition.type, check_string)
        self.assertEqual(definition.more_info, check_string)
        self.assertEqual(definition.interaction_type, 'choice')
        self.assertIn(definition.interaction_type, ActivityDefinition._interaction_types)
        self.assertEqual(definition.correct_responses_pattern, ['test'])
        self.assertEqual(definition.choices, [])
        self.assertIsInstance(definition.choices, InteractionComponentList)
        self.assertEqual(definition.scale, [])
        self.assertIsInstance(definition.scale, InteractionComponentList)
        self.assertEqual(definition.source, [])
        self.assertIsInstance(definition.source, InteractionComponentList)
        self.assertEqual(definition.target, [])
        self.assertIsInstance(definition.target, InteractionComponentList)
        self.assertEqual(definition.steps, [])
        self.assertIsInstance(definition.steps, InteractionComponentList)
        self.assertEqual(definition.extensions, {"test": "test"})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ActivityDefinitionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)