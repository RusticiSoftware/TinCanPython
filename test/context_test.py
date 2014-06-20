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
from tincan.context import Context
from tincan.context_activities import ContextActivities
from tincan.activity import Activity
from tincan.agent import Agent
#from tincan.statement_ref import StatementRef
from tincan.extensions import Extensions
from tincan.group import Group
import uuid
import re


class TestContext(unittest.TestCase):

    def test_InitEmpty(self):
        ctx = Context()
        self.assertIsInstance(ctx, Context)
        self.assertEqual(vars(ctx), {})

    def test_InitAll(self):
        ctx = Context(
            registration=uuid.uuid4(),
            instructor=Group(members=[Agent(name='instructorGroupMember')]),
            team=Group(members=[Agent(name='teamGroupMember')]),
            context_activities=ContextActivities(category=Activity(id='contextActivityCategory')),
            revision='revision',
            platform='platform',
            language='en-US',
            #statement=StatementRef(id='statementRef'),
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
            "instructor": {"members": [{"name": "instructorGroupMember"}]},\
            "team": {"members": [{"name": "teamGroupMember"}]},\
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
            "instructor": {"members": [{"name": "instructorGroupMember"}]},
            "team": {"members": [{"name": "teamGroupMember"}]},
            "context_activities": {"category": {"id": "contextActivityCategory"}},
            "revision": "revision",
            "platform": "platform",
            "language": "en-US",
            "extensions": {"extensions": "extend!"}
        }
        """ Keys are corrected, and ContextActivities is properly listified """
        check_obj = {
            "registration": "016699c6-d600-48a7-96ab-86187498f16f",
            "instructor": {"members": [{"name": "instructorGroupMember", "objectType": "Agent"}]},
            "team": {"members": [{"name": "teamGroupMember", "objectType": "Agent"}]},
            "contextActivities": {"category": [{"id": "contextActivityCategory"}]},
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
        self.assertEqual(ctx.instructor.members[0].name, 'instructorGroupMember')
        self.assertIsInstance(ctx.team, Group)
        self.assertEqual(ctx.team.members[0].name, 'teamGroupMember')
        self.assertIsInstance(ctx.context_activities, ContextActivities)
        self.assertEqual(ctx.context_activities.category.id, 'contextActivityCategory')
        self.assertEqual(ctx.revision, 'revision')
        self.assertEqual(ctx.platform, 'platform')
        self.assertEqual(ctx.language, 'en-US')
        #self.assertIsInstance(ctx.statement, StatementRef)
        #self.assertEqual(ctx.statement.id, 'statementRef')
        self.assertIsInstance(ctx.extensions, Extensions)
        self.assertEqual(ctx.extensions['extensions'], 'extend!')
