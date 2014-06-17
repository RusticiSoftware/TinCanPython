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
from tincan.group import Group
from tincan.agent import Agent

class TestGroup(unittest.TestCase):

    def test_InitEmpty(self):
        group = Group()
        self.assertEquals(group.members, [])

    def test_InitMember(self):
        group = Group(members=[Agent(name='test')])
        self.assertIsInstance(group.members[0], Agent)

    def test_InitMemberAnon(self):
        group = Group(members=[{"name":"test"}])
        self.assertIsInstance(group.members[0], Agent)

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            group = Group.from_json('')

    def test_FromJSONEmptyObject(self):
        group = Group.from_json('{}')
        self.assertEquals(group.members, [])

    def test_FromJSONMembers(self):
        group = Group.from_json('''{"members":[{"name":"test"}]}''')
        for k in group.members:
            self.assertIsInstance(k, Agent)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            group = Group.from_json('{"bad JSON"}')

    def test_AddMemberAnon(self):
        group = Group()
        group.addmember({"name":"test"})
        self.assertIsInstance(group.members[0], Agent)

    def test_AddMember(self):
        group = Group()
        group.addmember(Agent(name='test'))
        self.assertIsInstance(group.members[0], Agent)

    def test_InitUnpack(self):
        obj = {"members":[{"name":"test"}]}
        group = Group(**obj)
        self.assertIsInstance(group.members[0], Agent)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroup)
    unittest.TextTestRunner(verbosity = 2).run(suite)
