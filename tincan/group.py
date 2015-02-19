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

from tincan.agent import Agent
from tincan.agent_list import AgentList

"""

.. module:: Group
   :synopsis: An object that contains a group of Agents

"""


class Group(Agent):
    _props = [
        "member"
    ]

    _props.extend(Agent._props)

    def __init__(self, *args, **kwargs):
        self._object_type = None
        self._member = AgentList()

        super(Group, self).__init__(*args, **kwargs)

    def addmember(self, value):
        """Adds a single member to this group's list of members.
        Tries to convert to :class:`tincan.Agent`

        :param value: The member to add to this group
        :type value: :class:`tincan.Agent`

        """

        if value is not None and not isinstance(value, Agent):
            value = Agent(value)

        self._member.append(value)

    @property
    def member(self):
        """Members for Group

        :setter: Tries to convert to :class:`tincan.AgentList`
        :setter type: :class:`tincan.AgentList`
        :rtype: :class:`tincan.AgentList`
        """
        return self._member

    @member.setter
    def member(self, value):
        newmembers = AgentList()
        if value is not None:
            if isinstance(value, list):
                for k in value:
                    if not isinstance(k, Agent):
                        newmembers.append(Agent(k))
                    else:
                        newmembers.append(k)
            else:
                newmembers = AgentList(value)
        self._member = newmembers

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
    def object_type(self, _):
        self._object_type = 'Group'
