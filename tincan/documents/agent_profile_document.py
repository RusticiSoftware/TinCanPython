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
from tincan.documents import Document
from tincan.agent import Agent


class AgentProfileDocument(Document):
    """Extends Document with an Agent field, can be created from a dict, another Document, or from kwargs.

    :param id: The id of this document
    :type id: unicode
    :param content_type: The content_type of the content of this document
    :type content_type: unicode
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: unicode
    :param timestamp: The timestamp of this document
    :type timestamp: :mod:`datetime.datetime`
    :param agent: The agent object of this document
    :type agent: Agent
    """

    _props_req = list(Document._props_req)

    _props_req.extend([
        'agent',
    ])

    _props = list(Document._props)

    _props.extend(_props_req)

    @property
    def agent(self):
        """The Document's agent object

        :setter: Tries to convert to agent
        :setter type: :class:`tincan.agent.Agent`
        :rtype: :class:`tincan.agent.Agent`
        """
        return self._agent

    @agent.setter
    def agent(self, value):
        if not isinstance(value, Agent) and value is not None:
            try:
                value = Agent(value)
            except:
                raise TypeError(
                    "Property 'agent' in 'tincan.documents.%s' must be set with a type "
                    "that can be constructed into an Agent object." % self.__class__.__name__
                )
        self._agent = value
