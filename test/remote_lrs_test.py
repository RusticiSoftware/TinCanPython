import unittest
import uuid
from datetime import timedelta

from tincan.remote_lrs import RemoteLRS
from tincan.lrs_response import LRSResponse
from tincan.version import Version
from resources import lrs_properties
from tincan.activity import Activity
from tincan.activity_definition import ActivityDefinition
from tincan.languagemap import LanguageMap
from tincan.verb import Verb
from tincan.agent import Agent
from tincan.statement import Statement
from tincan.context import Context
from tincan.context_activities import ContextActivities
from tincan.score import Score
from tincan.result import Result
from tincan.substatement import SubStatement
from tincan.about import About
from tincan.statements_result import StatementsResult
from tincan.documement import (
    BaseDocument,
    StateDocument,
    ActivityProfileDocument,
    AgentProfileDocument
)


class RemoteLRSTest(unittest.TestCase):

    def __init__(self):
        self.endpoint = lrs_properties.endpoint
        self.version = lrs_properties.version
        self.username = lrs_properties.username
        self.password = lrs_properties.password
        self.lrs = RemoteLRS(
            self.version,
            self.endpoint,
            username=self.username,
            password=self.password
        )

        self.agent = Agent("mailto:tincanpython@tincanapi.com")
        self.verb = Verb(
            "http://adlnet.gov/expapi/verbs/experienced",
            LanguageMap({"en-US": "experienced"})
        )

        self.activity = Activity(
            "http://tincanapi.com/TinCanPython/Test/Unit/0",
            ActivityDefinition()
        )
        self.activity.type = "http://id.tincanapi.com/activitytype/unit-test"
        self.activity.definition.name(LanguageMap({"en-US": "Python Tests"}))
        self.activity.definition.description(LanguageMap(
            {"en-US": "Unit test in the test suite for the Python library"})
        )

        self.parent = Activity(
            "http://tincanapi.com/TinCanPython/Test",
            ActivityDefinition())
        self.activity.type = "http://id.tincanapi.com/activitytype/unit-test-suite"
        self.parent.definition.name(LanguageMap({"en-US": "Python Tests"}))
        self.parent.definition.description(LanguageMap(
            {"en-US": "Unit test in the test suite for the Python library"})
        )

        self.statement_ref = str(uuid.uuid4())

        self.context = Context(registration=uuid.uuid4(), statement=self.statement_ref)
        self.context.context_activities = ContextActivities(parent=[self.parent])

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
            duration=timedelta(seconds=120)
        )

        self.substatement = SubStatement(
            actor=self.agent,
            verb=self.verb,
            target=self.parent
        )

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instantiation(self):
        lrs = RemoteLRS()
        self.assertIsInstance(lrs, RemoteLRS)
        self.assertIsNone(lrs.get_endpoint())
        self.assertIsNone(lrs.get_auth())
        self.assertEqual(Version.latest, lrs.get_version())

    def test_about(self):
        response = self.lrs.about()

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, About)

    def test_about_failure(self):
        lrs = RemoteLRS(endpoint="http://cloud.scorm.com/tc/3TQLAI9/sandbox/")
        response = lrs.about()

        self.assertFalse(response.success)
        print "test_about_failure - errMsg: " + response.response.reason

    def test_save_statement(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.activity
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertEqual(statement, response.content)
        self.assertIsnotNone(response.content.id)

    def test_save_statement_with_id(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.activity,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertEqual(statement, response.content)

    def test_save_statement_ref(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.statement_ref,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertEqual(statement, response.content)

    def test_save_statement_substatement(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.substatement,
            id=str(uuid.uuid4())
        )
        response = self.lrs.save_statement(statement)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertEqual(statement, response.content)

    def test_save_statements(self):
        statement1 = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.parent
        )
        statement2 = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.activity,
            context=self.context
        )
        response = self.lrs.save_statements([statement1, statement2])

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.content[0].id)
        self.assertIsNotNone(response.content[1].id)
        self.assertEquals(statement1, response.content[0])
        self.assertEquals(statement2, response.content[1])

    def test_retrieve_statement(self):
        statement = Statement(
            actor=self.agent,
            verb=self.verb,
            target=self.activity,
            context=self.context,
            result=self.result,
            id=str(uuid.uuid4())
        )
        save_resp = self.lrs.save_statement(statement)

        if(save_resp.success):
            response = self.lrs.retrieve_statement(save_resp.content.id)
            self.assertIsInstance(response, LRSResponse)
            self.assertTrue(response.success)
            self.assertEquals(statement, response.content)
        else:
            print "test_retrieve_statement: save_statement failed"

    def test_query_statements(self):
        query = {
            "agent": self.agent,
            "verb": self.verb,
            "activity": self.parent,
            "related_activities": True,
            "related_agents": True,
            "format": "ids",
            "limit": 10
        }
        response = self.lrs.query_statements(query)

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, StatementsResult)

    def test_more_statements(self):
        query = {
            "format": "ids",
            "limit": 2
        }
        query_resp = self.lrs.query_statements(query)

        if query_resp.success and query_resp.content.more is not None:
            response = self.lrs.more_statements(query_resp.content)
            self.assertIsInstance(response, LRSResponse)
            self.assertTrue(response.success)
            self.assertIsInstance(response.content, StatementsResult)
        else:
            print "test_more_statements: query_statements failed or did not return a more url"

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

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RemoteLRSTest)
    unittest.TextTestRunner(verbosity=2).run(suite)