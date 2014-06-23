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
from tincan.agent import Agent
from tincan.group import Group
from tincan.verb import Verb
from tincan.attachment import Attachment
from tincan.result import Result
from tincan.context import Context
from tincan.substatement import Substatement
from tincan.statement_ref import StatementRef
from tincan.activity import Activity

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

    def __init__(self, *args, **kwargs):
        self._attachments = []
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
        if value is not None:
            if not isinstance(value, unicode):
                value = unicode(value)
        self._id = value

    @id.deleter
    def id(self):
        del(self._id)

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
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Agent) and not isinstance(value, Group):
                if isinstance(value, list):
                    value = Group(member=value)
                else:
                    value = Agent(value)
            elif len(vars(value)) == 0:
                value = None
        self._actor = value

    @actor.deleter
    def actor(self):
        del(self._actor)

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
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Verb):
                value = Verb(value)
            elif len(vars(value)) == 0:
                value = None
        self._verb = value

    @verb.deleter
    def verb(self):
        del(self._verb)

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
            if not value:
                value = None
            elif not isinstance(value, Agent) and not isinstance(value, Group) and not isinstance(value, Substatement) and not isinstance(value, StatementRef) and not isinstance(value, Activity):
                if isinstance(value, list):
                    value = Group(member=value)
                else:
                    if isinstance(value, dict):
                        if value['object_type'] is not None:
                            if value['object_type'] == 'Agent':
                                value = Agent(value)
                            elif value['object_type'] == 'Substatement':
                                value = Substatement(value)
                            elif value['object_type'] == 'StatementRef':
                                value = StatementRef(value)
                            elif value['object_type'] == 'Activity':
                                value = Activity(value)
                            else:
                                raise ValueError('Object type is invalid')
                    else:
                        raise ValueError('Must set an object_type for the statement object')
            elif len(vars(value)) == 0:
                value = None
        self._object = value

    @object.deleter
    def object(self):
        del(self._object)

    #TODO: make timestamp and stored compatible with datetime and timedelta objects
    @property
    def timestamp(self):
        """Timestamp for Statement

		:setter: Tries to convert to unicode
		:setter type: unicode | :class:`datetime.datetime`
		:rtype: unicode

		"""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property mbox_sha1sum can not be set to an empty string")
            elif not isinstance(value, unicode):
                value = unicode(value)
        self._timestamp = value

    @timestamp.deleter
    def timestamp(self):
        del(self._timestamp)

    #TODO: make timestamp and stored compatible with datetime and timedelta objects
    @property
    def stored(self):
        """Stored for Statement

		:setter: Tries to convert to unicode
		:setter type: unicode | :class:`datetime.datetime`
		:rtype: unicode

		"""
        return self._stored

    @stored.setter
    def stored(self, value):

        if value is not None:
            if value == '':
                raise ValueError("Property mbox_sha1sum can not be set to an empty string")
            elif not isinstance(value, unicode):
                value = unicode(value)
        self._stored = value

    @stored.deleter
    def stored(self):
        del(self._stored)

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
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Agent):
                value = Agent(value)
            elif len(vars(value)) == 0:
                value = None
        self._authority = value

    @authority.deleter
    def authority(self):
        del(self._authority)

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
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Result):
                value = Result(value)
            elif len(vars(value)) == 0:
                value = None
        self._result = value

    @result.deleter
    def result(self):
        del(self._result)

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
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, Context):
                value = Context(value)
            elif len(vars(value)) == 0:
                value = None
        self._context = value

    @context.deleter
    def context(self):
        del(self._context)

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
                raise ValueError("Property mbox_sha1sum can not be set to an empty string")
            elif not isinstance(value, unicode):
                value = unicode(value)
        self._version = value

    @version.deleter
    def version(self):
        del(self._version)

    @property
    def attachments(self):
        """Attachments for Statement

		:setter: Tries to convert each element to Attachment
		:setter type: list[:mod:`tincan.attachment`]
		:rtype: list[:mod:`tincan.attachment`]

		"""
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        newmembers = []
        if value is not None:
            if isinstance(value, list):
                for k in value:
                    if not isinstance(k, Attachment):
                        newmembers.append(Attachment(k))
                    else:
                        newmembers.append(k)
            else:
                 self._attachments = list(value)
        value = newmembers
        self._attachments = value

    @attachments.deleter
    def attachments(self):
        del(self._attachments)