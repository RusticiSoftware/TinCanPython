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

    def __init__(self, jobj):
        """Instantiate the StatementsResult object

        :param jobj: JSON object that will be used to construct the object
        :type jobj: JSON object
        """
        content = json.load(object)
        if "more" in content and content["more"] is not None:
            self.more_url = content["more"]

        if "statements" in content and content["statements"] is not None:
            self.statements = []
            for s in content["statements"]:
                self.statements.append(s)
