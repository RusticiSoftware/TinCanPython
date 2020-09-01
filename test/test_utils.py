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
    from test.main import setup_tincan_path

    setup_tincan_path()
from tincan import Version


class TinCanBaseTestCase(unittest.TestCase):
    # PEP8 says this should be lowercase, but unittest breaks this rule
    def assertSerializeDeserialize(self, obj, version=None):
        """
        Verifies that objects are packed to JSON and unpacked
        correctly for the version specified. If no version is
        specified, tests for all versions in TCAPIVersion.
        :param obj: A TinCan object to be tested.
        :param version: The version according to whose schema we will test.
        :type version: str
        """
        tested_versions = [version] if version is not None else Version.supported
        for version in tested_versions:
            constructor = obj.__class__.from_json
            json_obj = obj.to_json(version)
            clone = constructor(json_obj)

            self.assertEqual(obj.__class__, clone.__class__)

            if isinstance(obj, dict):
                orig_dict = obj
                clone_dict = clone
            else:
                orig_dict = obj.__dict__
                clone_dict = clone.__dict__

            self.assertEqual(orig_dict, clone_dict)
