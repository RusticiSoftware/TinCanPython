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

from tincan.serializable_base import SerializableBase
from tincan.statement_targetable import StatementTargetable
from tincan.activity_definition import ActivityDefinition

"""
.. module:: activity
   :synopsis: The Activity object that defines the boundaries on the 'Object' \
   part of 'Actor-Verb-Object' structure of a Statement

"""


class Activity(SerializableBase, StatementTargetable):
    _props_req = [
        'id',
        'object_type'
    ]

    _props = [
        'definition',
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._id = None
        self._object_type = None
        self._definition = None

        super(Activity, self).__init__(*args, **kwargs)

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
                    f"Property 'id' in 'tincan.{self.__class__.__name__}' object must be not empty."
                )
        self._id = None if value is None else str(value)

    @property
    def object_type(self):
        """Object type for Activity. Will always be "Activity"

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._object_type

    @object_type.setter
    def object_type(self, _):
        self._object_type = 'Activity'

    @property
    def definition(self):
        """Definition for Activity

        :setter: Tries to convert to :class:`tincan.ActivityDefinition`
        :setter type: :class:`tincan.ActivityDefinition`
        :rtype: :class:`tincan.ActivityDefinition`

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
