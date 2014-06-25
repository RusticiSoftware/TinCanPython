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
from tincan.context import Context
from tincan.context_activities import ContextActivities
from tincan.activity import Activity
from tincan.agent import Agent
from tincan.statement_ref import StatementRef
from tincan.extensions import Extensions
from tincan.group import Group
import uuid
import re


class ContextTest(unittest.TestCase):

    def test_InitEmpty(self):
        ctx = Context()
        self.assertIsInstance(ctx, Context)
        self.assertEqual(vars(ctx), {})

    def test_InitAll(self):
        ctx = Context(
            registration=uuid.uuid4(),
            instructor=Group(member=[Agent(name='instructorGroupMember')]),
            team=Group(member=[Agent(name='teamGroupMember')]),
            context_activities=ContextActivities(category=Activity(id='contextActivityCategory')),
            revision='revision',
            platform='platform',
            language='en-US',
            statement=StatementRef(id='016699c6-d600-48a7-96ab-86187498f16f'),
            extensions=Extensions({'extensions': 'extend!'})
        )
        self.ctxVerificationHelper(ctx)

    def test_InitUUIDFromString(self):
        reg = uuid.uuid4()
        """ Uses same regex as PHP """
        ctx = Context(registration=str(reg))
        self.assertEqual(ctx.registration, reg)

    def test_InitExceptionInvalidUUID(self):
        reg = 'not a valid uuid'
        with self.assertRaises(ValueError):
            ctx = Context(registration=reg)

    """ Try to break instructor, team, context_activities. See: test_InitException... in other test classes """

    def test_InitLanguages(self):
        language_ids = ['en','ast','zh-yue','ar-afb','zh-Hans','az-Latn','en-GB','es-005','zh-Hant-HK','sl-nedis','sl-IT-nedis','de-CH-1901','de-DE-u-co-phonebk','en-US-x-twain']
        for tag in language_ids:
            ctx = Context(language=tag)
            self.assertEqual(ctx.language, tag)
            self.assertIsInstance(ctx, Context)

    def test_InitExceptionInvalidLanguage(self):
        regional_id = 'In-valiD-Code'
        with self.assertRaises(ValueError):
            ctx = Context(language=regional_id)

    """ Statement Ref tests - will be trival """
    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            ctx = Context.from_json('{"bad JSON"}')

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ctx = Context.from_json('{"test": "invalid property"}')

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ctx = Context.from_json('{"test": "invalid property", "id": \
            "valid property"}')

    def test_FromJSON(self):
        json_str = '{\
            "registration": "016699c6-d600-48a7-96ab-86187498f16f",\
            "instructor": {"member": [{"name": "instructorGroupMember"}]},\
            "team": {"member": [{"name": "teamGroupMember"}]},\
            "context_activities": {"category": {"id": "contextActivityCategory"}},\
            "revision": "revision",\
            "platform": "platform",\
            "language": "en-US",\
            "extensions": {"extensions": "extend!"}}'
        ctx = Context.from_json(json_str)
        self.ctxVerificationHelper(ctx)

    def test_AsVersion(self):
        obj = {
            "registration": "016699c6-d600-48a7-96ab-86187498f16f",
            "instructor": {"member": [{"name": "instructorGroupMember"}]},
            "team": {"member": [{"name": "teamGroupMember"}]},
            "context_activities": {"category": {"id": "contextActivityCategory"}},
            "revision": "revision",
            "platform": "platform",
            "language": "en-US",
            "extensions": {"extensions": "extend!"}
        }
        """ Keys are corrected, and ContextActivities is properly listified """
        check_obj = {
            "registration": "016699c6-d600-48a7-96ab-86187498f16f",
            "instructor": {"member": [{"name": "instructorGroupMember", "objectType": "Agent"}], "objectType": "Group"},
            "team": {"member": [{"name": "teamGroupMember", "objectType": "Agent"}], "objectType": "Group"},
            "contextActivities": {"category": [{"id": "contextActivityCategory", "objectType": "Activity"}]},
            "revision": "revision",
            "platform": "platform",
            "language": "en-US",
            "extensions": {"extensions": "extend!"}
        }
        ctx = Context(**obj)
        ctx2 = ctx.as_version()
        self.assertEqual(ctx2, check_obj)

    def ctxVerificationHelper(self, ctx):
        self.assertIsInstance(ctx, Context)
        self.assertIsInstance(ctx.registration, uuid.UUID)
        self.assertIsInstance(ctx.instructor, Group)
        self.assertEqual(ctx.instructor.member[0].name, 'instructorGroupMember')
        self.assertIsInstance(ctx.team, Group)
        self.assertEqual(ctx.team.member[0].name, 'teamGroupMember')
        self.assertIsInstance(ctx.context_activities, ContextActivities)
        self.assertEqual(ctx.context_activities.category[0].id, 'contextActivityCategory')
        self.assertEqual(ctx.revision, 'revision')
        self.assertEqual(ctx.platform, 'platform')
        self.assertEqual(ctx.language, 'en-US')
        self.assertIsInstance(ctx.extensions, Extensions)
        self.assertEqual(ctx.extensions['extensions'], 'extend!')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContextTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
