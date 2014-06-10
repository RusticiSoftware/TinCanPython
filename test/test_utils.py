#!/usr/bin/env python

import unittest
import json

## TODO: re-enable this
# from TinCanPython.agent import Agent, AgentAccount
from TinCanPython.tcapi_version import TCAPIVersion


class TinCanBaseTestCase(unittest.TestCase):
    ## TODO: re-enable this
    # def get_agent(self, name, id_type, id_fields):
    #     agent = Agent()
    #     agent.name = name
    #
    #     if 'mbox' == id_type:
    #         agent.mbox = id_fields
    #     elif 'openid' == id_type:
    #         agent.openid = id_fields
    #     elif 'mbox_sha1sum' == id_type:
    #         agent.mbox_sha1sum = id_fields
    #     elif 'account' == id_type:
    #         parts = id_fields.split('|')
    #         acct = AgentAccount()
    #         acct.home_page = parts[0]
    #         acct.name = parts[1]
    #         agent.account = acct
    #
    #     return agent

    # PEP8 says this should be lowercase, but unittest breaks this rule
    def assertSerializeDeserialize(self, obj, version=None):
        """
        Verifies that objects are packed to JSON and unpacked
        correctly for the version specified. If no version is
        specified, tests for all versions in TCAPIVersion.
        :param obj: A TinCan object to be tested.
        :param version: The version according to whose schema we will test.
        :type version: str
        """
        tested_versions = [version] if version is not None else TCAPIVersion.values()
        for version in tested_versions:
            json_obj = obj.to_json(version)
            constructor = obj.__class__ if not isinstance(obj, dict) else dict
            unpacked_json = json.loads(json_obj)
            clone = constructor(**unpacked_json)

            self.assertEqual(isinstance(obj, dict), isinstance(clone, dict))

            orig_dict = obj if isinstance(obj, dict) else obj.__dict__
            clone_dict = clone if isinstance(clone, dict) else clone.__dict__

            self.assertEqual(orig_dict, clone_dict)
