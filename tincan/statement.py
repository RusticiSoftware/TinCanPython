# Copyright 2014 Rustici Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

from tincan.statement_base import StatementBase
from tincan.agent import Agent
from tincan.group import Group
from tincan.result import Result
from tincan.substatement import SubStatement
from tincan.statement_ref import StatementRef
from tincan.activity import Activity
from tincan.conversions.iso8601 import make_datetime
from tincan.version import Version


"""
.. module Statement
   :synopsis: A Statement object that contains all the information for one statement that is sent to an LRS
"""


class Statement(StatementBase):
    _UUID_REGEX = re.compile(
        r'^[a-f0-9]{8}-'
        r'[a-f0-9]{4}-'
        r'[1-5][a-f0-9]{3}-'
        r'[89ab][a-f0-9]{3}-'
        r'[a-f0-9]{12}$'
    )

    _props_req = [
        "id",
        "stored",
        "authority"
    ]

    _props = [
        "result",
        "version"
    ]

    _props.extend(StatementBase._props)
    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._id = None
        self._stored = None
        self._authority = None
        self._result = None
        self._version = Version.latest

        super(Statement, self).__init__(*args, **kwargs)

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
            if isinstance(value, str) and not self._UUID_REGEX.match(value):
                raise ValueError("Invalid UUID string")
            value = uuid.UUID(value)
        self._id = value

    @id.deleter
    def id(self):
        del self._id

    @property
    def object(self):
        """Object for Statement

        :setter: Sets the object
        :setter type: :class:`tincan.Agent` | :class:`tincan.Group` | :class:`tincan.StatementRef` |
                      :class:`tincan.SubStatement` | :class:`tincan.Activity`
        :rtype: :class:`tincan.Agent` | :class:`tincan.Group` | :class:`tincan.StatementRef` |
                :class:`tincan.SubStatement` | :class:`tincan.Activity`

        """
        return self._object

    @object.setter
    def object(self, value):
        if value is not None:
            if not isinstance(value, Agent) and \
                    not isinstance(value, Group) and \
                    not isinstance(value, SubStatement) and \
                    not isinstance(value, StatementRef) and \
                    not isinstance(value, Activity):
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

        :setter: Tries to convert to :class:`tincan.Agent`
        :setter type: :class:`tincan.Agent`
        :rtype: :class:`tincan.Agent`

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

        :setter: Tries to convert to :class:`tincan.Result`
        :setter type: :class:`tincan.Result`
        :rtype: :class:`tincan.Result`

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
            elif not isinstance(value, str):
                value = str(value)
        self._version = value

    @version.deleter
    def version(self):
        del self._version
