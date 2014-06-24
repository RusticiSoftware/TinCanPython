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
from tincan.statement_ref import StatementRef

class StatementRefTest(unittest.TestCase):

    def test_InitObjectType(self):
        statementref = StatementRef(object_type='StatementRef')
        self.assertEqual(statementref.object_type, 'StatementRef')

    def test_InitId(self):
        statementref = StatementRef(id='test')
        self.assertEqual(statementref.id, 'test')

    def test_InitUnpack(self):
        obj = {'object_type':'StatementRef', 'id':'test'}
        statementref = StatementRef(**obj)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, 'test')

    def test_FromJSON(self):
        json_str = '{"object_type":"StatementRef", "id":"test"}'
        statementref = StatementRef.from_json(json_str)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, 'test')

    def test_ToJSON(self):
        statementref = StatementRef(object_type='StatementRef', id='test')
        self.assertEqual(statementref.to_json(), '{"id": "test", "objectType": "StatementRef"}')

    def test_ToJSONNoObjectType(self):
        statementref = StatementRef(id='test')
        self.assertEqual(statementref.to_json(), '{"id": "test", "objectType": "StatementRef"}')

    def test_FromJSONToJSON(self):
        json_str = '{"object_type":"StatementRef", "id":"test"}'
        statementref = StatementRef.from_json(json_str)
        self.assertEqual(statementref.object_type, 'StatementRef')
        self.assertEqual(statementref.id, 'test')
        self.assertEqual(statementref.to_json(), '{"id": "test", "objectType": "StatementRef"}')

    def test_ToJSONEmpty(self):
        statementref = StatementRef()
        self.assertEqual(statementref.to_json(), '{}')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementRefTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
