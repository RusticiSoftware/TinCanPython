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
import uuid
import datetime
import re

from tincan.base import Base
from tincan.version import Version
from tincan.conversions.iso8601 import jsonify_datetime, jsonify_timedelta


"""
.. module:: serializable_base
   :synopsis: A base object that provides the common initializer from :class:`tincan.Base`
   as well as common serialization functionality

"""


class SerializableBase(Base):
    _props_corrected = {
        '_more_info': 'moreInfo',
        '_interaction_type': 'interactionType',
        '_correct_responses_pattern': 'correctResponsesPattern',
        '_object_type': 'objectType',
        '_usage_type': 'usageType',
        '_content_type': 'contentType',
        '_fileurl': 'fileUrl',
        '_context_activities': 'contextActivities',
        '_home_page': 'homePage',
    }

    _UUID_REGEX = re.compile(
        r'^[a-f0-9]{8}-'
        r'[a-f0-9]{4}-'
        r'[1-5][a-f0-9]{3}-'
        r'[89ab][a-f0-9]{3}-'
        r'[a-f0-9]{12}$'
    )

    def __init__(self, *args, **kwargs):

        new_kwargs = {}
        for obj in args:
            new_kwargs.update(obj if isinstance(obj, dict) else vars(obj))

        new_kwargs.update(kwargs)

        for uscore, camel in self._props_corrected.items():
            if camel in new_kwargs:
                new_kwargs[uscore[1:]] = new_kwargs[camel]
                new_kwargs.pop(camel)

        super(SerializableBase, self).__init__(**new_kwargs)

    @classmethod
    def from_json(cls, json_data):
        """Tries to convert a JSON representation to an object of the same
        type as self

        A class can provide a _fromJSON implementation in order to do specific
        type checking or other custom implementation details. This method
        will throw a ValueError for invalid JSON, a TypeError for
        improperly constructed, but valid JSON, and any custom errors
        that can be be propagated from class constructors.

        :param json_data: The JSON string to convert
        :type json_data: str | unicode

        :raises: TypeError, ValueError, LanguageMapInitError
        """

        data = json.loads(json_data)
        result = cls(data)
        if hasattr(result, "_from_json"):
            result._from_json()
        return result

    def to_json(self, version=Version.latest):
        """Tries to convert an object into a JSON representation and return
        the resulting string

        An Object can define how it is serialized by overriding the as_version()
        implementation. A caller may further define how the object is serialized
        by passing in a custom encoder. The default encoder will ignore
        properties of an object that are None at the time of serialization.

        :param version: The version to which the object must be serialized to.
        This will default to the latest version supported by the library.
        :type version: str | unicode

        """
        return json.dumps(self.as_version(version))

    def as_version(self, version=Version.latest):
        """Returns a dict that has been modified based on versioning
        in order to be represented in JSON properly

        A class should overload as_version(self, version)
        implementation in order to tailor a more specific representation

        :param version: the relevant version. This allows for variance
         between versions
        :type version: str | unicode

        """
        if not isinstance(self, list):
            result = {}
            for k, v in iter(self.items()) if isinstance(self, dict) else iter(vars(self).items()):
                k = self._props_corrected.get(k, k)
                if isinstance(v, SerializableBase):
                    result[k] = v.as_version(version)
                elif isinstance(v, list):
                    result[k] = []
                    for val in v:
                        if isinstance(val, SerializableBase):
                            result[k].append(val.as_version(version))
                        else:
                            result[k].append(val)
                elif isinstance(v, uuid.UUID):
                    result[k] = str(v)
                elif isinstance(v, datetime.timedelta):
                    result[k] = jsonify_timedelta(v)
                elif isinstance(v, datetime.datetime):
                    result[k] = jsonify_datetime(v)
                else:
                    result[k] = v
            result = self._filter_none(result)
        else:
            result = []
            for v in self:
                if isinstance(v, SerializableBase):
                    result.append(v.as_version(version))
                else:
                    result.append(v)
        return result

    @staticmethod
    def _filter_none(obj):
        """Filters out attributes set to None prior to serialization, and
        returns a new object without those attributes. This saves
        the serializer from sending empty bytes over the network. This method also
        fixes the keys to look as expected by ignoring a leading '_' if it
        is present.

        :param obj: the dictionary representation of an object that may have
        None attributes
        :type obj: dict

        """
        result = {}
        for k, v in obj.items():
            if v is not None:
                if k.startswith('_'):
                    k = k[1:]
                result[k] = v
        return result
