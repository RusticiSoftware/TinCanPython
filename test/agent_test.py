# Copyright 2014 Rustici Software
#
#   Licensed under the Apache License, Version 2.0 (the "License");
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
from tincan.agent import Agent
from tincan.agentaccount import AgentAccount

class TestAgent(unittest.TestCase):

    def test_InitEmpty(self):
        agent = Agent()
        self.assertEqual(agent.objecttype, "Agent")
        self.assertIsNone(agent.name)
        self.assertIsNone(agent.mbox)
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_InitName(self):
        agent = Agent(name='test')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertIsNone(agent.mbox)
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_InitMboxNoMailto(self):
        agent = Agent(name='test', mbox='test@test.com')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_InitMboxMailto(self):
        agent = Agent(name='test', mbox='mailto:test@test.com')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_InitMboxSha1(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_InitOpenId(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='test')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.assertIsNone(agent.account)

    def test_InitEmptyAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='test', account={})
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.assertIsNone(agent.account)

    def test_InitAnonAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='test', account={"name": "test", "homepage": "test.com"})
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='test', account=AgentAccount(name="test", homepage="test.com"))
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitObjectType(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='test', account=AgentAccount(name="test", homepage="test.com"), objecttype='Agent')
        self.assertEqual(agent.objecttype, 'Agent')
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitExceptionEmptyName(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='')

    def test_InitExceptionBadName(self):
        with self.assertRaises(TypeError):
            agent = Agent(name={})

    def test_InitExceptionEmptyMbox(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox='')

    def test_InitExceptionBadMbox(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox={})

    def test_InitExceptionEmptymboxsha1sum(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='')

    def test_InitExceptionBadmboxsha1sum(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum={})

    def test_InitExceptionEmptyOpenid(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid='')

    def test_InitExceptionBadOpenid(self):
        with self.assertRaises(TypeError):
            agent = Agent(name='test', mbox='mailto:test@test.com', mboxsha1sum='test', openid={})

    def test_FromJSONEmpty(self):
        with self.assertRaises(ValueError):
            agent = Agent.from_json('')

    def test_FromJSONName(self):
        agent = Agent.from_json('{"name":"test"}')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertIsNone(agent.mbox)
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_FromJSONMboxNoMailto(self):
        agent = Agent.from_json('{"name":"test", "mbox":"test@test.com"}')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_FromJSONMboxMailto(self):
        agent = Agent.from_json('{"name":"test", "mbox":"mailto:test@test.com"}')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertIsNone(agent.mboxsha1sum)
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_FromJSONMboxSha1(self):
        agent = Agent.from_json('{"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test"}')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertIsNone(agent.openid)
        self.assertIsNone(agent.account)

    def test_FromJSONOpenId(self):
        agent = Agent.from_json('{"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":"test"}')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.assertIsNone(agent.account)

    def test_FromJSONAccount(self):
        agent = Agent.from_json('''{"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":"test", "account":"{'name':'test', 'homepage':'test.com'}"}''')
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_FromJSONObjectType(self):
        agent = Agent.from_json('''{"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":"test", "account":"{'name':'test', 'homepage':'test.com'}", "objecttype":"Test"}''')
        self.assertEqual(agent.objecttype, 'Test')
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitUnpack(self):
        obj = {"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":"test", "account":"{'name':'test', 'homepage':'test.com'}"}
        agent = Agent(**obj)
        self.assertEqual(agent.objecttype, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mboxsha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitExceptionUnpackEmptyName(self):
        obj = {"name":""}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackBadName(self):
        obj = {"name":{}}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackEmptyMbox(self):
        obj = {"name":"test", "mbox":""}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackBadMbox(self):
        obj = {"name":"test", "mbox":{}}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackEmptymboxsha1sum(self):
        obj = {"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":""}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackBadmboxsha1sum(self):
        obj = {"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":{}}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackEmptyOpenid(self):
        obj = {"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":""}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def test_InitExceptionUnpackBadOpenid(self):
        obj = {"name":"test", "mbox":"mailto:test@test.com", "mboxsha1sum":"test", "openid":{}}
        with self.assertRaises(TypeError):
            agent = Agent(**obj)

    def accountVerificationHelper(self, account):
        self.assertIsInstance(account, AgentAccount)
        self.assertEqual(len(vars(account)), 2)
        self.assertIn('_name', account.__dict__)
        self.assertIn('_homepage', account.__dict__)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgent)
    unittest.TextTestRunner(verbosity = 2).run(suite)