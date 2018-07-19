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
from tincan.language_map import LanguageMap

"""
.. module:: interactioncomponent
   :synopsis: Provides action-level granularity to an object of a \
   statement. E.g. The text of a multiple choice question.

"""


class InteractionComponent(SerializableBase):
    _props_req = [
        'id',
    ]

    _props = [
        'description',
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._id = None
        self._description = None

        super(InteractionComponent, self).__init__(*args, **kwargs)

    @property
    def id(self):
        """Id for Agent

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._id

    @id.setter
    def id(self, value):
        if value is not None:
            if value == '':
                raise ValueError("id cannot be set to an empty string or non-string type")
        self._id = None if value is None else str(value)

    @property
    def description(self):
        """Description for Agent

        :setter: Tries to convert to :class:`tincan.LanguageMap`
        :setter type: :class:`tincan.LanguageMap`
        :rtype: :class:`tincan.LanguageMap`

        """
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._description = value

    @description.deleter
    def description(self):
        del self._description
