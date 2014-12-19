# Copyright 2014 Rustici Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

from tincan.statement_base import StatementBase
from tincan.agent import Agent
from tincan.group import Group
from tincan.activity import Activity


class SubStatement(StatementBase):
    _props_req = [
        'object_type'
    ]

    _props = []

    _props.extend(StatementBase._props)
    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._object_type = None

        super(SubStatement, self).__init__(*args, **kwargs)

    @property
    def object(self):
        """Object for SubStatement

        :setter: Setter for object
        :setter type: :class:`tincan.Agent` | :class:`tincan.Group` | :class:`tincan.Activity`
        :rtype: :class:`tincan.Agent` | :class:`tincan.Group` | :class:`tincan.Activity`

        """
        return self._object

    @object.setter
    def object(self, value):
        if value is not None and \
                not isinstance(value, Agent) and \
                not isinstance(value, Group) and \
                not isinstance(value, Activity):
            if isinstance(value, dict):
                if 'object_type' in value or 'objectType' in value:
                    if 'objectType' in value:
                        value['object_type'] = value['objectType']
                        value.pop('objectType')
                    if value['object_type'] == 'Agent':
                        value = Agent(value)
                    elif value['object_type'] == 'Activity':
                        value = Activity(value)
                    elif value['object_type'] == 'Group':
                        value = Group(value)
                    else:
                        value = Activity(value)
                else:
                    value = Activity(value)
        self._object = value

    @object.deleter
    def object(self):
        del self._object

    @property
    def object_type(self):
        """Object Type for SubStatement. Will always be "SubStatement"

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._object_type

    @object_type.setter
    def object_type(self, _):
        self._object_type = 'SubStatement'
