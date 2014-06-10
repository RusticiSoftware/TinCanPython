#!/usr/bin/env python

import unittest

## TODO: re-enable this
# from tincan.agent import Agent, AgentAccount
from tincan.version import Version


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
        tested_versions = [version] if version is not None else Version.supported
        for version in tested_versions:
            constructor = obj.__class__.from_json
            json_obj = obj.to_json(version)
            clone = constructor(json_obj)

            self.assertEqual(obj.__class__, clone.__class__)

            if isinstance(obj, dict):
                orig_dict = obj
                clone_dict = clone
            else:
                orig_dict = obj.__dict__
                clone_dict = clone.__dict__

            self.assertEqual(orig_dict, clone_dict)

