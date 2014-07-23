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
from tincan import TypedList


class TypedListTest(unittest.TestCase):

    def test_Init(self):
        with self.assertRaises(ValueError):
            tlist = TypedList()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TypedListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
