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

"""
.. module:: statements_result
   :synopsis: Statements result model class, returned by LRS calls to get
              multiple statements.
"""


class StatementsResult(SerializableBase):
    """
    Statements result model class, returned by LRS calls to get
    multiple statements.

    Attributes:
    statements - a list containing partial results from the LRS
    query.
    more - If there are more results, a URL pointing to the
    rest. None otherwise.
    """

    _props_req = [
        'statements',
    ]

    _props = [
        'more',
    ]
    _props.extend(_props_req)

    @property
    def statements(self):
        return self._statements

    @statements.setter
    def statements(self, value):
        """Setter for the _statements attribute. Tries to convert to
        list of tincan.Statement.

        :param value: list of statements
        :type value: list[tincan.Statement] | None
        """

        if isinstance(value, list):
            self._statements = value
            return
        if value is None:
            self._statements = []
            return
        try:
            if isinstance(value, dict):
                raise Exception('Expected a list, got a dict: %s' % repr(value))

            self._statements = list(value)
        except Exception as e:
            msg = (
                "Property 'statements' in a 'tincan.%s' object must be set with a "
                "list or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)

    
    @property
    def more(self):
        return self._more

    @more.setter
    def more(self, value):
        """Setter for the _more attribute. Tries to convert to
        string.

        :param value: if statements is incomplete, a URI to get the rest
        :type value: str | unicode | None
        """
        if value is None or isinstance(value, basestring):
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

    @more.deleter
    def more(self):
        del self._more
