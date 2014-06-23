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

from tincan.serializable_base import SerializableBase
from tincan.language_map import LanguageMap
from tincan.statement_targetable import StatementTargetable
from tincan.activity_definition import ActivityDefinition
from tincan.verb import Verb

"""
.. module:: activity
   :synopsis: The Activity object that defines the boundaries on the 'Object' \
   part of 'Actor-Verb-Object' structure of a Statement

"""


class Activity(SerializableBase, StatementTargetable):

    _props_req = [
        'id',
    ]

    _props = [
        'object_type',
        'definition',
    ]

    _props.extend(_props_req)

    @property
    def id(self):
        """Id for Activity

		:setter: Sets the id
		:setter type: unicode
		:rtype: unicode

		"""
        return self._id

    @id.setter
    def id(self, value):
        if value is not None:
            if value == '':
                raise ValueError(
                    "Property 'id' in 'tincan.%s' object must be not empty." \
                    % self.__class__.__name__)
        self._id = None if value is None else str(value)

    @property
    def object_type(self):
        """Object type for Activity. Must be "Activity"

		:setter: Tries to convert to unicode
		:setter type: unicode
		:rtype: unicode

		"""
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if str(value) != 'Activity':
            raise ValueError("object type must be 'Activity'")
        self._object_type = unicode(value)

    @object_type.deleter
    def object_type(self):
        del self._object_type

    @property
    def definition(self):
        """Definition for Activity

		:setter: Tries to convert to ActivityDefinition
		:setter type: :mod:`tincan.activity_definition`
		:rtype: :mod:`tincan.activity_definition`

		"""
        return self._definition

    @definition.setter
    def definition(self, value):
        if value is not None and not isinstance(value, ActivityDefinition):
            value = ActivityDefinition(value)
        self._definition = value

    @definition.deleter
    def definition(self):
        del self._definition
