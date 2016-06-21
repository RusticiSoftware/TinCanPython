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
    Agent,
    Group,
    Verb,
    StatementRef,
    Activity,
    SubStatement,
)


class SubStatementTest(unittest.TestCase):
    def test_InitAnonAgentActor(self):
        substatement = SubStatement(actor={'object_type': 'Agent', 'name': 'test'})
        self.agentVerificationHelper(substatement.actor)

    def test_InitAnonGroupActor(self):
        substatement = SubStatement(actor={'object_type': 'Group', 'member': [{"name": "test"}]})
        self.groupVerificationHelper(substatement.actor)

    def test_InitAnonVerb(self):
        substatement = SubStatement(verb={'id': 'test'})
        self.verbVerificationHelper(substatement.verb)

    def test_InitAnonObject(self):
        substatement = SubStatement(object={'id': 'test'})
        self.activityVerificationHelper(substatement.object)

    def test_InitAnonAgentObject(self):
        substatement = SubStatement(object={'object_type': 'Agent', 'name': 'test'})
        self.agentVerificationHelper(substatement.object)

    def test_InitDifferentNamingObject(self):
        substatement = SubStatement(object={'objectType': 'Agent', 'name': 'test'})
        self.agentVerificationHelper(substatement.object)

    def test_InitObjectType(self):
        substatement = SubStatement(object_type="SubStatement")
        self.assertEqual(substatement.object_type, "SubStatement")

    def test_InitAgentActor(self):
        substatement = SubStatement(actor=Agent(name='test'))
        self.agentVerificationHelper(substatement.actor)

    def test_InitGroupActor(self):
        substatement = SubStatement(actor=Group(member=[Agent(name='test')]))
        self.groupVerificationHelper(substatement.actor)

    def test_InitVerb(self):
        substatement = SubStatement(verb=Verb(id='test'))
        self.verbVerificationHelper(substatement.verb)

    def test_InitAgentObject(self):
        substatement = SubStatement(object=Agent(name='test'))
        self.agentVerificationHelper(substatement.object)

    def test_InitGroupObject(self):
        substatement = SubStatement(object=Group(member=[Agent(name='test')]))
        self.groupVerificationHelper(substatement.object)

    def test_InitActivityObject(self):
        substatement = SubStatement(object=Activity(id='test'))
        self.activityVerificationHelper(substatement.object)

    def test_InitUnpack(self):
        obj = {'object_type': 'SubStatement', 'actor': {'name': 'test'}, 'verb': {'id': 'test'},
               'object': {'id': 'test'}}
        substatement = SubStatement(**obj)
        self.assertEqual(substatement.object_type, 'SubStatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)

    def test_FromJSON(self):
        json_str = '{"object_type":"SubStatement", "actor":{"name":"test"}, ' \
                   '"verb":{"id":"test"}, "object":{"id":"test"}}'
        substatement = SubStatement.from_json(json_str)
        self.assertEqual(substatement.object_type, 'SubStatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)

    def test_ToJSONEmpty(self):
        substatement = SubStatement()
        self.assertEqual(json.loads(substatement.to_json()), json.loads('{"objectType": "SubStatement"}'))

    def test_ToJSON(self):
        substatement = SubStatement(object_type='SubStatement', actor=Agent(name='test'), verb=Verb(id='test'),
                                    object=Activity(id='test'))
        self.assertEqual(json.loads(substatement.to_json()),
                         json.loads('{"verb": {"id": "test"}, "object": {"id": "test", "objectType": "Activity"}, '
                                    '"actor": {"name": "test", "objectType": "Agent"}, "objectType": "SubStatement"}'))

    def test_FromJSONToJSON(self):
        json_str = '{"object_type":"SubStatement", "actor":{"name":"test"}, "verb":{"id":"test"}, "' \
                   'object":{"id":"test", "objectType": "Activity"}}'
        substatement = SubStatement.from_json(json_str)
        self.assertEqual(substatement.object_type, 'SubStatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)
        self.assertEqual(json.loads(substatement.to_json()),
                         json.loads('{"verb": {"id": "test"}, "object": {"id": "test", "objectType": "Activity"}, '
                                    '"actor": {"name": "test", "objectType": "Agent"}, "objectType": "SubStatement"}'))

    def agentVerificationHelper(self, value):
        self.assertIsInstance(value, Agent)
        self.assertEqual(value.name, 'test')

    def groupVerificationHelper(self, value):
        self.assertIsInstance(value, Group)
        for k in value.member:
            self.assertIsInstance(k, Agent)
            self.assertEqual(k.name, 'test')

    def verbVerificationHelper(self, value):
        self.assertIsInstance(value, Verb)
        self.assertEqual(value.id, 'test')

    def statementrefVerificationHelper(self, value):
        self.assertIsInstance(value, StatementRef)
        self.assertEqual(value.object_type, 'StatementRef')

    def activityVerificationHelper(self, value):
        self.assertIsInstance(value, Activity)
        self.assertEqual(value.id, 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SubStatementTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
