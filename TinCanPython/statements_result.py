#!/usr/bin/env python

from TinCanPython.tincanbase import TinCanBaseObject


class StatementsResult(TinCanBaseObject):
    """
    Statements result model class, returned by LRS calls to get
    multiple statements.

    Attributes:
     * ``statements`` - a list containing partial results from the LRS
    query.
     * ``more`` - If there are more results, a URL pointing to the
     rest. None otherwise.
    """

    def __init__(self, statements, more=None):
        """
        :param statements: list of partial results from the LRS
        :type statements: list
        :param more: If there are more results, a URL pointing to the
        rest. None otherwise.
        :type more: str
        """
        self.statements = statements
        self.more = more
