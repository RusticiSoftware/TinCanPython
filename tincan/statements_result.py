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
from six import string_types

from tincan.serializable_base import SerializableBase
from tincan.statement_list import StatementList

"""
.. module:: statements_result
   :synopsis: Statements result model class, returned by LRS calls to get
              multiple statements.
"""


class StatementsResult(SerializableBase):
    _props_req = [
        'statements',
        'more',
    ]

    _props = []
    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._statements = None
        self._more = None

        super(StatementsResult, self).__init__(*args, **kwargs)

    @property
    def statements(self):
        """Statements for StatementsResult

        :setter: Tries to convert each element to :class:`tincan.Statement`
        :setter type: list of :class:`tincan.Statement`
        :rtype: list of :class:`tincan.Statement`

        """
        return self._statements

    @statements.setter
    def statements(self, value):
        if value is None:
            self._statements = StatementList()
            return
        try:
            self._statements = StatementList(value)
        except Exception as e:
            msg = (
                "Property 'statements' in a 'tincan.%s' object must be set with a "
                "list or None."
                "\n\n"
                "Tried to set it with a '%s' object: %s"
                "\n\n" %
                (
                    self.__class__.__name__,
                    value.__class__.__name__,
                    repr(value),
                )
            )
            msg += e.message
            raise TypeError(msg)

    @property
    def more(self):
        """More for StatementsResult

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._more

    @more.setter
    def more(self, value):
        if value is None or isinstance(value, string_types):
            self._more = value
            return
        try:
            self._more = str(value)
        except Exception as e:
            msg = (
                "Property 'more' in a 'tincan.%s' object must be set with a "
                "str or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)
