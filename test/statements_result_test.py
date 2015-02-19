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
import uuid

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import StatementsResult, Statement
from test_utils import TinCanBaseTestCase


class StatementsResultTest(TinCanBaseTestCase):
    def test_serialize_deserialize(self):
        sr = StatementsResult()
        uuid_str = '016699c6-d600-48a7-96ab-86187498f16f'
        sr.statements = [Statement(id=uuid_str), Statement(id=uuid_str), Statement(id=uuid_str), ]
        sr.more = 'http://www.example.com/more/1234'

        self.assertSerializeDeserialize(sr)

    def test_serialize_deserialize_init(self):
        uuid_str = '016699c6-d600-48a7-96ab-86187498f16f'
        data = {
            'statements': [Statement(id=uuid_str), Statement(id=uuid_str), Statement(id=uuid_str),
                           Statement(id=uuid_str), ],
            'more': 'http://www.example.com/more/1234',
        }

        sr = StatementsResult(data)
        self.assertSerializeDeserialize(sr)

    def test_read_write(self):
        sr = StatementsResult()
        self.assertEqual(len(sr.statements), 0, 'Empty StatementsResult inited as non-empty!')

        uuid_str = '016699c6-d600-48a7-96ab-86187498f16f'
        sr.statements = (Statement(id=uuid_str), Statement(id=uuid_str), Statement(id=uuid_str),)
        self.assertIsInstance(sr.statements, list, 'Did not convert tuple to list!')

        sr.statements.append(Statement(id=uuid_str))
        self.assertEqual(sr.statements[3].id, uuid.UUID('016699c6-d600-48a7-96ab-86187498f16f'),
                         'Did not append value!')

        self.assertIsNone(sr.more)

        sr.more = 'http://www.example.com/more/1234'

        self.assertEqual(sr.more, 'http://www.example.com/more/1234', 'Did not set sr.more!')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementsResultTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
