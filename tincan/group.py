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

"""

.. module:: Group
   :synopsis: An object that contains a group of Agents

"""


class Group(SerializableBase):
    _props = [
        "members"
    ]

    def __init__(self, *args, **kwargs):
        """

        :param members: The list of the members of this group
        :type members: list

        """

        self._members = []

        super(Group, self).__init__(*args, **kwargs)


    def addmember(self, value):
        """Adds a single member to this group's list of members

        :param value: The member to add to this group
        :type value: :mod:`tincan.agent`

        """

        if value is not None:
            if not isinstance(value, Agent):
                value = Agent(value)

        self._members.append(value)

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        """Setter for the _members attribute

        :param value: The group's members
        :type value: list

        """
        newmembers = []
        if value is not None:
            if isinstance(value, list):
                for k in value:
                    if not isinstance(k, Agent):
                        newmembers.append(Agent(k))
                    else:
                        newmembers.append(k)
            else:
                 self.members = value
        value = newmembers
        self._members = value

    @members.deleter
    def members(self):
        del self._members
