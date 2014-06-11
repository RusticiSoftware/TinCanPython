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

import json
from version import Version

"""
.. module:: tincanbase
   :synopsis: A Base level object that provides common functionality to other \
   TinCan objects

"""


class IgnoreNoneEncoder(json.JSONEncoder):

    def default(self, obj):
        """A Default Encoder for serializing only attributes of a class that \
        are not None.

        .. note:: This Encoder allows an empty object to be serialized

        :params obj: the object to be serialized

        """
        result = {}
        for k, v in vars(obj).iteritems():
            if v is not None:
                result[k] = v
        return result


class TinCanBaseObject(object):

    @classmethod
    def from_json(cls, json_data):
        """Tries to convert a JSON representation to an object of the same \
        type as self

        A class can provide a _fromJSON implementation in order to do specific\
         type checking or other custom implementation details. This method \
        will throw a ValueError for invalid JSON, a TypeError for \
        improperly constructed, but valid JSON, and any custom errors \
        that can be be propagated from class constructors.

        :param json_data: The JSON string to convert
        :type json_data: str

        :raises: TypeError, ValueError, LangaugeMapInitError

        """
        data = json.loads(json_data)
        result = cls(**data)
        if "_from_json" in dir(result):
            result._from_json()
        return result

    def to_json(self, version=Version.latest, encoder=IgnoreNoneEncoder):
        """Tries to convert an object into a JSON respresentation and return \
        the resulting string

        An Object can define how it is serialized by providing an _as_version() \
        implementation. A caller may further define how the object is serialized\
        by passing in a custom encoder. The default encoder will ignore \
        properties of an object that are None at the time of serialization.

        :param version: The version to which the object must be serialized to.\
        This will default to the latest version supported by the library.
        :type version: str
        :param encoder: The custom encoder. The default is described above.
        :type encoder: json.JSONEncoder

        """
        return json.dumps(self.as_version(version), cls=encoder)

    def as_version(self, version=Version.latest):
        """Returns an object that has been modified based on versioning \
        in order to be represented in JSON properly

        A class can provide an _asVersion(self, result, version) \
        implementation in order to tailor a more specific representation

        :param version: the relevant version. This allows for variance \
         between versions
        :type version: str

        """
        result = self
        if "_as_version" in dir(self):
            self._as_version(result, version)
        return result
