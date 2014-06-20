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
from tincan.group import Group
from tincan.verb import Verb

class Substatement(SerializableBase):

    _props = [
        "object_type",
        "actor",
        "verb",
        "object"
	]

    @property
    def actor(self):
        """Actor for Substatement

		:setter: Tries to convert to Agent
		:setter type: :mod:`tincan.Agent`
		:rtype: :mod:`tincan.Agent`

		"""
        return self._actor

    @actor.setter
    def actor(self, value):
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Agent) and not isinstance(value, Group):
                if isinstance(value, list):
                    value = Group(members=value)
                else:
                    value = Agent(value)
            elif len(vars(value)) == 0:
                value = None
        self._actor = value

    @actor.deleter
    def actor(self):
        del(self._actor)

    @property
    def verb(self):
        """Verb for Substatement

		:setter: Tries to convert to Verb
		:setter type: :mod:`tincan.Verb`
		:rtype: :mod:`tincan.Verb`

		"""
        return self._verb

    @verb.setter
    def verb(self, value):
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Verb):
                value = Verb(value)
            elif len(vars(value)) == 0:
                value = None
        self._verb = value

    @verb.deleter
    def verb(self):
        del(self._verb)

    @property
    def object(self):
        """Object for Substatement

		:setter: Setter for object
		:setter type: :mod:`tincan.Agent` | :mod:`tincan.Group`
		:rtype: :mod:`tincan.Agent` | :mod:`tincan.Group`

		"""
        return self._object

    @object.setter
    def object(self, value):
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Agent) and not isinstance(value, Group):
                if isinstance(value, list):
                    value = Group(value)
                else:
                    value = Agent(value)
            elif len(vars(value)) == 0:
                value = None
        self._object = value

    @object.deleter
    def object(self):
        del(self._object)

    @property
    def object_type(self):
        """Object Type for Substatement. Must be "Substatement"

		:setter: Tries to convert to unicode
		:setter type: unicode
		:rtype: unicode

		"""
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if value != "Substatement":
            raise ValueError("Object_type must be 'Substatement'")
        elif not isinstance(value, unicode):
            value = unicode(value)
        self._object_type = value

    @object_type.deleter
    def object_type(self):
        del self._object_type