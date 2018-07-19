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
import uuid

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import StatementRef


class StatementRefTest(unittest.TestCase):
    def test_InitObjectType(self):
        statementref = StatementRef(object_type='StatementRef')
        self.assertEqual(statementref.object_type, 'StatementRef')

    def test_InitId(self):
        statementref = StatementRef(id='016699c6-d600-48a7-96ab-86187498f16f')
        self.assertEqual(statementref.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))

    def test_InitUnpack(self):
        obj = {'object_type': 'StatementRef', 'id': '016699c6-d600-48a7-96ab-86187498f16f'}
        statementref = StatementRef(**obj)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))

    def test_FromJSON(self):
        json_str = '{"object_type":"StatementRef", "id":"016699c6-d600-48a7-96ab-86187498f16f"}'
        statementref = StatementRef.from_json(json_str)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))

    def test_ToJSON(self):
        statementref = StatementRef(object_type='StatementRef', id='016699c6-d600-48a7-96ab-86187498f16f')
        self.assertEqual(json.loads(statementref.to_json()),
                         json.loads('{"id": "016699c6-d600-48a7-96ab-86187498f16f", "objectType": "StatementRef"}'))

    def test_ToJSONNoObjectType(self):
        statementref = StatementRef(id='016699c6-d600-48a7-96ab-86187498f16f')
        self.assertEqual(json.loads(statementref.to_json()),
                         json.loads('{"id": "016699c6-d600-48a7-96ab-86187498f16f", "objectType": "StatementRef"}'))

    def test_FromJSONToJSON(self):
        json_str = '{"object_type":"StatementRef", "id":"016699c6-d600-48a7-96ab-86187498f16f"}'
        statementref = StatementRef.from_json(json_str)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'))
        self.assertEqual(json.loads(statementref.to_json()),
                         json.loads('{"id": "016699c6-d600-48a7-96ab-86187498f16f", "objectType": "StatementRef"}'))

    def test_ToJSONEmpty(self):
        statementref = StatementRef()
        self.assertEqual(statementref.to_json(), '{"objectType": "StatementRef"}')

    def test_ExceptionInvalidUUID(self):
        with self.assertRaises(ValueError):
            StatementRef(id='badtest')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementRefTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
