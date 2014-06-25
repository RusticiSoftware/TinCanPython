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

from datetime import datetime
from tincan.serializable_base import SerializableBase
from tincan.agent import Agent
from tincan.group import Group
from tincan.verb import Verb
from tincan.context import Context
from tincan.attachment import Attachment
from tincan.attachment_list import AttachmentList
from tincan.conversions.iso8601 import make_datetime

"""

.. module:: StatementBase
   :synopsis: The base object for both Statement and SubStatement

"""

class StatementBase(SerializableBase):

    _props_req = [
        'actor',
        'verb',
        'object',
        'timestamp',
    ]

    _props = [
        'context',
        'attachments'
    ]

    _props.extend(_props_req)

    @property
    def actor(self):
        """Actor for StatementBase

        :setter: Tries to convert to Agent or Group
        :setter type: :class:`tincan.agent.Agent` | :class:`tincan.group.Group`
        :rtype: :class:`tincan.agent.Agent` | :class:`tincan.group.Group`

        """
        return self._actor

    @actor.setter
    def actor(self, value):
        if value is not None and not isinstance(value, Agent) and not isinstance(value, Group):
            if isinstance(value, dict):
                if 'object_type' in value or 'objectType' in value:
                    if 'objectType' in value:
                        value['object_type'] = value['objectType']
                        value.pop('objectType')
                    if value['object_type'] == 'Agent':
                        value = Agent(value)
                    elif value['object_type'] == 'Group':
                        value = Group(value)
                    else:
                        value = Agent(value)
                else:
                    value = Agent(value)
        self._actor = value

    @actor.deleter
    def actor(self):
        del self._actor

    @property
    def verb(self):
        """Verb for StatementBase

        :setter: Tries to convert to Verb
        :setter type: :class:`tincan.verb.Verb`
        :rtype: :class:`tincan.verb.Verb`

        """
        return self._verb

    @verb.setter
    def verb(self, value):
        if value is not None and not isinstance(value, Verb):
                value = Verb(value)
        self._verb = value

    @verb.deleter
    def verb(self):
        del self._verb

    @property
    def timestamp(self):
        """Timestamp for StatementBase

        :setter: Tries to convert to :class:`datetime.datetime`. If
        no timezone is given, makes a naive `datetime.datetime`.

        Strings will be parsed as ISO 8601 timestamps.

        If a number is provided, it will be interpreted as a UNIX
        timestamp, which by definition is UTC.

        If a `dict` is provided, does `datetime.datetime(**value)`.

        If a `tuple` or a `list` is provided, does
        `datetime.datetime(*value)`. Uses the timezone in the tuple or
        list if provided.

        :setter type: :class:`datetime.datetime` | unicode | str | int | float | dict | tuple | list | None
        :rtype: :class:`datetime.datetime`
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if value is None or isinstance(value, datetime):
            self._timestamp = value
            return

        try:
            self._timestamp = make_datetime(value)
        except TypeError as e:
            e.message = (
                "Property 'timestamp' in a 'tincan.%s' "
                "object must be set with a "
                "datetime.datetime, str, unicode, int, float, dict "
                "or None.\n\n%s" %
                (
                    self.__class__.__name__,
                    e.message,
                )
            )
            raise e

    @timestamp.deleter
    def timestamp(self):
        del self._timestamp

    @property
    def context(self):
        """Context for StatementBase

        :setter: Tries to convert to Context
        :setter type: :class:`tincan.context.Context`
        :rtype: :class:`tincan.context.Context`

        """
        return self._context

    @context.setter
    def context(self, value):
        if value is not None and not isinstance(value, Context):
                value = Context(value)
        self._context = value

    @context.deleter
    def context(self):
        del self._context

    @property
    def attachments(self):
        """Attachments for StatementBase

        :setter: Tries to convert each element to Attachment
        :setter type: :class:`tincan.attachment_list.AttachmentList`
        :rtype: :class:`tincan.attachment_list.AttachmentList`

        """
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        if value is not None and not isinstance(value, AttachmentList):
            try:
                value = AttachmentList([Attachment(value)])
            except (TypeError, AttributeError):
                value = AttachmentList(value)
        self._attachments = value

    @attachments.deleter
    def attachments(self):
        del self._attachments