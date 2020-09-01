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

"""

.. module:: Agent Account
   :synopsis: The account object that can be included in an agent

"""


class AgentAccount(SerializableBase):
    _props = [
        "name",
        "home_page"
    ]

    def __init__(self, *args, **kwargs):
        self._name = None
        self._home_page = None

        super(AgentAccount, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """Name for Account

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._name

    @name.setter
    def name(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property name can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def home_page(self):
        """Homepage for Account

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._home_page

    @home_page.setter
    def home_page(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property homepage can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._home_page = value

    @home_page.deleter
    def home_page(self):
        del self._home_page
