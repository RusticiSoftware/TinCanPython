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
from tincan.activity import Activity
import uuid


class StateDocument(Document):
    """Extends Document with Agent, Activity, and Registration fields; can be created from a dict, another Document, or from kwargs.

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
    :param activity: The activity object of this document
    :type activity: Activity
    :param registration: The registration id of the state for this document
    :type registration: str
    """

    _properties = list(Document._properties)

    _properties.extend([
        "agent",
        "activity",
        "registration",
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

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, value):
        """Setter for the _activity attribute

        :param value: Desired object for the document's activity
        :type value: Activity
        """
        if not isinstance(value, Activity):
            try:
                value = Activity(value)
            except:
                raise TypeError(
                    "Property 'activity' in 'tincan.%s' must be set with a type "
                    "that can be constructed into an Activity object." % self.__class__.__name__
                )
        self._activity = value

    @activity.deleter
    def activity(self, value):
        del self._activity

    @property
    def registration(self):
        return self._registration

    @registration.setter
    def registration(self, value):
        """Setter for the _registration attribute

        :param value: Desired value for the document's registration id
        :type value: str | uuid.UUID
        """
        if isinstance(value, uuid.UUID):
            str(value)
        elif value is not None and not isinstance(value, basestring):
            raise TypeError("registration can only be set with a str or UUID")

        self._registration = value

    @registration.deleter
    def registration(self):
        del self._registration