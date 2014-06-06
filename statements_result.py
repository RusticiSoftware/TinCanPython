#!/usr/bin/env python

from datetime import datetime

import json


class StatementsResult(object):
    """
    Statements result model class, returned by LRS calls to get multiple statements
    """
    def __init__(self, json_str):
        self.statements = []

        root = json.loads(json_str)
        statements_node = root.get('statements')
        if statements_node is not None:
            self.statements.extend(statements_node)

        self.more = root.get('more')
