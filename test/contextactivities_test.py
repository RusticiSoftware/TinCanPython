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
from tincan import ContextActivities, Activity, ActivityList


class ContextActivitiesTest(unittest.TestCase):
    def test_initEmpty(self):
        ctx_act = ContextActivities()
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertEqual(vars(ctx_act), {'_category': None, '_grouping': None, '_other': None, '_parent': None})

    def test_InitExceptionNotActivityOrList(self):
        with self.assertRaises(TypeError):
            # All properties are identical in structure, so this test applies to all
            # properties of ContextActivities, not just category
            ContextActivities(category='notActivityOrList')

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
        self.assertIsInstance(ctx_act.parent, ActivityList)
        self.assertEqual(ctx_act.parent[0].id, 'parentActivity')
        self.assertIsInstance(ctx_act.grouping, ActivityList)
        self.assertEqual(ctx_act.grouping[0].id, 'groupingList')
        self.assertIsInstance(ctx_act.other, ActivityList)
        self.assertEqual(ctx_act.other[0].id, 'otherActivity')

    def test_InitAnonList(self):
        ctx_act = ContextActivities(category=[Activity(id='anonymousList')])
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'anonymousList')

    def test_InitAnonActivity(self):
        ctx_act = ContextActivities(category={'id': 'anonymousActivity'})
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'anonymousActivity')

    def test_InitUnpack(self):
        obj = {'category': [{'id': 'categoryList'}], 'parent': [{'id': 'parentList'}],
               'grouping': [{'id': 'groupingList'}], 'other': [{'id': 'otherList'}]}
        ctx_act = ContextActivities(**obj)
        self.listVerificationHelper(ctx_act)

    def test_InitExceptionUnpackNotActivityOrList(self):
        obj = {'category': 'notActivityOrList', 'parent': Activity(id='parentActivity')}
        with self.assertRaises(TypeError):
            ContextActivities(**obj)

    def test_FromJSONExceptionMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ContextActivities.from_json('{"test": "invalid property"}')

    def test_FromJSONExceptionPartiallyMalformedJSON(self):
        with self.assertRaises(AttributeError):
            ContextActivities.from_json('{"category": {"id": "test"}, "test": "invalid property"}')

    def test_FromJSONEmptyObject(self):
        ctx_act = ContextActivities.from_json('{}')
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertEqual(vars(ctx_act), {'_category': None, '_grouping': None, '_other': None, '_parent': None})

    def test_FromJSONList(self):
        ctx_act = ContextActivities.from_json(
            '{"category": [{"id": "categoryList"}], "parent": [{"id": "parentList"}], '
            '"grouping": [{"id": "groupingList"}], "other": [{"id": "otherList"}]}')
        self.listVerificationHelper(ctx_act)

    def test_FromJSONActivity(self):
        ctx_act = ContextActivities.from_json(
            '{"category": {"id": "categoryActivity"}, "parent": {"id": "parentActivity"}, '
            '"grouping": {"id": "groupingActivity"}, "other": {"id": "otherActivity"}}')
        self.activityVerificationHelper(ctx_act)

    def test_AsVersionList(self):
        obj = {
            'category': [{'id': 'categoryList', "objectType": "Activity"}],
            'parent': [{'id': 'parentList', 'objectType': 'Activity'}],
            'grouping': [{'id': 'groupingList', 'objectType': 'Activity'}],
            'other': [{'id': 'otherList', 'objectType': 'Activity'}]}
        ctx_act = ContextActivities(**obj)
        self.listVerificationHelper(ctx_act)
        ctx_act2 = ctx_act.as_version()
        self.assertEqual(ctx_act2, obj)

    def test_AsVersionActivity(self):
        obj = {
            'category': {'id': 'categoryActivity', 'object_type': 'Activity'},
            'parent': {'id': 'parentActivity', 'object_type': 'Activity'},
            'grouping': {'id': 'groupingActivity', 'object_type': 'Activity'},
            'other': {'id': 'otherActivity', 'object_type': 'Activity'}}
        check_obj = {
            'category': [{'id': 'categoryActivity', 'objectType': 'Activity'}],
            'parent': [{'id': 'parentActivity', 'objectType': 'Activity'}],
            'grouping': [{'id': 'groupingActivity', 'objectType': 'Activity'}],
            'other': [{'id': 'otherActivity', 'objectType': 'Activity'}]}
        ctx_act = ContextActivities(**obj)
        self.activityVerificationHelper(ctx_act)
        ctx_act2 = ctx_act.as_version()
        self.assertEqual(ctx_act2, check_obj)

    def activityVerificationHelper(self, ctx_act):
        self.assertIsInstance(ctx_act, ContextActivities)
        self.assertIsInstance(ctx_act.category, ActivityList)
        self.assertEqual(ctx_act.category[0].id, 'categoryActivity')
        self.assertIsInstance(ctx_act.parent, ActivityList)
        self.assertEqual(ctx_act.parent[0].id, 'parentActivity')
        self.assertIsInstance(ctx_act.grouping, ActivityList)
        self.assertEqual(ctx_act.grouping[0].id, 'groupingActivity')
        self.assertIsInstance(ctx_act.other, ActivityList)
        self.assertEqual(ctx_act.other[0].id, 'otherActivity')

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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContextActivitiesTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
