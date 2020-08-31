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
        except Exception:
            raise TypeError(f"Property 'statements' in a 'tincan.{self.__class__.__name__}' object must be set with a "
                            f"list or None."
                            f"\n\n"
                            f"Tried to set it with a '{value.__class__.__name__}' object: {repr(value)}"
                            f"\n\n")


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
        if value is None or isinstance(value, str):
            self._more = value
            return
        try:
            self._more = str(value)
        except Exception as e:
            msg = (
                f"Property 'more' in a 'tincan.{self.__class__.__name__}' object must be set with a "
                f"str or None."
            )
            msg += repr(e)
            raise TypeError(msg) from e
