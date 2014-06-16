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

from tincan.serializablebase import SerializableBase

"""

.. module:: Agent Account
   :synopsis: The account object that can be included in an agent

"""

class AgentAccount(SerializableBase):
    _props = [
        "name",
        "homepage"
    ]

    def __init__(self, *args, **kwargs):
        """

        :param name: The account name
        :type name: str
        :param homepage: The URL for the account's page
        :type homepage: str

        """

        super(AgentAccount, self).__init__(*args, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Setter for the _name attribute.

        :param value: The account's name
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value is '':
                raise ValueError("Property name can not be set to an empty string")
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def homepage(self):
        return self._homepage

    @homepage.setter
    def homepage(self, value):
        """Setter for the _homepage attribute

        :param value: The account's homepage
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value is '':
                raise ValueError("Property homepage can not be set to an empty string")
        self._homepage = value

    @homepage.deleter
    def homepage(self):
        del self._homepage