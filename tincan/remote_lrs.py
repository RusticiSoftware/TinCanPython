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

import httplib
import urllib
import json
import base64

from tincanbase import IgnoreNoneEncoder
from urlparse import urlparse
from lrs_response import LRSResponse
from http_request import HTTPRequest
from agent import Agent
from statement import Statement
from activity import Activity
from statements_result import StatementsResult
from about import About
from version import Version
from tincan.documents import (
    Document,
    StateDocument,
    ActivityProfileDocument,
    AgentProfileDocument
)

"""
.. module:: remote_lrs
   :synopsis: The RemoteLRS class implements LRS communication.
"""


class RemoteLRS(object):

    def __init__(self, version=Version.latest, endpoint=None, username=None, password=None, auth=None):
        """RemoteLRS Constructor

        :param endpoint: lrs endpoint
        :type endpoint: str
        :param version: Version used for lrs communication
        :type version: str
        :param username: username for lrs
        :type username: str
        :param password: password for lrs
        :type password: str
        :param auth: Authentication object
        :type auth: dict
        """
        self.set_version(version)
        if endpoint is not None:
            self.set_endpoint(endpoint)
        if auth is not None or (username is not None and password is not None):
            self.set_auth(auth, username, password)

    def send_request(self, request):
        """Establishes connection and returns http response based off of request.

        :param request: HTTPRequest object
        :type request: :mod:tincan.http_request`
        :returns: LRS Response object
        :rtype: :mod:`tincan.lrs_response`
        """

        if "http" in request.resource:
            url = request.resource
        else:
            url = self._endpoint
            url += request.resource

        headers = {"X-Experience-API-Version": self._version}

        if self._auth is not None:
            headers["Authorization"] = self._auth

        headers.update(request.headers)

        params = request.query_params
        params = {k: unicode(params[k]).encode('utf-8') for k in params.keys()}
        params = urllib.urlencode(params)

        parsed = urlparse(url)

        if parsed.scheme == "https":
            web_req = httplib.HTTPSConnection(parsed.hostname, parsed.port)
        else:
            web_req = httplib.HTTPConnection(parsed.hostname, parsed.port)

        path = parsed.path
        if params:
            path += "?" + params

        web_req.request(request.method, path, headers)

        if request.content is not None:
            web_req.send(request.content)

        response = web_req.getresponse()

        web_req.close()

        if (200 <= response.status < 300) or (response.status == 404 and request.ignore404):
            success = True
        else:
            success = False

        return LRSResponse(success, request, response)

    def about(self):
        """Gets about response from LRS

        :return: LRS Response object with the returned LRS about object as content
        :rtype: :mod:`tincan.lrs_response`
        """
        request = HTTPRequest(self._endpoint, "GET", "about")
        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = About.from_json(lrs_response.response.read())

        return lrs_response

    def save_statement(self, statement):
        """Save statement to LRS and update statement id if necessary

        :param statement: Statement object to be saved
        :type statement: Statement
        :return: LRS Response object with the saved statement as content
        :rtype: :mod:`tincan.lrs_response`
        """
        if not isinstance(statement, Statement):
            statement = Statement(statement)

        request = HTTPRequest(self._endpoint, "POST", "statements")

        if statement.id is not None:
            request.method = "PUT"
            request.query_params["statementId"] = statement.id

        request.headers["Content-Type"] = "application/json"
        request.content = statement.as_version(self._version)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            if statement.id is None:
                statement.id = json.load(lrs_response.response.read())[0]
            lrs_response.content = statement

        return lrs_response

    def save_statements(self, statements):
        """Save statements to LRS and update their statement id's

        :param statements: A list of statement objects to be saved
        :type statements: list
        :return: LRS Response object with the saved list of statements as content
        :rtype: :mod:`tincan.lrs_response`
        """
        def make_statement(s):
            return s if isinstance(s, Statement) else Statement(s)

        statements = [make_statement(s) for s in statements]

        request = HTTPRequest(self._endpoint, "POST", "statements")
        request.headers["Content-Type"] = "application/json"

        request.content = json.dump([s.as_version(self._version) for s in statements], cls=IgnoreNoneEncoder)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            id_list = json.load(lrs_response.response.read())
            for s, id in zip(statements, id_list):
                s.id = id

            lrs_response.content = statements

        return lrs_response

    def retrieve_statement(self, statement_id):
        """Retrieve a statement from the server from its id

        :param statement_id: The UUID of the desired statement
        :type statement_id: str
        :return: LRS Response object with the retrieved statement as content
        :rtype: :mod:`tincan.lrs_response`
        """
        request = HTTPRequest(self._endpoint, "GET", "statements")
        request.query_params["statementId"] = statement_id

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = Statement.from_json(lrs_response.response.read())

        return lrs_response

    def retrieve_voided_statement(self, statement_id):
        """Retrieve a voided statement from the server from its id

        :param statement_id: The UUID of the desired voided statement
        :type statement_id: str
        :return: LRS Response object with the retrieved voided statement as content
        :rtype: :mod:`tincan.lrs_response`
        """
        request = HTTPRequest(self._endpoint, "GET", "statements")
        request.query_params["voidedStatementId"] = statement_id

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = Statement.from_json(lrs_response.response.read())

        return lrs_response

    def query_statements(self, query):
        """Query the LRS for statements with specified parameters

        :param query: Dictionary of query parameters and their values
        :type query: dict
        :return: LRS Response object with the returned StatementsResult object as content
        :rtype: :mod:`tincan.lrs_response`
        """
        params = {}

        param_keys = [
            "registration",
            "since",
            "until",
            "limit",
            "ascending",
            "related_activities",
            "related_agents",
            "format",
            "attachments",
        ]

        for k, v in query.iteritems():
            if v is not None:
                if k == "agent":
                    params[k] = v.as_version(self._version)
                elif k == "verb" or k == "activity":
                    params[k] = v.id
                elif k in param_keys:
                    params[k] = v

        request = HTTPRequest(self._endpoint, "GET", "statements")
        request.query_params = params

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult.from_json(lrs_response.response.read())

        return lrs_response

    def more_statements(self, more_url):
        """Query the LRS for more statements

        :param more_url: URL from a StatementsResult object used to retrieve more statements
        :type more_url: str
        :return: LRS Response object with the returned StatementsResult object as content
        :rtype: :mod:`tincan.lrs_response`
        """
        if isinstance(more_url, StatementsResult):
            more_url = more_url.more

        more_url = self.get_endpoint_server_root() + more_url

        request = HTTPRequest(self._endpoint, "GET", more_url)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult(lrs_response.response.read())

        return lrs_response

    def retrieve_state_ids(self, activity, agent, registration=None, since=None):
        """Retrieve state id's from the LRS with the provided parameters

        :param activity: Activity object of desired states
        :type activity: :mod:`tincan.activity`
        :param agent: Agent object of desired states
        :type agent: :mod:`tincan.agent`
        :param registration: Registration UUID of desired states
        :type registration: str
        :param since: Retrieve state id's since this time
        :type since: str
        :return: LRS Response object with the retrieved state id's as content
        :rtype: :mod:`tincan.lrs_response`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "activities/state")
        request.query_params = {"activityId": activity.id, "agent": agent.as_version(self._version)}

        if registration is not None:
            request.query_params["registration"] = registration
        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = json.load(lrs_response.response.read())

        return lrs_response

    def retrieve_state(self, activity, agent, state_id, registration=None):
        """Retrieve state from LRS with the provided parameters

        :param activity: Activity object of desired state
        :type activity: Activity
        :param agent: Agent object of desired state
        :type agent: Agent
        :param state_id: UUID of desired state
        :type state_id: str
        :param registration: registration UUID of desired state
        :type registration: str
        :return: LRS Response object with retrieved state document as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "activities/state", ignore404=True)

        request.query_params = {
            "activityId": activity.id,
            "agent": agent.as_version(self._version),
            "stateId": state_id
        }

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self.send_request(request)

        if lrs_response.success:
            doc = StateDocument(id=state_id, content=lrs_response.response.read(), activity=activity, agent=agent)
            if registration is not None:
                doc.registration = registration

            headers = lrs_response.response.getheader()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.time_stamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_state(self, state):
        """Save a state doc to the LRS

        :param state: State document to be saved
        :type state: StateDocument
        :return: LRS Response object with saved state as content
        :rtype: LRSResponse
        """
        request = HTTPRequest(self._endpoint, "PUT", "activities/state", content=state.content)
        request.headers["Content-Type"] = state.content_type

        if state.etag is not None:
            request.headers["If-Match"] = state.etag

        request.query_params = {"stateId": state.id,
                                "activityId": state.activity.id,
                                "agent": state.agent.as_version(self._version)}

        lrs_response = self.send_request(request)
        lrs_response.content = state

        return self.send_request(request)

    def _delete_state(self, activity, agent, state_id=None, registration=None, etag=None):
        """Private method to delete a specified state from the LRS

        :param activity: Activity object of state to be deleted
        :type activity: Activity
        :param agent: Agent object of state to be deleted
        :type agent: Agent
        :param state_id: UUID of state to be deleted
        :type state_id: str
        :param registration: registration UUID of state to be deleted
        :type registration: str
        :param etag: etag of state to be deleted
        :type etag: str
        :return: LRS Response object with deleted state as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "DELETE", "activities/state")

        if etag is not None:
            request.headers["If-Match"] = etag

        request.query_params = {"activityId": activity.id,
                                "agent": agent.as_version(self._version)}

        if state_id is not None:
            request.query_params["stateId"] = state_id

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self.send_request(request)

        return lrs_response

    def delete_state(self, state):
        """Delete a specified state from the LRS

        :param state: State document to be deleted
        :type state: StateDocument
        :return: LRS Response object
        :rtype: LRSResponse
        """
        return self._delete_state(state.activity, state.agent, state_id=state.id, etag=state.etag)

    def clear_state(self, activity, agent, registration=None):
        """Clear state(s) with specified activity and agent

        :param activity: Activity object of state(s) to be deleted
        :type activity: Activity
        :param agent: Agent object of state(s) to be deleted
        :type agent: Agent
        :param registration: registration UUID of state(s) to be deleted
        :type registration: str
        :return: LRS Response object
        :rtype: LRSResponse
        """
        return self._delete_state(activity, agent, registration=registration)

    def retrieve_activity_profile_ids(self, activity, since=None):
        """Retrieve activity profile id(s) with the specified parameters

        :param activity: Activity object of desired activity profiles
        :type activity: Activity
        :param since: Retrieve activity profile id's since this time
        :type since: str
        :return: LRS Response object with list of retrieved activity profile id's as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(self._endpoint, "GET", "activities/profile")

        request.query_params["activityId"] = activity.id

        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = json.load(lrs_response.response.read())

        return lrs_response

    def retrieve_activity_profile(self, activity, profile_id):
        """Retrieve activity profile with the specified parameters

        :param activity: Activity object of the desired activity profile
        :type activity: Activity
        :param profile_id: UUID of the desired profile
        :type profile_id: str
        :return: LRS Response object with an activity profile doc as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(self._endpoint, "GET", "activities/profile", ignore404=True)

        request.query_params = {"profileId": profile_id, "activityId": activity.id}

        lrs_response = self.send_request(request)

        if lrs_response.success:
            doc = ActivityProfileDocument(id=profile_id, content=lrs_response.response.read(), activity=activity)

            headers = lrs_response.response.getheader()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.time_stamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_activity_profile(self, profile):
        """Save an activity profile doc to the LRS

        :param profile: Activity profile doc to be saved
        :type profile: ActivityProfileDocument
        :return: LRS Response object with the saved activity profile doc as content
        :rtype: LRSResponse
        """
        request = HTTPRequest(self._endpoint, "PUT", "activities/profile", content=profile.content)
        request.headers["Content-Type"] = profile.content_type

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        request.query_params = {"profileId": profile.id, "activityId": profile.activity.id}

        lrs_response = self.send_request(request)
        lrs_response.content = profile

        return lrs_response

    def delete_activity_profile(self, profile):
        """Delete activity profile doc from LRS

        :param profile: Activity profile document to be deleted
        :type profile: ActivityProfileDocument
        :return: LRS Response object
        :rtype: LRSResponse
        """
        request = HTTPRequest(self._endpoint, "DELETE", "activities/profile")
        request.query_params = {"profileId": profile.id, "activityId": profile.activity.id}

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        return self.send_request(request)

    def retrieve_agent_profile_ids(self, agent, since=None):
        """Retrieve agent profile id(s) with the specified parameters

        :param agent: Agent object of desired agent profiles
        :type agent: Agent
        :param since: Retrieve agent profile id's since this time
        :type since: str
        :return: LRS Response object with list of retrieved agent profile id's as content
        :rtype: LRSResponse
        """
        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "agents/profile")

        request.query_params["agent"] = agent.as_version(self._version)

        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = json.load(lrs_response.response.read())

        return lrs_response

    def retrieve_agent_profile(self, agent, profile_id):
        """Retrieve agent profile with the specified parameters

        :param agent: Agent object of the desired agent profile
        :type agent: Agent
        :param profile_id: UUID of the desired agent profile
        :type profile_id: str
        :return: LRS Response object with an agent profile doc as content
        :rtype: LRSResponse
        """
        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "agents/profile", ignore404=True)

        request.query_params = {"profileId": profile_id, "agent": agent.as_version(self._version)}

        lrs_response = self.send_request(request)

        if lrs_response.success:
            doc = AgentProfileDocument(id=profile_id, content=lrs_response.response.read(), agent=agent)

            headers = lrs_response.response.getheader()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.time_stamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_agent_profile(self, profile):
        """Save an agent profile doc to the LRS

        :param profile: Agent profile doc to be saved
        :type profile: AgentProfileDocument
        :return: LRS Response object with the saved agent profile doc as content
        :rtype: LRSResponse
        """
        request = HTTPRequest(self._endpoint, "PUT", "agents/profile", content=profile.content)
        request.headers["Content-Type"] = profile.content_type

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        request.query_params = {"profileId": profile.id, "agent": profile.agent.as_version(self._version)}

        lrs_response = self.send_request(request)
        lrs_response.content = profile

        return lrs_response

    def delete_agent_profile(self, profile):
        """Delete agent profile doc from LRS

        :param profile: Agent profile document to be deleted
        :type profile: AgentProfileDocument
        :return: LRS Response object
        :rtype: LRSResponse
        """
        request = HTTPRequest(self._endpoint, "DELETE", "agents/profile")
        request.query_params = {"profileId": profile.id, "agent": profile.agent.as_version(self._version)}

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        return self.send_request(request)

    def set_endpoint(self, endpoint):
        """Sets the target LRS endpoint

        :param endpoint: Endpoint of target LRS
        :type endpoint: str
        """
        if not endpoint.endswith("/"):
            endpoint += "/"

        self._endpoint = endpoint

    def get_endpoint(self):
        """Get the endpoint of this RemoteLRS object

        :return: Endpoint of target LRS
        :rtype: str
        """
        return self._endpoint

    def set_version(self, version):
        """Set the version to be used by this RemoteLRS object. Raises an exception for unsupported versions.

        :param version: Version to be used
        :type version: str
        """
        if not version in Version.supported:
            raise Exception("Unsupported Version")

        self._version = version

    def get_version(self):
        """Get the version being used by this RemoteLRS object.

        :return: version being used
        :rtype: str
        """
        return self._version

    def set_auth(self, auth=None, username=None, password=None):
        """Set the authority for this RemoteLRS object. Must be called with auth or with username and password.
        If not, an exception is thrown.

        :param auth: Authority for this RemoteLRS object
        :type auth: str
        :param username: Username for the authority
        :type username: str
        :param password: Password for this authority
        :type password: str
        """
        if auth is not None:
            self._auth = auth
        elif username is not None and password is not None:
            self._auth = "Basic " + base64.b64encode(username + ":" + password)
        else:
            raise Exception("set_auth must be called with auth or with username and password")

    def get_auth(self):
        """Get the authority being used for this Remote LRS object

        :return: Authority for this Remote LRS object
        :rtype: str
        """
        return self._auth

    def get_endpoint_server_root(self):
        """Parses RemoteLRS object's endpoint and returns its root

        :return: Root of the RemoteLRS object endpoint
        :rtype: str
        """
        parsed = urlparse(self._endpoint)
        root = parsed.scheme + "://" + parsed.hostname

        if parsed.port is not None:
            root += ":" + str(parsed.port)

        return root