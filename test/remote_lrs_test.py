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

import unittest
import uuid
from datetime import datetime
from calendar import timegm
from pytz import utc

if __name__ == '__main__':
    from main import setup_tincan_path
    setup_tincan_path()
from tincan.remote_lrs import RemoteLRS
from tincan.lrs_response import LRSResponse
from tincan.version import Version
from resources import lrs_properties
from tincan.activity import Activity
from tincan.activity_definition import ActivityDefinition
from tincan.language_map import LanguageMap
from tincan.verb import Verb
from tincan.agent import Agent
from tincan.statement import Statement
from tincan.context import Context
from tincan.score import Score
from tincan.group import Group
from tincan.base import Base
from tincan.result import Result
from tincan.substatement import SubStatement
from tincan.statement_ref import StatementRef
from tincan.about import About
from tincan.statements_result import StatementsResult
from tincan.documents import (
    StateDocument,
    ActivityProfileDocument,
    AgentProfileDocument,
)


class RemoteLRSTest(unittest.TestCase):

    def setUp(self):
        self.endpoint = lrs_properties.endpoint
        self.version = lrs_properties.version
        self.username = lrs_properties.username
        self.password = lrs_properties.password
        self.lrs = RemoteLRS(
            version=self.version,
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
        )

        self.agent = Agent(mbox="mailto:tincanpython@tincanapi.com")
        self.agent2 = Agent(mbox="Agent2.mailto:tincanpython@tincanapi.com")
        self.verb = Verb(
            id="http://adlnet.gov/expapi/verbs/experienced",
            display=LanguageMap({"en-US": "experienced"})
        )

        self.group = Group(member=[self.agent, self.agent2])

        self.activity = Activity(
            id="http://tincanapi.com/TinCanPython/Test/Unit/0",
            definition=ActivityDefinition()
        )
        self.activity.definition.type = "http://id.tincanapi.com/activitytype/unit-test"
        self.activity.definition.name = LanguageMap({"en-US": "Python Tests"})
        self.activity.definition.description = LanguageMap(
            {"en-US": "Unit test in the test suite for the Python library"}
        )
        self.activity.object_type = 'Activity'

        self.parent = Activity(
            id="http://tincanapi.com/TinCanPython/Test",
            definition=ActivityDefinition())
        self.parent.definition.type = "http://id.tincanapi.com/activitytype/unit-test-suite"
        self.parent.definition.name = LanguageMap({"en-US": "Python Tests"})
        self.parent.definition.description = LanguageMap(
            {"en-US": "Unit test in the test suite for the Python library"}
        )
        self.parent.object_type = 'Activity'

        self.statement_ref = StatementRef(id=uuid.uuid4())

        self.context = Context(registration=uuid.uuid4(), statement=self.statement_ref)
        #self.context.context_activities = ContextActivities(parent=[self.parent])

        self.score = Score(
            raw=97,
            scaled=0.97,
            max=100,
            min=0
        )

        self.result = Result(
            score=self.score,
            success=True,
            completion=True,
            duration="PT120S"
        )

        self.substatement = SubStatement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity,
        )

    def tearDown(self):
        pass

    def test_instantiation(self):
        lrs = RemoteLRS()
        self.assertIsInstance(lrs, RemoteLRS)
        self.assertIsNone(lrs.endpoint)
        self.assertIsNone(lrs.auth)
        self.assertEqual(Version.latest, lrs.version)

    def test_about(self):
        response = self.lrs.about()

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, About)

    def test_about_failure(self):
        lrs = RemoteLRS(endpoint="http://cloud.scorm.com/tc/3TQLAI9/sandbox/")
        response = lrs.about()

        self.assertFalse(response.success)

    def test_save_statement(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.content.id)
        self._vars_verifier(statement, response.content, ['_authority', '_stored'])

    def test_save_statement_with_id(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(statement, response.content)

    def test_save_statement_conflict(self):
        test_id = unicode(uuid.uuid4())

        statement1 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.substatement,
            id=test_id
        )
        statement2 = Statement(
            actor=self.agent2,
            verb=self.verb,
            object=self.substatement,
            id=test_id
        )
        response = self.lrs.save_statement(statement1)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

        response = self.lrs.save_statement(statement2)

        self.assertIsInstance(response, LRSResponse)
        self.assertFalse(response.success)
        self.assertEquals(response.response.status, 409)

    def test_save_statement_ref(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.statement_ref,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(statement, response.content, ['_authority', '_stored'])

    def test_save_statement_group(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.group,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(statement, response.content)

    def test_save_statement_substatement(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.substatement,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(statement, response.content, ['_authority', '_stored'])

    def test_save_statements(self):
        statement1 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity
        )
        statement2 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity,
            context=self.context
        )
        response = self.lrs.save_statements([statement1, statement2])

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.content[0].id)
        self.assertIsNotNone(response.content[1].id)
        self._vars_verifier(statement1, response.content[0], ['_authority', '_stored'])
        self._vars_verifier(statement2, response.content[1], ['_authority', '_stored'])

    @unittest.skip("LRS truncates timestamps which makes returned statements evaluate not equal")
    def test_retrieve_statement(self):
        id_str = str(uuid.uuid4())
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity,
            context=self.context,
            result=self.result,
            id=id_str,
            version=Version.latest,
            timestamp=utc.localize(datetime.utcnow())
        )
        save_resp = self.lrs.save_statement(statement)

        self.assertTrue(save_resp.success)
        response = self.lrs.retrieve_statement(save_resp.content.id)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(response.content, statement, ['_authority', '_stored'])

    def test_retrieve_statement_no_microsecond(self):
        id_str = str(uuid.uuid4())
        dt = utc.localize(datetime.min)
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.activity,
            context=self.context,
            result=self.result,
            id=id_str,
            version=Version.latest,
            timestamp=dt
        )
        save_resp = self.lrs.save_statement(statement)

        self.assertTrue(save_resp.success)
        response = self.lrs.retrieve_statement(save_resp.content.id)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self._vars_verifier(response.content, statement, ['_authority', '_stored'])

    @unittest.skip("LRS truncates timestamps which makes returned statements evaluate not equal")
    def test_query_statements(self):
        tstamp = utc.localize(datetime.utcnow())
        s1 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s1)

        s2 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s2)

        s3 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s3)

        query = {
            "agent": self.agent,
            "verb": self.verb,
            "activity": self.parent,
            "related_activities": True,
            "related_agents": True,
            "limit": 2
        }
        response = self.lrs.query_statements(query)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, StatementsResult)
        self.assertTrue(hasattr(response.content, 'more'))
        self.assertIsNotNone(response.content.more)
        self._vars_verifier(s1, response.content.statements[0])
        self._vars_verifier(s2, response.content.statements[1])

    def test_query_statements_no_microsecond(self):
        tstamp = utc.localize(datetime.min)
        s1 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s1)

        s2 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s2)

        s3 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4()),
            timestamp=tstamp
        )
        self.lrs.save_statement(s3)

        query = {
            "agent": self.agent,
            "verb": self.verb,
            "activity": self.parent,
            "related_activities": True,
            "related_agents": True,
            "limit": 2
        }
        response = self.lrs.query_statements(query)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, StatementsResult)
        self.assertTrue(hasattr(response.content, 'more'))
        self.assertIsNotNone(response.content.more)
        self._vars_verifier(s1, response.content.statements[0])
        self._vars_verifier(s2, response.content.statements[1])

    def test_query_none(self):
        query = {
            "agent": self.agent,
            "verb": self.verb,
            "activity": self.parent,
            "related_activities": True,
            "related_agents": True,
            "format": "ids",
            "limit": 2,
            "registration": unicode(uuid.uuid4()),
        }
        response = self.lrs.query_statements(query)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, StatementsResult)
        self.assertTrue(hasattr(response.content, 'more'))
        self.assertTrue(hasattr(response.content, 'statements'))
        self.assertEquals(response.content.statements, [])

    def test_more_statements(self):
        s1 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4())
        )
        self.lrs.save_statement(s1)

        s2 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4())
        )
        self.lrs.save_statement(s2)

        s3 = Statement(
            actor=self.agent,
            verb=self.verb,
            object=self.parent,
            result=self.result,
            id=str(uuid.uuid4())
        )
        self.lrs.save_statement(s3)

        query = {
            "agent": self.agent,
            "verb": self.verb,
            "activity": self.parent,
            "related_activities": True,
            "related_agents": True,
            "format": "ids",
            "limit": 2
        }
        query_resp = self.lrs.query_statements(query)

        self.assertIsInstance(query_resp, LRSResponse)
        self.assertTrue(query_resp.success)
        self.assertIsNotNone(query_resp.content.more)

        response = self.lrs.more_statements(query_resp.content)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, StatementsResult)

    def test_retrieve_state_ids(self):
        response = self.lrs.retrieve_state_ids(activity=self.activity, agent=self.agent)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_retrieve_state(self):
        response = self.lrs.retrieve_state(
            activity=self.activity,
            agent=self.agent,
            state_id="test"
        )
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_save_state(self):
        doc = StateDocument(
            activity=self.activity,
            agent=self.agent,
            id="test",
            content=bytearray("Test value", encoding="utf-8")
        )
        response = self.lrs.save_state(doc)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_delete_state(self):
        doc = StateDocument(
            activity=self.activity,
            agent=self.agent,
            id="test"
        )
        response = self.lrs.delete_state(doc)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_clear_state(self):
        response = self.lrs.clear_state(activity=self.activity, agent=self.agent)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_retrieve_activity_profile_ids(self):
        response = self.lrs.retrieve_activity_profile_ids(activity=self.activity)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_retrieve_activity_profile(self):
        response = self.lrs.retrieve_activity_profile(activity=self.activity, profile_id="test")

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_save_activity_profile(self):
        doc = ActivityProfileDocument(
            activity=self.activity,
            id="test",
            content=bytearray("Test value", encoding="utf-8")
        )
        response = self.lrs.save_activity_profile(doc)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_delete_activity_profile(self):
        doc = ActivityProfileDocument(activity=self.activity, id="test")
        response = self.lrs.delete_activity_profile(doc)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_retrieve_agent_profile_ids(self):
        response = self.lrs.retrieve_agent_profile_ids(self.agent)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_retrieve_agent_profile(self):
        response = self.lrs.retrieve_agent_profile(agent=self.agent, profile_id="test")
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_save_agent_profile(self):
        doc = AgentProfileDocument(
            agent=self.agent,
            id="test",
            content=bytearray("Test value", encoding="utf-8")
        )
        response = self.lrs.save_agent_profile(doc)
        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def test_delete_agent_profile(self):
        doc = AgentProfileDocument(agent=self.agent, id="test")
        response = self.lrs.delete_agent_profile(doc)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

    def _vars_verifier(self, obj1, obj2, _ignored_attrs=['_authority', '_stored', '_id']):
        for k, v in vars(obj1).iteritems():
            if k in _ignored_attrs:
                continue
            elif isinstance(v, datetime):
                dt1 = getattr(obj1, k)
                dt2 = getattr(obj2, k)
                ts1 = timegm(dt1.timetuple())
                ts2 = timegm(dt2.timetuple())
                self.assertEqual(ts1, ts2)
                self.assertEqual(round(dt1.microsecond, 3), round(dt2.microsecond, 3))
            elif isinstance(v, Base):
                self._vars_verifier(getattr(obj1, k), getattr(obj2, k))
            else:
                self.assertEqual(getattr(obj1, k), getattr(obj2, k))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RemoteLRSTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
