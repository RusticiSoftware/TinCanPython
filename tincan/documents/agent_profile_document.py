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
from document import Document
from tincan.agent import Agent


class AgentProfileDocument(Document):
    """Extends Document with an Agent field, can be created from a dict, another Document, or from kwargs.

    :param id: The id of this document
    :type id: str
    :param content_type: The content_type of the content of this document
    :type content_type: str
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: str
    :param time_stamp: The time stamp of this document
    :type time_stamp: str
    :param agent: The agent object of this document
    :type agent: Agent
    """

    _properties = list(Document._properties)

    _properties.extend([
        "agent",
    ])

    @property
    def agent(self):
        return self._agent

    @agent.setter
    def agent(self, value):
        """Setter for the _agent attribute

        :param value: Desired object for the document's agent
        :type value: Agent
        """
        if not isinstance(value, Agent):
            try:
                value = Agent(value)
            except:
                raise TypeError(
                    "Property 'agent' in 'tincan.%s' must be set with a type "
                    "that can be constructed into an Agent object." % self.__class__.__name__
                )
        self._agent = value

    @agent.deleter
    def agent(self, value):
        del self._agent