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
from tincan.context_activities import ContextActivities
from tincan.activity import Activity
from tincan.activity_list import ActivityList


class TestContextActivities(unittest.TestCase):

    def test_initEmpty(self):
        ctx_act = ContextActivities()
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertEqual(vars(ctx_act), {})

    def test_InitExceptionNotActivityOrList(self):
        with self.assertRaises(TypeError):
            # All properties are identical in structure, so this test applies to all
            # properties of ContextActivities, not just category
            ctx_act = ContextActivities(category='notActivityOrList')

    def test_InitAsActivity(self):
        ctx_act = ContextActivities(
            category=Activity(id='categoryActivity'),
            parent=Activity(id='parentActivity'),
            grouping=Activity(id='groupingActivity'),
            other=Activity(id='otherActivity'))
        self.activityVerificationHelper(ctx_act)

    def test_InitAsList(self):
        ctx_act = ContextActivities(
            category=ActivityList([Activity(id='categoryList')]),
            parent=ActivityList([Activity(id='parentList')]),
            grouping=ActivityList([Activity(id='groupingList')]),
            other=ActivityList([Activity(id='otherList')]))
        self.listVerificationHelper(ctx_act)

    def test_InitAsEither(self):
        ctx_act = ContextActivities(
            category=ActivityList([Activity(id='categoryList')]),
            parent=Activity(id='parentActivity'),
            grouping=ActivityList([Activity(id='groupingList')]),
            other=Activity(id='otherActivity'))
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'categoryList')
        self.assertIsInstance(ctx_act.parent, Activity)
        self.assertEqual(ctx_act.parent.id, 'parentActivity')
        self.assertIsInstance(ctx_act.grouping, ActivityList)
        self.assertEqual(ctx_act.grouping[0].id, 'groupingList')
        self.assertIsInstance(ctx_act.other, Activity)
        self.assertEqual(ctx_act.other.id, 'otherActivity')

    def test_InitAnonList(self):
        ctx_act = ContextActivities(category=[Activity(id='anonymousList')])
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'anonymousList')

    def test_InitAnonActivity(self):
        ctx_act = ContextActivities(category={'id': 'anonymousActivity'})
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, Activity)
        self.assertEqual(ctx_act.category.id, 'anonymousActivity')

    def test_InitUnpack(self):
        obj = {'category': [{'id': 'categoryList'}], 'parent': [{'id': 'parentList'}], 'grouping': [{'id': 'groupingList'}], 'other': [{'id': 'otherList'}]}
        ctx_act = ContextActivities(**obj)
        self.listVerificationHelper(ctx_act)

    def test_InitExceptionUnpackNotActivityOrList(self):
        obj = {'category': 'notActivityOrList', 'parent': Activity(id='parentActivity')}
        with self.assertRaises(TypeError):
            ctx_act = ContextActivities(**obj)

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ctx_act = ContextActivities.from_json('{"test": "invalid property"}')

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ctx_act = ContextActivities.from_json('{"category": {"id": "test"}, "test": "invalid property"}')

    def test_FromJSONEmptyObject(self):
        ctx_act = ContextActivities.from_json('{}')
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertEqual(vars(ctx_act), {})

    def test_FromJSONList(self):
        ctx_act = ContextActivities.from_json('{"category": [{"id": "categoryList"}], "parent": [{"id": "parentList"}], "grouping": [{"id": "groupingList"}], "other": [{"id": "otherList"}]}')
        self.listVerificationHelper(ctx_act)

    def test_FromJSONActivity(self):
        ctx_act = ContextActivities.from_json('{"category": {"id": "categoryActivity"}, "parent": {"id": "parentActivity"}, "grouping": {"id": "groupingActivity"}, "other": {"id": "otherActivity"}}')
        self.activityVerificationHelper(ctx_act)

    def test_AsVersionList(self):
        obj = {'category': [{'id': 'categoryList'}], 'parent': [{'id': 'parentList'}], 'grouping': [{'id': 'groupingList'}], 'other': [{'id': 'otherList'}]}
        ctx_act = ContextActivities(**obj)
        self.listVerificationHelper(ctx_act)
        ctx_act2 = ctx_act.as_version()
        self.assertEqual(ctx_act2, obj)

    def test_AsVersionActivity(self):
        obj = {'category': {'id': 'categoryActivity'}, 'parent': {'id': 'parentActivity'}, 'grouping': {'id': 'groupingActivity'}, 'other': {'id': 'otherActivity'}}
        check_obj = {'category': [{'id': 'categoryActivity'}], 'parent': [{'id': 'parentActivity'}], 'grouping': [{'id': 'groupingActivity'}], 'other': [{'id': 'otherActivity'}]}
        ctx_act = ContextActivities(**obj)
        self.activityVerificationHelper(ctx_act)
        ctx_act2 = ctx_act.as_version()
        self.assertEqual(ctx_act2, check_obj)

    def activityVerificationHelper(self, ctx_act):
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, Activity)
        self.assertEqual(ctx_act.category.id, 'categoryActivity')
        self.assertIsInstance(ctx_act.parent, Activity)
        self.assertEqual(ctx_act.parent.id, 'parentActivity')
        self.assertIsInstance(ctx_act.grouping, Activity)
        self.assertEqual(ctx_act.grouping.id, 'groupingActivity')
        self.assertIsInstance(ctx_act.other, Activity)
        self.assertEqual(ctx_act.other.id, 'otherActivity')

    def listVerificationHelper(self, ctx_act):
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'categoryList')
        self.assertIsInstance(ctx_act.parent, ActivityList)
        self.assertEqual(ctx_act.parent[0].id, 'parentList')
        self.assertIsInstance(ctx_act.grouping, ActivityList)
        self.assertEqual(ctx_act.grouping[0].id, 'groupingList')
        self.assertIsInstance(ctx_act.other, ActivityList)
        self.assertEqual(ctx_act.other[0].id, 'otherList')
