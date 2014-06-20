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

"""
.. module:: verb
   :synopsis: A Verb object that contains an id and a display

"""


class Verb(SerializableBase):

    _props_req = [
        'id',
    ]

    _props = [
        'display',
    ]

    _props.extend(_props_req)

    def __repr__(self):
        return 'Verb: %s' % self.__dict__

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        """Setter for the _id attribute. Tries to convert to str

        :param value: The desired value for id
        :type value: basestring

        """
        if value is not None:
            if value == '':
                raise ValueError(
                    "Property 'id' in 'tincan.%s' object must be not empty." \
                    % self.__class__.__name__)
        self._id = None if value is None else str(value)

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        """Setter for the _display attribute. Tries to convert to str

        :param value: The desired value for display
        :type value: LanguageMap | dict

        """
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._display = value

    @display.deleter
    def display(self):
        del self._display
