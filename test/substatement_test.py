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
from tincan.agent import Agent
from tincan.group import Group
from tincan.verb import Verb
from tincan.statement_ref import StatementRef
from tincan.activity import Activity
from tincan.substatement import Substatement

class TestSubstatement(unittest.TestCase):

    def test_InitAnonAgentActor(self):
        substatement = Substatement(actor={'name':'test'})
        self.agentVerificationHelper(substatement.actor)

    def test_InitAnonGroupActor(self):
        substatement = Substatement(actor=[Agent(name='test')])
        self.groupVerificationHelper(substatement.actor)

    def test_InitAnonVerb(self):
        substatement = Substatement(verb={'id':'test'})
        self.verbVerificationHelper(substatement.verb)

    def test_InitAnonObject(self):
        substatement = Substatement(object={'id':'test'})
        self.activityVerificationHelper(substatement.object)

    def test_InitAnonAgentObject(self):
        substatement = Substatement(object={'object_type':'Agent', 'name':'test'})
        self.agentVerificationHelper(substatement.object)

    def test_InitDifferentNamingObject(self):
        substatement = Substatement(object={'objectType':'Agent', 'name':'test'})
        self.agentVerificationHelper(substatement.object)

    def test_InitObjectType(self):
        substatement = Substatement(object_type="Substatement")
        self.assertEqual(substatement.object_type, "Substatement")

    def test_InitAgentActor(self):
        substatement = Substatement(actor=Agent(name='test'))
        self.agentVerificationHelper(substatement.actor)

    def test_InitGroupActor(self):
        substatement = Substatement(actor=Group(member=[Agent(name='test')]))
        self.groupVerificationHelper(substatement.actor)

    def test_InitVerb(self):
        substatement = Substatement(verb=Verb(id='test'))
        self.verbVerificationHelper(substatement.verb)

    def test_InitAgentObject(self):
        substatement = Substatement(object=Agent(name='test'))
        self.agentVerificationHelper(substatement.object)

    def test_InitGroupObject(self):
        substatement = Substatement(object=Group(member=[Agent(name='test')]))
        self.groupVerificationHelper(substatement.object)

    def test_InitActivityObject(self):
        substatement = Substatement(object=Activity(id='test'))
        self.activityVerificationHelper(substatement.object)

    def test_InitUnpack(self):
        obj = {'object_type':'Substatement', 'actor':{'name':'test'}, 'verb':{'id':'test'}, 'object':{'id':'test'}}
        substatement = Substatement(**obj)
        self.assertEqual(substatement.object_type, 'Substatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)

    def test_FromJSON(self):
        json_str = '{"object_type":"Substatement", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"id":"test"}}'
        substatement = Substatement.from_json(json_str)
        self.assertEqual(substatement.object_type, 'Substatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)

    def test_ToJSONEmpty(self):
        substatement = Substatement()
        self.assertEqual(substatement.to_json(), '{}')

    def test_ToJSON(self):
        substatement = Substatement(object_type='Substatement', actor=Agent(name='test'), verb=Verb(id='test'), object=Activity(id='test'))
        self.assertEqual(substatement.to_json(), '{"verb": {"id": "test"}, "object": {"id": "test"}, "actor": {"name": "test", "objectType": "Agent"}, "objectType": "Substatement"}')

    def test_FromJSONToJSON(self):
        json_str = '{"object_type":"Substatement", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"id":"test"}}'
        substatement = Substatement.from_json(json_str)
        self.assertEqual(substatement.object_type, 'Substatement')
        self.agentVerificationHelper(substatement.actor)
        self.verbVerificationHelper(substatement.verb)
        self.activityVerificationHelper(substatement.object)
        self.assertEqual(substatement.to_json(), '{"verb": {"id": "test"}, "object": {"id": "test"}, "actor": {"name": "test", "objectType": "Agent"}, "objectType": "Substatement"}')

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