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
from tincan import Group, Agent, AgentAccount


class GroupTest(unittest.TestCase):

    def test_InitEmpty(self):
        group = Group()
        self.assertEquals(group.member, [])

    def test_InitObjectType(self):
        group = Group(object_type='Group')
        self.assertEqual(group.object_type, 'Group')
        self.assertEqual(group.member, [])

    def test_InitMember(self):
        group = Group(member=[Agent(name='test')])
        self.assertIsInstance(group.member[0], Agent)

    def test_InitMemberAnon(self):
        group = Group(member=[{"name":"test"}])
        self.assertIsInstance(group.member[0], Agent)

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            group = Group.from_json('')

    def test_FromJSONEmptyObject(self):
        group = Group.from_json('{}')
        self.assertEquals(group.member, [])

    def test_FromJSONmember(self):
        group = Group.from_json('''{"member":[{"name":"test"}]}''')
        for k in group.member:
            self.assertIsInstance(k, Agent)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            group = Group.from_json('{"bad JSON"}')

    def test_AddMemberAnon(self):
        group = Group()
        group.addmember({"name":"test"})
        self.assertIsInstance(group.member[0], Agent)

    def test_AddMember(self):
        group = Group()
        group.addmember(Agent(name='test'))
        self.assertIsInstance(group.member[0], Agent)

    def test_InitUnpack(self):
        obj = {"member":[{"name":"test"}]}
        group = Group(**obj)
        self.assertIsInstance(group.member[0], Agent)

    def test_ToJSONFromJSON(self):
         group = Group.from_json('{"member":[{"name":"test"}, {"name":"test2"}]}')
         self.assertIsInstance(group.member[0], Agent)
         self.assertEqual(group.to_json(), '{"member": [{"name": "test", "objectType": "Agent"}, {"name": "test2", "objectType": "Agent"}], "objectType": "Group"}')

    def test_ToJSON(self):
         group = Group(**{'member':[{'name':'test'}, {'name':'test2'}]})
         self.assertEqual(group.to_json(), '{"member": [{"name": "test", "objectType": "Agent"}, {"name": "test2", "objectType": "Agent"}], "objectType": "Group"}')

    def test_InitIFI(self):
        group = Group(name='test', mbox='mailto:test@test.com', mbox_sha1sum='test', openid='test', account=AgentAccount(name="test", home_page="test.com"), object_type='Agent')
        self.assertEqual(group.name, 'test')
        self.assertEqual(group.mbox, 'mailto:test@test.com')
        self.assertEqual(group.mbox_sha1sum, 'test')
        self.assertEqual(group.openid, 'test')
        self.assertIsInstance(group.account, AgentAccount)
        self.assertEqual(len(vars(group.account)), 2)
        self.assertIn('_name', group.account.__dict__)
        self.assertIn('_home_page', group.account.__dict__)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GroupTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
