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

from serializablebase import SerializableBase
from agent import Agent

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

		new_kwargs = {}
		for obj in args:
			new_kwargs.update(obj if isinstance(obj, dict) else obj.__dict__)

		if kwargs:
			new_kwargs.update(kwargs)

		filtered_keys = [k for k in new_kwargs.keys() if k in self._props]
		for k in filtered_keys:
			setattr(self, k, new_kwargs[k])


	def addmember(self, member):
		"""Adds a single member to this group's list of members

		:param member: The member to add to this group
		:type member: :mod:`tincan.agent`

		"""

		if member is not None:
			if not isinstance(member, Agent):
				member = Agent(member=member)

		self._members.append(member)

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
			for member in value:
				if not isinstance(member, Agent):
					newmembers.append(Agent(member=member))
				else:
					newmembers.append(member)
		value = newmembers
		self._members = value

	@members.deleter
	def members(self):
		del self._members