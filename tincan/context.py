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

import uuid
import re

from tincan.serializable_base import SerializableBase
from tincan.group import Group
from tincan.agent import Agent
from tincan.extensions import Extensions
from tincan.context_activities import ContextActivities
from tincan.statement_ref import StatementRef


"""
.. module:: context
   :synopsis: A context object that provides contextual information
   about a statement

"""


class Context(SerializableBase):
    _LANG_REGEX = re.compile(
        '^(((([A-Za-z]{2,3}(-([A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-([A-Za-z]{4}))?(-([A-Za-z]'
        '{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-([0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(x(-[A-Z'
        'a-z0-9]{1,8})+))?)|(x(-[A-Za-z0-9]{1,8})+)|((en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|'
        'i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE)|(art-lojban|cel-gaulish|no-bok|no-nyn|'
        'zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang)))$')

    _props = [
        'registration',
        'instructor',
        'team',
        'context_activities',
        'revision',
        'platform',
        'language',
        'statement',
        'extensions'
    ]

    def __init__(self, *args, **kwargs):
        self._registration = None
        self._instructor = None
        self._team = None
        self._context_activities = None
        self._revision = None
        self._platform = None
        self._language = None
        self._statement = None
        self._extensions = None

        super(Context, self).__init__(*args, **kwargs)

    @property
    def registration(self):
        """Registration for Context

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._registration

    @registration.setter
    def registration(self, value):
        if value is not None and not isinstance(value, uuid.UUID):
            if isinstance(value, str) and not self._UUID_REGEX.match(value):
                raise ValueError("Invalid UUID string")
            value = uuid.UUID(value)
        self._registration = value

    @registration.deleter
    def registration(self):
        del self._registration

    @property
    def instructor(self):
        """Instructor for Context

        :setter: Tries to convert to :class:`tincan.Agent` or :class:`tincan.Group`
        :setter type: :class:`tincan.Agent` | :class:`tincan.Group`
        :rtype: :class:`tincan.Agent` | :class:`tincan.Group`

        """
        return self._instructor

    @instructor.setter
    def instructor(self, value):
        if value is not None and not isinstance(value, Group) and not isinstance(value, Agent):
            try:
                value = Agent(value)
            except (TypeError, AttributeError):
                value = Group(value)
        self._instructor = value

    @instructor.deleter
    def instructor(self):
        del self._instructor

    @property
    def team(self):
        """Team for Context

        :setter: Tries to convert to :class:`tincan.Group`
        :setter type: :class:`tincan.Group`
        :rtype: :class:`tincan.Group`

        """
        return self._team

    @team.setter
    def team(self, value):
        if value is not None and not isinstance(value, Group):
            value = Group(value)
        self._team = value

    @team.deleter
    def team(self):
        del self._team

    @property
    def context_activities(self):
        """Context Activities for Context

        :setter: Tries to convert to :class:`tincan.ContextActivities`
        :setter type: :class:`tincan.ContextActivities`
        :rtype: :class:`tincan.ContextActivities`

        """
        return self._context_activities

    @context_activities.setter
    def context_activities(self, value):
        if value is not None and not isinstance(value, ContextActivities):
            value = ContextActivities(value)
        self._context_activities = value

    @context_activities.deleter
    def context_activities(self):
        del self._context_activities

    @property
    def revision(self):
        """Revision for Context

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._revision

    @revision.setter
    def revision(self, value):
        if value is not None and not isinstance(value, str):
            value = str(value)
        self._revision = value

    @revision.deleter
    def revision(self):
        del self._revision

    @property
    def platform(self):
        """Platform for Context

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._platform

    @platform.setter
    def platform(self, value):
        if value is not None and not isinstance(value, str):
            value = str(value)
        self._platform = value

    @platform.deleter
    def platform(self):
        del self._platform

    @property
    def language(self):
        """Language for Context

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._language

    @language.setter
    def language(self, value):
        if value is not None:
            if not isinstance(value, str):
                value = str(value)
            if not self._LANG_REGEX.match(value):
                raise ValueError("invalid regional identifier")
        self._language = value

    @language.deleter
    def language(self):
        del self._language

    @property
    def statement(self):
        """Statement for Context

        :setter: Tries to convert to :class:`tincan.StatementRef`
        :setter type: :class:`tincan.StatementRef`
        :rtype: :class:`tincan.StatementRef`

        """
        return self._statement

    @statement.setter
    def statement(self, value):
        if value is not None and not isinstance(value, StatementRef):
            value = StatementRef(value)
        self._statement = value

    @statement.deleter
    def statement(self):
        del self._statement

    @property
    def extensions(self):
        """Extensions for Context

        :setter: Tries to convert to :class:`tincan.Extensions`
        :setter type: :class:`tincan.Extensions`
        :rtype: :class:`tincan.Extensions`

        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if value is not None and not isinstance(value, Extensions):
            value = Extensions(value)
        self._extensions = value

    @extensions.deleter
    def extensions(self):
        del self._extensions
