#!/usr/bin/env python

from tincan.base import Base


class StatementsResult(Base):
    """
    Statements result model class, returned by LRS calls to get
    multiple statements.

    Attributes:
    statements - a list containing partial results from the LRS
    query.
    more - If there are more results, a URL pointing to the
    rest. None otherwise.
    """

    _props = [
        'statements',
        'more',
    ]

    @property
    def statements(self):
        return self._statements

    @statements.setter
    def statements(self, value):
        if value is None or isinstance(value, list):
            self._statements = value
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

    @statements.deleter
    def statements(self):
        del self._statements
        
    
    @property
    def more(self):
        return self._more

    @more.setter
    def more(self, value):
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
