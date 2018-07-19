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
from datetime import timedelta, datetime
import uuid

import pytz


if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import (
    Statement,
    Agent,
    Group,
    Verb,
    Result,
    Context,
    Attachment,
    SubStatement,
    Activity,
    StatementRef,
)


class StatementTest(unittest.TestCase):
    def test_InitEmpty(self):
        statement = Statement()
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitVersion(self):
        statement = Statement(version='test')
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertEqual(statement.version, 'test')

    def test_InitId(self):
        statement = Statement(id='016699c6-d600-48a7-96ab-86187498f16f')
        self.assertEqual(statement.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitTimestamp(self):
        statement = Statement(timestamp="2014-06-23T15:25:00-05:00")
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)

        central = pytz.timezone("US/Central")  # UTC -0500
        dt = central.localize(datetime(2014, 6, 23, 15, 25))
        self.assertEqual(statement.timestamp, dt)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitStored(self):
        statement = Statement(stored="2014-06-23T15:25:00-05:00")
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)

        central = pytz.timezone("US/Central")  # UTC -0500
        dt = central.localize(datetime(2014, 6, 23, 15, 25))
        self.assertEqual(statement.stored, dt)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.authority)

    def test_InitEmptyActor(self):
        statement = Statement(actor={})
        self.assertIsNone(statement.id)
        self.assertIsInstance(statement.actor, Agent)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitEmptyVerb(self):
        statement = Statement(verb={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsInstance(statement.verb, Verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitEmptyObject(self):
        statement = Statement(object={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsInstance(statement.object, Activity)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitEmptyAuthority(self):
        statement = Statement(authority={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsInstance(statement.authority, Agent)

    def test_InitEmptyResult(self):
        statement = Statement(result={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertIsInstance(statement.result, Result)

    def test_InitEmptyContext(self):
        statement = Statement(context={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertIsInstance(statement.context, Context)

    def test_InitEmptyAttachments(self):
        statement = Statement(attachments=[])
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertEqual(statement.attachments, [])

    def test_InitAnonAgentActor(self):
        statement = Statement(actor={'name': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.actor)

    def test_InitAnonGroupActor(self):
        statement = Statement(actor={'member': [Agent(name='test')], 'object_type': 'Group'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.groupVerificationHelper(statement.actor)

    def test_InitAnonVerb(self):
        statement = Statement(verb={'id': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.verbVerificationHelper(statement.verb)

    def test_InitAnonObject(self):
        statement = Statement(object={'id': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.activityVerificationHelper(statement.object)

    def test_InitAnonAgentObject(self):
        statement = Statement(object={'object_type': 'Agent', 'name': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.object)

    def test_InitDifferentNamingObject(self):
        statement = Statement(object={'objectType': 'Agent', 'name': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.object)

    def test_InitAnonAuthority(self):
        statement = Statement(authority={'name': 'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.actor)
        self.agentVerificationHelper(statement.authority)

    def test_InitAnonResult(self):
        statement = Statement(result={'duration': timedelta(days=7)})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.result)

    def test_InitAnonContext(self):
        statement = Statement(context={'registration': '016699c6-d600-48a7-96ab-86187498f16f'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.contextVerificationHelper(statement.context)

    def test_InitAnonAttachments(self):
        statement = Statement(attachments=[{'usage_type': 'test'}])
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_InitAgentActor(self):
        statement = Statement(actor=Agent(name='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.actor)

    def test_InitGroupActor(self):
        statement = Statement(actor=Group(member=[Agent(name='test')]))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.groupVerificationHelper(statement.actor)

    def test_InitVerb(self):
        statement = Statement(verb=Verb(id='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.verbVerificationHelper(statement.verb)

    def test_InitAgentObject(self):
        statement = Statement(object=Agent(name='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.object)

    def test_InitSubStatementObject(self):
        statement = Statement(object=SubStatement(object_type='SubStatement'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.substatementVerificationHelper(statement.object)

    def test_InitStatementRefObject(self):
        statement = Statement(object=StatementRef(object_type='StatementRef'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.statementrefVerificationHelper(statement.object)

    def test_InitActivityObject(self):
        statement = Statement(object=Activity(id='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.activityVerificationHelper(statement.object)

    def test_InitAuthority(self):
        statement = Statement(authority=Agent(name='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.actor)
        self.agentVerificationHelper(statement.authority)

    def test_InitResult(self):
        statement = Statement(result=Result(duration=timedelta(days=7)))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.result)

    def test_InitContext(self):
        statement = Statement(context=Context(registration='016699c6-d600-48a7-96ab-86187498f16f'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.contextVerificationHelper(statement.context)

    def test_InitAttachments(self):
        statement = Statement(attachments=[Attachment(usage_type='test')])
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_InitUnpack(self):
        obj = {'id': '016699c6-d600-48a7-96ab-86187498f16f', 'actor': {'name': 'test'}, 'verb': {'id': 'test'},
               'object': {'object_type': 'Agent', 'name': 'test'}, 'authority': {'name': 'test'},
               'context': {'registration': '016699c6-d600-48a7-96ab-86187498f16f'},
               'attachments': [{'usage_type': 'test'}]}
        statement = Statement(**obj)
        self.assertEqual(statement.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_FromJSON(self):
        json_str = '{"id":"016699c6-d600-48a7-96ab-86187498f16f", "actor":{"name":"test"}, ' \
                   '"verb":{"id":"test"}, "object":{"object_type":"Agent", "name":"test"}, ' \
                   '"authority":{"name":"test"}, "context":{"registration":"016699c6-d600-48a7-96ab-86187498f16f"}, ' \
                   '"attachments":[{"usage_type":"test"}]}'
        statement = Statement.from_json(json_str)
        self.assertEqual(statement.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_ToJSON(self):
        statement = Statement(
            **{'id': '016699c6-d600-48a7-96ab-86187498f16f', 'actor': {'name': 'test'}, 'verb': {'id': 'test'},
               'object': {'object_type': 'Agent', 'name': 'test'}, 'authority': {'name': 'test'},
               'context': {'registration': '016699c6-d600-48a7-96ab-86187498f16f'},
               'attachments': [{'usage_type': 'test'}]})
        self.assertEqual(json.loads(statement.to_json()),
                         json.loads('{"verb": {"id": "test"}, '
                         '"attachments": [{"usageType": "test"}], '
                         '"object": {"name": "test", "objectType": "Agent"}, '
                         '"actor": {"name": "test", "objectType": "Agent"}, '
                         '"version": "1.0.1", '
                         '"authority": {"name": "test", "objectType": "Agent"}, '
                         '"context": {"registration": "016699c6-d600-48a7-96ab-86187498f16f"}, '
                                    '"id": "016699c6-d600-48a7-96ab-86187498f16f"}'))

    def test_ToJSONEmpty(self):
        statement = Statement()
        self.assertEqual(json.loads(statement.to_json()), json.loads('{"version": "1.0.1"}'))

    def test_FromJSONToJSON(self):
        json_str = '{"id":"016699c6-d600-48a7-96ab-86187498f16f", ' \
                   '"actor": {"name":"test"}, ' \
                   '"verb": {"id":"test"}, ' \
                   '"object": {"object_type":"Agent", "name":"test"}, ' \
                   '"authority":{ "name":"test"}, ' \
                   '"context": {"registration":"016699c6-d600-48a7-96ab-86187498f16f"}, ' \
                   '"attachments":[{"usage_type":"test"}]}'
        statement = Statement.from_json(json_str)
        self.assertEqual(statement.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)
        self.assertEqual(json.loads(statement.to_json()),
                         json.loads('{"verb": {"id": "test"}, '
                         '"attachments": [{"usageType": "test"}], '
                         '"object": {"name": "test", "objectType": "Agent"}, '
                         '"actor": {"name": "test", "objectType": "Agent"}, '
                         '"version": "1.0.1", '
                         '"authority": {"name": "test", "objectType": "Agent"}, '
                         '"context": {"registration": "016699c6-d600-48a7-96ab-86187498f16f"}, '
                                    '"id": "016699c6-d600-48a7-96ab-86187498f16f"}'))

    def test_ExceptionInvalidUUID(self):
        with self.assertRaises(ValueError):
            Statement(id='badtest')

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

    def resultVerificationHelper(self, value):
        self.assertIsInstance(value, Result)
        self.assertEqual(value.duration, timedelta(days=7))

    def contextVerificationHelper(self, value):
        self.assertIsInstance(value, Context)
        self.assertEqual(value.registration, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))

    def attachmentVerificationHelper(self, value):
        self.assertIsInstance(value, Attachment)
        self.assertEqual(value.usage_type, 'test')

    def substatementVerificationHelper(self, value):
        self.assertIsInstance(value, SubStatement)
        self.assertEqual(value.object_type, 'SubStatement')

    def statementrefVerificationHelper(self, value):
        self.assertIsInstance(value, StatementRef)
        self.assertEqual(value.object_type, 'StatementRef')

    def activityVerificationHelper(self, value):
        self.assertIsInstance(value, Activity)
        self.assertEqual(value.id, 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
