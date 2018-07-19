# Copyright 2014 Rustici Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import ActivityList, Activity


class ActivityListTest(unittest.TestCase):
    def test_InitNoArgs(self):
        alist = ActivityList()
        self.assertEqual(alist, [])
        self.assertIsInstance(alist, ActivityList)

    def test_InitEmpty(self):
        alist = ActivityList([])
        self.assertEqual(alist, [])
        self.assertIsInstance(alist, ActivityList)

    def test_Init(self):
        alist = ActivityList(
            [Activity(id='test1', object_type='Activity'), Activity(id='test2', object_type='Activity')]
        )
        self.listVerificationHelper(alist)

    def test_InitList(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        alist = ActivityList([a1, a2])
        self.listVerificationHelper(alist)

    def test_InitActivityList(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        arg = ActivityList([a1, a2])
        alist = ActivityList(arg)
        self.listVerificationHelper(alist)

    def test_InitExceptionNotActivity(self):
        with self.assertRaises(TypeError):
            ActivityList([Activity(), 'not InteractionComponent'])

    def test_FromJSON(self):
        alist = ActivityList.from_json(
            '[{"id": "test1"}, {"id": "test2"}]'
        )
        self.listVerificationHelper(alist)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            ActivityList.from_json('{"bad JSON"}')

    def test_FromJSONExceptionNestedObject(self):
        with self.assertRaises(TypeError):
            ActivityList.from_json(
                '[{"id": "test1"}, [{"id": "nested!"}]]'
            )

    def test_FromJSONEmptyList(self):
        alist = ActivityList.from_json('[]')
        self.assertIsInstance(alist, ActivityList)
        self.assertEqual(alist, [])

    def test_AsVersionEmpty(self):
        alist = ActivityList()
        check = alist.as_version()
        self.assertEqual(check, [])

    def test_AsVersionNotEmpty(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        alist = ActivityList([a1, a2])
        check = alist.as_version()
        self.assertEqual(check,
                         [{"id": "test1", "objectType": "Activity"}, {"id": "test2", "objectType": "Activity"}])

    def test_ToJSONFromJSON(self):
        json_str = '[{"id": "test1", "objectType": "Activity"}, {"id": "test2", "objectType": "Activity"}]'
        alist = ActivityList.from_json(json_str)
        self.listVerificationHelper(alist)
        self.assertEqual(json.loads(alist.to_json()), json.loads(json_str))

    def test_ToJSON(self):
        alist = ActivityList([{"id": "test1"}, {"id": "test2"}])
        self.assertEqual(json.loads(alist.to_json()),
                         json.loads(
                             '[{"id": "test1", "objectType": "Activity"}, {"id": "test2", "objectType": "Activity"}]'))

    def test_setItem(self):
        alist = ActivityList([Activity(), Activity()])
        alist[0] = {"id": "test1"}
        alist[1] = Activity(id="test2")
        self.listVerificationHelper(alist)

    def test_setItemException(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        alist = ActivityList([a1, a2])
        with self.assertRaises(TypeError):
            alist[0] = 'not Activity'
        self.listVerificationHelper(alist)

    def test_appendItem(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        alist = ActivityList()
        alist.append(a1)
        alist.append(a2)
        self.listVerificationHelper(alist)

    def test_appendItemException(self):
        alist = ActivityList()
        with self.assertRaises(TypeError):
            alist.append('not Activity')
        self.assertEqual(alist, [])

    def test_appendItemCoercion(self):
        alist = ActivityList()
        alist.append({"id": "test1"})
        alist.append({"id": "test2"})
        self.listVerificationHelper(alist)

    def test_extend(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test2', object_type='Activity')
        arglist = ActivityList([a1, a2])
        alist = ActivityList([Activity(id='test3')])
        alist.extend(arglist)
        self.assertEqual(len(alist), 3)
        self.assertEqual(alist[0].id, 'test3')
        self.assertEqual(alist[1].id, 'test1')
        self.assertEqual(alist[2].id, 'test2')

    def test_extendExceptionNotComponent(self):
        a1 = Activity(id='test1', object_type='Activity')
        arglist = [a1, 'not Activity']
        alist = ActivityList([Activity()])
        with self.assertRaises(TypeError):
            alist.extend(arglist)

    def test_insert(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test3')
        alist = ActivityList([a1, a2])
        alist.insert(1, Activity(id='test2', object_type='Activity'))
        self.assertEqual(len(alist), 3)
        self.assertEqual(alist[0].id, 'test1')
        self.assertEqual(alist[1].id, 'test2')
        self.assertEqual(alist[2].id, 'test3')

    def test_insertExceptionNotComponent(self):
        a1 = Activity(id='test1', object_type='Activity')
        a2 = Activity(id='test3')
        alist = ActivityList([a1, a2])
        with self.assertRaises(TypeError):
            alist.insert(1, 'not Activity')

    def listVerificationHelper(self, alist):
        self.assertIsInstance(alist, ActivityList)
        self.assertEqual(len(alist), 2)
        self.assertIsInstance(alist[0], Activity)
        self.assertIsInstance(alist[1], Activity)
        self.assertEqual(alist[0].id, 'test1')
        self.assertEqual(alist[1].id, 'test2')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ActivityListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
