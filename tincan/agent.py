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
from tincan.agent_account import AgentAccount

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
        """

        :param name: The name of this agent
        :type name: str
        :param mbox: The mailto address for this agent
        :type mbox: str
        :param mbox_sha1sum: The sha1sum of the mbox of this agent
        :type mbox_sha1sum: str
        :param openid: The openid for this agent
        :type openid: str
        :param account: The alternative account for this agent (e.g. a Twitter handle)
        :type account: :mod:`tincan.agentaccount`
        :param object_type: The object type for this agent. Defaults to "Agent"
        :type object_type: str

        """

        super(Agent, self).__init__(*args, **kwargs)

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        """Setter for the _object_type attribute. Tries to convert to string.
        
        :param value: The agent's object_type
        :type value: str
        
        """
        newtype = "Agent"
        if value is not None:
            if not isinstance(value, basestring):
                newtype = str(value)
            elif value == '':
                raise ValueError("Property object_type can not be set to an empty string")
            else: newtype = value
        self._object_type = newtype

    @object_type.deleter
    def object_type(self):
        del self._object_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Setter for the _name attribute. Tries to convert to string.

        :param value: The agent's name
        :type value: str
        
        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property name can not be set to an empty string")
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def mbox(self):
        return self._mbox

    @mbox.setter
    def mbox(self, value):
        """Setter for the _mbox attribute. Tries to convert to string.

        :param value: The agent's mbox
        :type value: str
        
        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property mbox can not be set to an empty string")
        if not value.startswith("mailto:"):
            value = "mailto:" + value
        self._mbox = value

    @mbox.deleter
    def mbox(self):
        del self._mbox

    @property
    def mbox_sha1sum(self):
        return self._mbox_sha1sum

    @mbox_sha1sum.setter
    def mbox_sha1sum(self, value):
        """Setter for the _mbox_sha1sum attribute. Tries to convert to string.

        :param value: The agent's mbox_sha1sum
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property mbox_sha1sum can not be set to an empty string")
        self._mbox_sha1sum = value

    @mbox_sha1sum.deleter
    def mbox_sha1sum(self):
        del self._mbox_sha1sum

    @property
    def openid(self):
        return self._openid

    @openid.setter
    def openid(self, value):
        """Setter for the _openid attribute. Tries to convert to string.

        :param value: The agent's openid
        :type value: str
        
        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property openid can not be set to an empty string")
        self._openid = value

    @openid.deleter
    def openid(self):
        del self._openid

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        """Setter for the _account attribute. Tries to convert to :mod:`tincan.AgentAccount`

        :param value: The agent's account
        :type value: :mod:`tincan.AgentAccount`

        """
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, AgentAccount):
                value = AgentAccount(value)
            elif len(vars(value)) == 0:
                value = None
        self._account = value

    @account.deleter
    def account(self):
        del self._account
