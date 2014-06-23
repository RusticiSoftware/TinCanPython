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
from tincan.statement import Statement
from tincan.agent import Agent
from tincan.group import Group
from tincan.verb import Verb
from tincan.result import Result
from tincan.context import Context
from tincan.attachment import Attachment
from tincan.substatement import Substatement

class TestStatement(unittest.TestCase):

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
        self.assertEquals(statement.version, 'test')

    def test_InitId(self):
        statement = Statement(id='016699c6-d600-48a7-96ab-86187498f16f')
        self.assertEquals(statement.id, '016699c6-d600-48a7-96ab-86187498f16f')
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitTimestamp(self):
        statement = Statement(timestamp='test o clock')
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertEqual(statement.timestamp, 'test o clock')
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitStored(self):
        statement = Statement(stored='test o clock')
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertEqual(statement.stored, 'test o clock')
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.authority)

    def test_InitEmptyActor(self):
        statement = Statement(actor={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitEmptyVerb(self):
        statement = Statement(verb={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)

    def test_InitEmptyObject(self):
        statement = Statement(object={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
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
        self.assertIsNone(statement.authority)

    def test_InitEmptyResult(self):
        statement = Statement(result={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertIsNone(statement.result)

    def test_InitEmptyContext(self):
        statement = Statement(context={})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.assertIsNone(statement.context)

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
        statement = Statement(actor={'name':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.agentVerificationHelper(statement.actor)

    def test_InitAnonGroupActor(self):
        statement = Statement(actor=[Agent(name='test')])
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.groupVerificationHelper(statement.actor)

    def test_InitAnonVerb(self):
        statement = Statement(verb={'id':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.verbVerificationHelper(statement.verb)

    def test_InitAnonObject(self):
        statement = Statement(object={'id':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.statementVerificationHelper(statement.object)

    def test_InitAnonAuthority(self):
        statement = Statement(authority={'name':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.actor)
        self.agentVerificationHelper(statement.authority)

    def test_InitAnonResult(self):
        statement = Statement(result={'duration':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.result)

    def test_InitAnonContext(self):
        statement = Statement(context={'registration':'test'})
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.context)

    def test_InitAnonAttachments(self):
        statement = Statement(attachments=[{'usage_type':'test'}])
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
        statement = Statement(actor=Group(members=[Agent(name='test')]))
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

    def test_InitStatementObject(self):
        statement = Statement(object=Statement(id='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.statementVerificationHelper(statement.object)

    def test_InitSubstatementObject(self):
        statement = Statement(object=Substatement(object_type='Substatement'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.substatementVerificationHelper(statement.object)

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
        statement = Statement(result=Result(duration='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.result)

    def test_InitContext(self):
        statement = Statement(context=Context(registration='test'))
        self.assertIsNone(statement.id)
        self.assertIsNone(statement.actor)
        self.assertIsNone(statement.verb)
        self.assertIsNone(statement.object)
        self.assertIsNone(statement.timestamp)
        self.assertIsNone(statement.stored)
        self.assertIsNone(statement.authority)
        self.resultVerificationHelper(statement.context)

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
        obj = {'id':'016699c6-d600-48a7-96ab-86187498f16f', 'actor':{'name':'test'}, 'verb':{'id':'test'}, 'object':{'name':'test'}, 'authority':{'name':'test'}, 'context':{'registration':'test'}, 'attachments':[{'usage_type':'test'}]}
        statement = Statement(**obj)
        self.assertEqual(statement.id, 'test')
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_FromJSON(self):
        json_str = '{"id":"016699c6-d600-48a7-96ab-86187498f16f", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"name":"test"}, "authority":{"name":"test"}, "context":{"registration":"test"}, "attachments":[{"usage_type":"test"}]}'
        statement = Statement.from_json(json_str)
        self.assertEqual(statement.id, '016699c6-d600-48a7-96ab-86187498f16f')
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)

    def test_ToJSON(self):
        statement = Statement(**{'id':'016699c6-d600-48a7-96ab-86187498f16f', 'actor':{'name':'test'}, 'verb':{'id':'test'}, 'object':{'name':'test'}, 'authority':{'name':'test'}, 'context':{'registration':'test'}, 'attachments':[{'usage_type':'test'}]})
        self.assertEqual(statement.to_json(), '{"id":"016699c6-d600-48a7-96ab-86187498f16f", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"name":"test"}, "authority":{"name":"test"}, "context":{"registration":"test"}, "attachments":[{"usage_type":"test"}]}')

    def test_ToJSONEmpty(self):
        statement = Statement()
        self.assertEqual(statement.to_json(), '{"attachments": []}')

    def test_FromJSONToJSON(self):
        json_str = '{"id":"016699c6-d600-48a7-96ab-86187498f16f", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"name":"test"}, "authority":{"name":"test"}, "context":{"registration":"test"}, "attachments":[{"usage_type":"test"}]}'
        statement = Statement.from_json(json_str)
        self.assertEqual(statement.id, '016699c6-d600-48a7-96ab-86187498f16f')
        self.agentVerificationHelper(statement.actor)
        self.verbVerificationHelper(statement.verb)
        self.agentVerificationHelper(statement.object)
        self.agentVerificationHelper(statement.authority)
        self.contextVerificationHelper(statement.context)
        for k in statement.attachments:
            self.attachmentVerificationHelper(k)
        self.assertEqual(statement.to_json(), '{"id":"016699c6-d600-48a7-96ab-86187498f16f", "actor":{"name":"test"}, "verb":{"id":"test"}, "object":{"name":"test"}, "authority":{"name":"test"}, "context":{"registration":"test"}, "attachments":[{"usage_type":"test"}]}')

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

    def statementVerificationHelper(self, value):
        self.assertIsInstance(value, Statement)
        self.assertEqual(value.id, 'test')

    def resultVerificationHelper(self, value):
        self.assertIsInstance(value, Result)
        self.assertEqual(value.duration, 'test')

    def contextVerificationHelper(self, value):
        self.assertIsInstance(value, Context)
        self.assertEqual(value.registration, 'test')

    def attachmentVerificationHelper(self, value):
        self.assertIsInstance(value, Attachment)
        self.assertEqual(value.usage_type, 'test')

    def substatementVerificationHelper(self, value):
        self.assertIsInstance(value, Substatement)
        self.assertEqual(value.object_type, 'Substatement')

if __name__ == '__main__':
     suite = unittest.TestLoader().loadTestsFromTestCase(TestStatement)
     unittest.TextTestRunner(verbosity = 2).run(suite)