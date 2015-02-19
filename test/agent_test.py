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

import unittest

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import Agent, AgentAccount


class AgentTest(unittest.TestCase):
    def test_InitEmpty(self):
        agent = Agent()
        self.assertEqual(agent.object_type, "Agent")

    def test_InitName(self):
        agent = Agent(name='test')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')

    def test_InitMboxNoMailto(self):
        agent = Agent(name='test', mbox='test@test.com')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')

    def test_InitMboxMailto(self):
        agent = Agent(name='test', mbox='mailto:test@test.com')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')

    def test_InitMboxSha1(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')

    def test_InitOpenId(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')

    def test_InitEmptyAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test', account={})
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.assertIsInstance(agent.account, AgentAccount)

    def test_InitAnonAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test',
                      account={"name": "test", "home_page": "test.com"})
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitAccount(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test',
                      account=AgentAccount(name="test", home_page="test.com"))
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_Initobject_type(self):
        agent = Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test',
                      account=AgentAccount(name="test", home_page="test.com"), object_type='Agent')
        self.assertEqual(agent.object_type, 'Agent')
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitExceptionEmptyName(self):
        with self.assertRaises(ValueError):
            Agent(name='')

    def test_InitExceptionEmptyMbox(self):
        with self.assertRaises(ValueError):
            Agent(name='test', mbox='')

    def test_InitExceptionEmptymbox_sha1sum(self):
        with self.assertRaises(ValueError):
            Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='')

    def test_InitExceptionEmptyOpenid(self):
        with self.assertRaises(ValueError):
            Agent(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='')

    def test_FromJSONEmpty(self):
        with self.assertRaises(ValueError):
            Agent.from_json('')

    def test_FromJSONName(self):
        agent = Agent.from_json('{"name":"test"}')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')

    def test_FromJSONMboxNoMailto(self):
        agent = Agent.from_json('{"name":"test", "mbox":"test@test.com"}')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')

    def test_FromJSONMboxMailto(self):
        agent = Agent.from_json('{"name":"test", "mbox":"mailto:test@test.com"}')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')

    def test_FromJSONMboxSha1(self):
        agent = Agent.from_json('{"name":"test", "mbox":"mailto:test@test.com", "mbox_sha1sum":"test"}')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')

    def test_FromJSONOpenId(self):
        agent = Agent.from_json(
            '{"name":"test", "mbox":"mailto:test@test.com", "mbox_sha1sum":"test", "openid":"test"}')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')

    def test_FromJSONAccount(self):
        agent = Agent.from_json(
            '''{"name":"test", "mbox":"mailto:test@test.com", "mbox_sha1sum":"test", "openid":"test",
            "account":{"name":"test", "home_page":"test.com"}}''')
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_FromJSONobject_type(self):
        agent = Agent.from_json(
            '''{"name":"test", "mbox":"mailto:test@test.com", "mbox_sha1sum":"test", "openid":"test",
            "account":{"name":"test", "home_page":"test.com"}, "object_type":"Test"}''')
        self.assertEqual(agent.object_type, 'Agent')
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitUnpack(self):
        obj = {"name": "test", "mbox": "mailto:test@test.com", "mbox_sha1sum": "test", "openid": "test",
               "account": {'name': 'test', 'home_page': 'test.com'}}
        agent = Agent(**obj)
        self.assertEqual(agent.object_type, "Agent")
        self.assertEqual(agent.name, 'test')
        self.assertEqual(agent.mbox, 'mailto:test@test.com')
        self.assertEqual(agent.mbox_sha1sum, 'test')
        self.assertEqual(agent.openid, 'test')
        self.accountVerificationHelper(agent.account)

    def test_InitExceptionUnpackEmptyName(self):
        obj = {"name": ""}
        with self.assertRaises(ValueError):
            Agent(**obj)

    def test_InitExceptionUnpackEmptyMbox(self):
        obj = {"name": "test", "mbox": ""}
        with self.assertRaises(ValueError):
            Agent(**obj)

    def test_InitExceptionUnpackEmptymbox_sha1sum(self):
        obj = {"name": "test", "mbox": "mailto:test@test.com", "mbox_sha1sum": ""}
        with self.assertRaises(ValueError):
            Agent(**obj)

    def test_InitExceptionUnpackEmptyOpenid(self):
        obj = {"name": "test", "mbox": "mailto:test@test.com", "mbox_sha1sum": "test", "openid": ""}
        with self.assertRaises(ValueError):
            Agent(**obj)

    def accountVerificationHelper(self, account):
        self.assertIsInstance(account, AgentAccount)
        self.assertEqual(len(vars(account)), 2)
        self.assertIn('_name', account.__dict__)
        self.assertIn('_home_page', account.__dict__)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AgentTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
