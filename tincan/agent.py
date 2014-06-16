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
from tincan.agent_account import AgentAccount

class Agent(SerializableBase):
    _props_req = [
        "objecttype"
    ]

    _props = [
        "name",
        "mbox",
        "mboxsha1sum",
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
        :param mboxsha1sum: The sha1sum of the mbox of this agent
        :type mboxsha1sum: str
        :param openid: The openid for this agent
        :type openid: str
        :param account: The alternative account for this agent (e.g. a Twitter handle)
        :type account: :mod:`tincan.agentaccount`
        :param objecttype: The object type for this agent. Defaults to "Agent"
        :type objecttype: str

        """

        super(Agent, self).__init__(*args, **kwargs)

    @property
    def objecttype(self):
        return self._objecttype

    @objecttype.setter
    def objecttype(self, value):
        """Setter for the _objecttype attribute. Tries to convert to string.
        
        :param value: The agent's objecttype
        :type value: str
        
        """
        newtype = "Agent"
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value is '':
                raise ValueError("Property objecttype can not be set to an empty string")
            else: newtype = value
        self._objecttype = newtype

    @objecttype.deleter
    def objecttype(self):
        del self._objecttype

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
            elif value is '':
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
            elif value is '':
                raise ValueError("Property mbox can not be set to an empty string")
        if not value.startswith("mailto:"):
            value = "mailto:" + value
        self._mbox = value

    @mbox.deleter
    def mbox(self):
        del self._mbox

    @property
    def mboxsha1sum(self):
        return self._mboxsha1sum

    @mboxsha1sum.setter
    def mboxsha1sum(self, value):
        """Setter for the _mboxsha1sum attribute. Tries to convert to string.

        :param value: The agent's mboxsha1sum
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value is '':
                raise ValueError("Property mboxsha1sum can not be set to an empty string")
        self._mboxsha1sum = value

    @mboxsha1sum.deleter
    def mboxsha1sum(self):
        del self._mboxsha1sum

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
            elif value is '':
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