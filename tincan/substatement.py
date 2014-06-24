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
from tincan.activity import Activity

class Substatement(SerializableBase):

    _props_req = [
        'object_type'
    ]

    _props = [
        "actor",
        "verb",
        "object"
    ]

    _props.extend(_props_req)

    @property
    def actor(self):
        """Actor for Substatement

        :setter: Tries to convert to Agent
        :setter type: :mod:`tincan.agent`
        :rtype: :mod:`tincan.agent`

        """
        return self._actor

    @actor.setter
    def actor(self, value):
        if value is not None and not isinstance(value, Agent) and not isinstance(value, Group):
                if isinstance(value, list):
                    value = Group(member=value)
                else:
                    value = Agent(value)
        self._actor = value

    @actor.deleter
    def actor(self):
        del(self._actor)

    @property
    def verb(self):
        """Verb for Substatement

        :setter: Tries to convert to Verb
        :setter type: :mod:`tincan.verb`
        :rtype: :mod:`tincan.verb`

        """
        return self._verb

    @verb.setter
    def verb(self, value):
        if value is not None and not isinstance(value, Verb):
                value = Verb(value)
        self._verb = value

    @verb.deleter
    def verb(self):
        del(self._verb)

    @property
    def object(self):
        """Object for Substatement

        :setter: Setter for object
        :setter type: :mod:`tincan.Agent` | :mod:`tincan.Group`
        :rtype: :mod:`tincan.agent` | :mod:`tincan.group` | :mod:`tincan.activity` |

        """
        return self._object

    @object.setter
    def object(self, value):
        if value is not None and not isinstance(value, Agent) and not isinstance(value, Group) and not isinstance(value, Activity):
                if isinstance(value, list):
                    value = Group(member=value)
                else:
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
        del(self._object)

    @property
    def object_type(self):
        """Object Type for Substatement. Will always be "SubStatement"

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type = 'SubStatement'
