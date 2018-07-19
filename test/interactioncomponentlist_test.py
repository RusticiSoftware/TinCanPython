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
import json
import unittest

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import InteractionComponentList, InteractionComponent, LanguageMap


class InteractionComponentListTest(unittest.TestCase):
    def test_InitNoArgs(self):
        iclist = InteractionComponentList()
        self.assertEqual(iclist, [])
        self.assertIsInstance(iclist, InteractionComponentList)

    def test_InitEmpty(self):
        iclist = InteractionComponentList([])
        self.assertEqual(iclist, [])
        self.assertIsInstance(iclist, InteractionComponentList)

    def test_Init(self):
        iclist = InteractionComponentList(
            [{"id": "test1", "description": {"en-US": "test1"}}, {"id": "test2", "description": {"en-US": "test2"}}]
        )
        self.listVerificationHelper(iclist)

    def test_InitList(self):
        ic1 = InteractionComponent(id='test1', description={"en-US": "test1"})
        ic2 = InteractionComponent(id='test2', description={"en-US": "test2"})
        iclist = InteractionComponentList([ic1, ic2])
        self.listVerificationHelper(iclist)

    def test_InitInteractionComponentList(self):
        ic1 = InteractionComponent(id='test1', description={"en-US": "test1"})
        ic2 = InteractionComponent(id='test2', description={"en-US": "test2"})
        arg = InteractionComponentList([ic1, ic2])
        iclist = InteractionComponentList(arg)
        self.listVerificationHelper(iclist)

    def test_InitExceptionNotInteractionComponent(self):
        with self.assertRaises(TypeError):
            InteractionComponentList([InteractionComponent(), 'not InteractionComponent'])

    def test_FromJSON(self):
        iclist = InteractionComponentList.from_json(
            '[{"id": "test1", "description": {"en-US": "test1"}}, {"id": "test2", "description": {"en-US": "test2"}}]'
        )
        self.listVerificationHelper(iclist)

    def test_FromJSONExceptionBadJSON(self):
        with self.assertRaises(ValueError):
            InteractionComponentList.from_json('{"bad JSON"}')

    def test_FromJSONExceptionNestedObject(self):
        with self.assertRaises(TypeError):
            InteractionComponentList.from_json(
                '[{"id": "test1", "description": {"en-US": "test1"}}, [{"id": "nested!"}]]'
            )

    def test_FromJSONEmptyList(self):
        iclist = InteractionComponentList.from_json('[]')
        self.assertIsInstance(iclist, InteractionComponentList)
        self.assertEqual(iclist, [])

    def test_AsVersionEmpty(self):
        iclist = InteractionComponentList()
        check = iclist.as_version()
        self.assertEqual(check, [])

    def test_AsVersionNotEmpty(self):
        ic1 = InteractionComponent(id='test1', description={"en-US": "test1"})
        ic2 = InteractionComponent(id='test2', description={"en-US": "test2"})
        iclist = InteractionComponentList([ic1, ic2])
        check = iclist.as_version()
        self.assertEqual(check,
                         [{"id": "test1", "description": {"en-US": "test1"}},
                          {"id": "test2", "description": {"en-US": "test2"}}])

    def test_ToJSONFromJSON(self):
        json_str = '[{"id": "test1", "description": {"en-US": "test1"}}, ' \
                   '{"id": "test2", "description": {"en-US": "test2"}}]'
        iclist = InteractionComponentList.from_json(json_str)
        self.listVerificationHelper(iclist)
        self.assertEqual(json.loads(iclist.to_json()), json.loads(json_str))

    def test_ToJSON(self):
        iclist = InteractionComponentList(
            [{"id": "test1", "description": {"en-US": "test1"}}, {"id": "test2", "description": {"en-US": "test2"}}])
        # since the map is unordered, it is ok that to_json() changes ordering
        self.assertEqual(json.loads(iclist.to_json()),
                         json.loads('[{"id": "test1", "description": {"en-US": "test1"}}, '
                                    '{"id": "test2", "description": {"en-US": "test2"}}]'))

    def test_setItem(self):
        iclist = InteractionComponentList([InteractionComponent(), InteractionComponent()])
        iclist[0] = {"id": "test1", "description": {"en-US": "test1"}}
        iclist[1] = InteractionComponent(id="test2", description={"en-US": "test2"})
        self.listVerificationHelper(iclist)

    def test_setItemException(self):
        ic1 = InteractionComponent(id='test1', description={"en-US": "test1"})
        ic2 = InteractionComponent(id='test2', description={"en-US": "test2"})
        iclist = InteractionComponentList([ic1, ic2])
        with self.assertRaises(TypeError):
            iclist[0] = 'not InteractionComponent'
        self.listVerificationHelper(iclist)

    def test_appendItem(self):
        ic1 = InteractionComponent(id='test1', description={"en-US": "test1"})
        ic2 = InteractionComponent(id='test2', description={"en-US": "test2"})
        iclist = InteractionComponentList()
        iclist.append(ic1)
        iclist.append(ic2)
        self.listVerificationHelper(iclist)

    def test_appendItemException(self):
        iclist = InteractionComponentList()
        with self.assertRaises(TypeError):
            iclist.append('not InteractionComponent')
        self.assertEqual(iclist, [])

    def test_appendItemCoercion(self):
        iclist = InteractionComponentList()
        iclist.append({"id": "test1", "description": {"en-US": "test1"}})
        iclist.append({"id": "test2", "description": {"en-US": "test2"}})
        self.listVerificationHelper(iclist)

    def test_extend(self):
        ic1 = InteractionComponent(id='test1')
        ic2 = InteractionComponent(id='test2')
        arglist = InteractionComponentList([ic1, ic2])
        iclist = InteractionComponentList([InteractionComponent(id='test3')])
        iclist.extend(arglist)
        self.assertEqual(len(iclist), 3)
        self.assertEqual(iclist[0].id, 'test3')
        self.assertEqual(iclist[1].id, 'test1')
        self.assertEqual(iclist[2].id, 'test2')

    def test_extendExceptionNotComponent(self):
        ic1 = InteractionComponent(id='test1')
        arglist = [ic1, 'not InteractionComponent']
        iclist = InteractionComponentList([InteractionComponent()])
        with self.assertRaises(TypeError):
            iclist.extend(arglist)

    def test_insert(self):
        ic1 = InteractionComponent(id='test1')
        ic2 = InteractionComponent(id='test3')
        iclist = InteractionComponentList([ic1, ic2])
        iclist.insert(1, InteractionComponent(id='test2'))
        self.assertEqual(len(iclist), 3)
        self.assertEqual(iclist[0].id, 'test1')
        self.assertEqual(iclist[1].id, 'test2')
        self.assertEqual(iclist[2].id, 'test3')

    def test_insertExceptionNotComponent(self):
        ic1 = InteractionComponent(id='test1')
        ic2 = InteractionComponent(id='test3')
        iclist = InteractionComponentList([ic1, ic2])
        with self.assertRaises(TypeError):
            iclist.insert(1, 'not InteractionComponent')

    def listVerificationHelper(self, iclist):
        self.assertIsInstance(iclist, InteractionComponentList)
        self.assertEqual(len(iclist), 2)
        self.assertIsInstance(iclist[0], InteractionComponent)
        self.assertIsInstance(iclist[1], InteractionComponent)
        self.assertEqual(iclist[0].id, 'test1')
        self.assertEqual(iclist[1].id, 'test2')
        self.assertEqual(iclist[0].description, LanguageMap({"en-US": "test1"}))
        self.assertEqual(iclist[1].description, LanguageMap({"en-US": "test2"}))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InteractionComponentListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
