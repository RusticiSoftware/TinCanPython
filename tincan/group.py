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

"""

.. module:: Group
   :synopsis: An object that contains a group of Agents

"""


class Group(SerializableBase):

    _props = [
	    "object_type",
        "member"
    ]

    def __init__(self, *args, **kwargs):
<<<<<<< HEAD
        self._member = []
=======
        """

        :param members: The list of the members of this group
        :type members: list

        """
        self._members = []
>>>>>>> master
        super(Group, self).__init__(*args, **kwargs)

    def addmember(self, value):
        """Adds a single member to this group's list of members

        :param object_type: The object type for this group. Will always be "Group"
        :type objec_type: str
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

		:setter: Tries to convert each member to Agent
		:setter type: list[:mod:`tincan.agent`]
		:rtype: list[:mod:`tincan.agent`]

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
            else:
                 self._member = value
        value = newmembers
        self._member = value

    @member.deleter
    def member(self):
        del self._member

    @property
    def object_type(self):
        """Object type for Group

		:setter: Tries to convert to unicode
		:setter type: unicode
		:rtype: unicode

		"""
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if value != "Group":
            raise ValueError("Object_type must be 'Group'")
        elif not isinstance(value, unicode):
            value = unicode(value)
        self._object_type = value

    @object_type.deleter
    def object_type(self):
        del self._object_type

    def _as_version(self, version=Version.latest):
        return {'members': [l.as_version(version) for l in self.members]}
