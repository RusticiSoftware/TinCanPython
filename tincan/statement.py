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

import uuid
import re
from datetime import datetime

from tincan.serializable_base import SerializableBase
from tincan.agent import Agent
from tincan.group import Group
from tincan.verb import Verb
from tincan.attachment import Attachment
from tincan.attachment_list import AttachmentList
from tincan.result import Result
from tincan.context import Context
from tincan.substatement import SubStatement
from tincan.statement_ref import StatementRef
from tincan.activity import Activity
from tincan.conversions.iso8601 import make_datetime

"""
.. module Statement
   :synopsis: A Statement object that contains all the information for one statement that is sent to an LRS
"""


class Statement(SerializableBase):

    _props_req = [
        "id",
        "actor",
        "verb",
        "object",
        "timestamp",
        "stored",
        "authority"
    ]

    _props = [
        "result",
        "context",
        "version",
        "attachments"
    ]

    _props.extend(_props_req)

    @property
    def id(self):
        """Id for Statement

        :setter: Tries to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, uuid.UUID):
            if isinstance(value, basestring) and not self._UUID_REGEX.match(value):
                raise ValueError("Invalid UUID string")
            value = uuid.UUID(value)
        self._id = value

    @id.deleter
    def id(self):
        del self._id

    @property
    def actor(self):
        """Actor for Statement

        :setter: Tries to convert to Agent or Group
        :setter type: :mod:`tincan.agent` | :mod:`tincan.group`
        :rtype: :mod:`tincan.agent` | :mod:`tincan.group`

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
        """Verb for Statement

        :setter: Tries to convert to Verb
        :setter type: :mod:`tincan.verb`
        :rtype: :mod:`tincan.verb`

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
    def object(self):
        """Object for Statement

        :setter: Sets the object
        :setter type: :mod:`tincan.agent` | :mod:`tincan.group` | :mod:`tincan.statement_ref` | :mod:`tincan.substatement` | :mod:`tincan.activity`
        :rtype: :mod:`tincan.agent` | :mod:`tincan.group` | :mod:`tincan.statement_ref` | :mod:`tincan.substatement` | :mod:`tincan.activity`

        """
        return self._object

    @object.setter
    def object(self, value):
        if value is not None:
            if not isinstance(value, Agent) and not isinstance(value, Group) and not isinstance(value, SubStatement) and not isinstance(value, StatementRef) and not isinstance(value, Activity):
                if isinstance(value, dict):
                    if 'object_type' in value or 'objectType' in value:
                        if 'objectType' in value:
                            value['object_type'] = value['objectType']
                            value.pop('objectType')
                        if value['object_type'] == 'Agent':
                            value = Agent(value)
                        elif value['object_type'] == 'SubStatement':
                            value = SubStatement(value)
                        elif value['object_type'] == 'StatementRef':
                            value = StatementRef(value)
                        elif value['object_type'] == 'Activity':
                            value = Activity(value)
                        elif value['object_type'] == 'Group':
                            value = Group(value)
                        else:
                            value = Activity(value)
                    else:
                        value = Activity(value)
        self._object = value

    @object.deleter
    def object(self):
        del self._object

    @property
    def timestamp(self):
        """Timestamp for Statement

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
    def stored(self):
        """Storage time. Tries to convert to :class:`datetime.datetime`.
        If no timezone is given, makes a naive `datetime.datetime`.

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
        return self._stored

    @stored.setter
    def stored(self, value):
        if value is None or isinstance(value, datetime):
            self._stored = value
            return

        try:
            self._stored = make_datetime(value)
        except TypeError as e:
            e.message = (
                "Property 'stored' in a 'tincan.%s' "
                "object must be set with a "
                "datetime.datetime, str, unicode, int, float, dict "
                "or None.\n\n%s" %
                (
                    self.__class__.__name__,
                    e.message,
                )
            )
            raise e

    @stored.deleter
    def stored(self):
        del self._stored

    @property
    def authority(self):
        """Authority for Statement

        :setter: Tries to convert to Agent
        :setter type: :mod:`tincan.agent`
        :rtype: :mod:`tincan.agent`

        """
        return self._authority

    @authority.setter
    def authority(self, value):
        if value is not None and not isinstance(value, Agent):
                value = Agent(value)
        self._authority = value

    @authority.deleter
    def authority(self):
        del self._authority

    @property
    def result(self):
        """Result for Statement

        :setter: Tries to convert to Result
        :setter type: :mod:`tincan.result`
        :rtype: :mod:`tincan.result`

        """
        return self._result

    @result.setter
    def result(self, value):
        if value is not None and not isinstance(value, Result):
                value = Result(value)
        self._result = value

    @result.deleter
    def result(self):
        del self._result

    @property
    def context(self):
        """Context for Statement

        :setter: Tries to convert to Context
        :setter type: :mod:`tincan.context`
        :rtype: :mod:`tincan.context`

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
    def version(self):
        """Version for Statement

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._version

    @version.setter
    def version(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property version can not be set to an empty string")
            elif not isinstance(value, unicode):
                value = unicode(value)
        self._version = value

    @version.deleter
    def version(self):
        del self._version

    @property
    def attachments(self):
        """Attachments for Statement

        :setter: Tries to convert each element to Attachment
        :setter type: :mod:`tincan.attachment_list`
        :rtype: :mod:`tincan.attachment_list`

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
