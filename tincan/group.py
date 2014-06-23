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
from tincan.agent import Agent
from tincan.version import Version
from tincan.agent_list import AgentList

"""

.. module:: Group
   :synopsis: An object that contains a group of Agents

"""


class Group(Agent):

    _props = [
        "object_type",
        "member"
    ]

    def __init__(self, *args, **kwargs):
        self._member = []
        super(Group, self).__init__(*args, **kwargs)

    def addmember(self, value):
        """Adds a single member to this group's list of members

        :param value: The member to add to this group
        :type value: :mod:`tincan.agent`

        """

        if value is not None:
            if not isinstance(value, Agent):
                value = Agent(value)

        self._member.append(value)

    @property
    def member(self):
        """Members for Group

        :setter: Tries to convert to AgentList
        :setter type: :mod:`tincan.agent_list`
        :rtype: :mod:`tincan.agent_list`
        """
        return self._member

    @member.setter
    def member(self, value):
        newmembers = []
        if value is not None:
            if isinstance(value, list):
                for k in value:
                    if not isinstance(k, Agent):
                        newmembers.append(Agent(k))
                    else:
                        newmembers.append(k)
                value = AgentList(newmembers)
            else:
                value = AgentList(value)
        self._member = value

    @member.deleter
    def member(self):
        del self._member

    @property
    def object_type(self):

        """Object type for Group. Will always be "Group"

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type = 'Group'

    @object_type.deleter
    def object_type(self):
        del self._object_type
