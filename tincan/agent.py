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
from tincan.agent_account import AgentAccount

"""

.. module:: Agent
   :synopsis: The Agent object that contains the information about an Agent

"""


class Agent(SerializableBase):
    _props_req = [
        "object_type"
    ]

    _props = [
        "name",
        "mbox",
        "mbox_sha1sum",
        "openid",
        "account"
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._object_type = None
        self._name = None
        self._mbox = None
        self._mbox_sha1sum = None
        self._openid = None
        self._account = None

        super(Agent, self).__init__(*args, **kwargs)

    @property
    def object_type(self):
        """Object Type for Agent. Will always be 'Agent'

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._object_type

    @object_type.setter
    def object_type(self, _):
        self._object_type = 'Agent'

    @property
    def name(self):
        """Name for Agent

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
    def mbox(self):
        """Mbox for Agent

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._mbox

    @mbox.setter
    def mbox(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property mbox can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        if not value.startswith("mailto:"):
            value = "mailto:" + value
        self._mbox = value

    @mbox.deleter
    def mbox(self):
        del self._mbox

    @property
    def mbox_sha1sum(self):
        """Mbox_sha1sum for Agent

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._mbox_sha1sum

    @mbox_sha1sum.setter
    def mbox_sha1sum(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property mbox_sha1sum can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._mbox_sha1sum = value

    @mbox_sha1sum.deleter
    def mbox_sha1sum(self):
        del self._mbox_sha1sum

    @property
    def openid(self):
        """Openid for Agent

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._openid

    @openid.setter
    def openid(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property openid can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._openid = value

    @openid.deleter
    def openid(self):
        del self._openid

    @property
    def account(self):
        """Account for Agent

        :setter: Tries to convert to :class:`tincan.AgentAccount`
        :setter type: :class:`tincan.AgentAccount`
        :rtype: :class:`tincan.AgentAccount`

        """
        return self._account

    @account.setter
    def account(self, value):
        if value is not None and not isinstance(value, AgentAccount):
            value = AgentAccount(value)
        self._account = value

    @account.deleter
    def account(self):
        del self._account
