# Copyright 2014 Rustici Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import http.client
import json
import base64


from urllib.parse import urlparse, urlencode

from tincan.lrs_response import LRSResponse
from tincan.http_request import HTTPRequest
from tincan.statement_list import StatementList
from tincan.agent import Agent
from tincan.statement import Statement
from tincan.activity import Activity
from tincan.statements_result import StatementsResult
from tincan.about import About
from tincan.version import Version
from tincan.base import Base
from tincan.documents import (
    StateDocument,
    ActivityProfileDocument,
    AgentProfileDocument
)

"""
.. module:: remote_lrs
   :synopsis: The RemoteLRS class implements LRS communication.
"""


class RemoteLRS(Base):
    _props_req = [
        'version',
        'endpoint',
        'auth',
    ]

    _props = []

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        """RemoteLRS Constructor

        :param endpoint: lrs endpoint
        :type endpoint: str | unicode
        :param version: Version used for lrs communication
        :type version: str | unicode
        :param username: Username for lrs. Used to build the authentication string.
        :type username: str | unicode
        :param password: Password for lrs. Used to build the authentication string.
        :type password: str | unicode
        :param auth: Authentication string
        :type auth: str | unicode
        """

        self._version = Version.latest
        self._endpoint = None
        self._auth = None

        if "username" in kwargs \
                and kwargs["username"] is not None \
                and "password" in kwargs \
                and kwargs["password"] is not None \
                and "auth" not in kwargs:
            bytes = (
                str(kwargs["username"]) +
                ":" +
                str(kwargs["password"])).encode('ASCII')
            auth_string = str.format("Basic {}", base64.b64encode(bytes).decode("utf-8"))

            kwargs.pop("username")
            kwargs.pop("password")
            kwargs["auth"] = auth_string

        super(RemoteLRS, self).__init__(*args, **kwargs)

    def _send_request(self, request):
        """Establishes connection and returns http response based off of request.

        :param request: HTTPRequest object
        :type request: :class:`tincan.http_request.HTTPRequest`
        :returns: LRS Response object
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        headers = {"X-Experience-API-Version": self.version}

        if self.auth is not None:
            headers["Authorization"] = self.auth

        headers.update(request.headers)

        params = request.query_params
        params = {k: str(params[k]).encode('utf-8') for k in list(params.keys())}
        params = urlencode(params)

        if request.resource.startswith('http'):
            url = request.resource
        else:
            url = self.endpoint
            url += request.resource

        parsed = urlparse(url)

        if parsed.scheme == "https":
            web_req = http.client.HTTPSConnection(parsed.hostname, parsed.port)
        else:
            web_req = http.client.HTTPConnection(parsed.hostname, parsed.port)

        path = parsed.path
        if parsed.query or parsed.path:
            path += "?"
            if parsed.query:
                path += parsed.query
            if params:
                path += params

        if hasattr(request, "content") and request.content is not None:
            web_req.request(
                method=request.method,
                url=path,
                body=request.content,
                headers=headers,
            )
        else:
            web_req.request(
                method=request.method,
                url=path,
                headers=headers,
            )

        response = web_req.getresponse()
        data = response.read()
        web_req.close()

        if (200 <= response.status < 300
            or (response.status == 404
                and hasattr(request, "ignore404")
                and request.ignore404)):
            success = True
        else:
            success = False

        return LRSResponse(
            success=success,
            request=request,
            response=response,
            data=data,
        )

    def about(self):
        """Gets about response from LRS

        :return: LRS Response object with the returned LRS about object as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="GET",
            resource="about"
        )
        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = About.from_json(lrs_response.data)

        return lrs_response

    def save_statement(self, statement):
        """Save statement to LRS and update statement id if necessary

        :param statement: Statement object to be saved
        :type statement: :class:`tincan.statement.Statement`
        :return: LRS Response object with the saved statement as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(statement, Statement):
            statement = Statement(statement)

        request = HTTPRequest(
            method="POST",
            resource="statements"
        )
        if statement.id is not None:
            request.method = "PUT"
            request.query_params["statementId"] = statement.id

        request.headers["Content-Type"] = "application/json"
        request.content = statement.to_json(self.version)

        lrs_response = self._send_request(request)

        if lrs_response.success:
            if statement.id is None:
                statement.id = json.loads(lrs_response.data)[0]
            lrs_response.content = statement

        return lrs_response

    def save_statements(self, statements):
        """Save statements to LRS and update their statement id's

        :param statements: A list of statement objects to be saved
        :type statements: :class:`StatementList`
        :return: LRS Response object with the saved list of statements as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(statements, StatementList):
            statements = StatementList(statements)

        request = HTTPRequest(
            method="POST",
            resource="statements"
        )
        request.headers["Content-Type"] = "application/json"

        request.content = statements.to_json()

        lrs_response = self._send_request(request)

        if lrs_response.success:
            id_list = json.loads(lrs_response.data)
            for s, statement_id in zip(statements, id_list):
                s.id = statement_id

            lrs_response.content = statements

        return lrs_response

    def retrieve_statement(self, statement_id):
        """Retrieve a statement from the server from its id

        :param statement_id: The UUID of the desired statement
        :type statement_id: str | unicode
        :return: LRS Response object with the retrieved statement as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="GET",
            resource="statements"
        )
        request.query_params["statementId"] = statement_id

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = Statement.from_json(lrs_response.data)

        return lrs_response

    def retrieve_voided_statement(self, statement_id):
        """Retrieve a voided statement from the server from its id

        :param statement_id: The UUID of the desired voided statement
        :type statement_id: str | unicode
        :return: LRS Response object with the retrieved voided statement as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="GET",
            resource="statements"
        )
        request.query_params["voidedStatementId"] = statement_id

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = Statement.from_json(lrs_response.data)

        return lrs_response

    def query_statements(self, query):
        """Query the LRS for statements with specified parameters

        :param query: Dictionary of query parameters and their values
        :type query: dict
        :return: LRS Response object with the returned StatementsResult object as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`

        .. note::
           Optional query parameters are\n
               **statementId:** (*str*) ID of the Statement to fetch
               **voidedStatementId:** (*str*) ID of the voided Statement to fetch
               **agent:** (*Agent* |*Group*) Filter to return Statements for which the
               specified Agent or Group is the Actor
               **verb:** (*Verb id IRI*) Filter to return Statements matching the verb id
               **activity:** (*Activity id IRI*) Filter to return Statements for which the
               specified Activity is the Object
               **registration:** (*UUID*) Filter to return Statements matching the specified registration ID
               **related_activities:** (*bool*) Include Statements for which the Object,
               Context Activities or any Sub-Statement
               properties match the specified Activity
               **related_agents:** (*bool*) Include Statements for which the Actor, Object,
               Authority, Instructor, Team, or any Sub-Statement properties match the specified Agent
               **since:** (*datetime*) Filter to return Statements stored since the specified datetime
               **until:** (*datetime*) Filter to return Statements stored at or before the specified datetime
               **limit:** (*positive int*) Allow <limit> Statements to be returned. 0 indicates the
               maximum supported by the LRS
               **format:** (*str* {"ids"|"exact"|"canonical"}) Manipulates how the LRS handles
               importing and returning the statements
               **attachments:** (*bool*) If true, the LRS will use multipart responses and include
               all attachment data per Statement returned.
               Otherwise, application/json is used and no attachment information will be returned
               **ascending:** (*bool*) If true, the LRS will return results in ascending order of
               stored time (oldest first)
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

        for k, v in query.items():
            if v is not None:
                if k == "agent":
                    params[k] = v.to_json(self.version)
                elif k == "verb" or k == "activity":
                    params[k] = v.id
                elif k in param_keys:
                    params[k] = v

        request = HTTPRequest(
            method="GET",
            resource="statements"
        )
        request.query_params = params

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult.from_json(lrs_response.data)

        return lrs_response

    def more_statements(self, more_url):
        """Query the LRS for more statements

        :param more_url: URL from a StatementsResult object used to retrieve more statements
        :type more_url: str | unicode
        :return: LRS Response object with the returned StatementsResult object as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if isinstance(more_url, StatementsResult):
            more_url = more_url.more

        more_url = self.get_endpoint_server_root() + more_url

        request = HTTPRequest(
            method="GET",
            resource=more_url
        )

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult.from_json(lrs_response.data)

        return lrs_response

    def retrieve_state_ids(self, activity, agent, registration=None, since=None):
        """Retrieve state id's from the LRS with the provided parameters

        :param activity: Activity object of desired states
        :type activity: :class:`tincan.activity.Activity`
        :param agent: Agent object of desired states
        :type agent: :class:`tincan.agent.Agent`
        :param registration: Registration UUID of desired states
        :type registration: str | unicode
        :param since: Retrieve state id's since this time
        :type since: str | unicode
        :return: LRS Response object with the retrieved state id's as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(
            method="GET",
            resource="activities/state"
        )
        request.query_params = {
            "activityId": activity.id,
            "agent": agent.to_json(self.version)
        }

        if registration is not None:
            request.query_params["registration"] = registration
        if since is not None:
            request.query_params["since"] = since

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = json.loads(lrs_response.data)

        return lrs_response

    def retrieve_state(self, activity, agent, state_id, registration=None):
        """Retrieve state from LRS with the provided parameters

        :param activity: Activity object of desired state
        :type activity: :class:`tincan.activity.Activity`
        :param agent: Agent object of desired state
        :type agent: :class:`tincan.agent.Agent`
        :param state_id: UUID of desired state
        :type state_id: str | unicode
        :param registration: registration UUID of desired state
        :type registration: str | unicode
        :return: LRS Response object with retrieved state document as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(
            method="GET",
            resource="activities/state",
            ignore404=True
        )

        request.query_params = {
            "activityId": activity.id,
            "agent": agent.to_json(self.version),
            "stateId": state_id
        }

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self._send_request(request)

        if lrs_response.success:
            doc = StateDocument(
                id=state_id,
                content=lrs_response.data,
                activity=activity,
                agent=agent
            )
            if registration is not None:
                doc.registration = registration

            headers = lrs_response.response.getheaders()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.timestamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_state(self, state):
        """Save a state doc to the LRS

        :param state: State document to be saved
        :type state: :class:`tincan.documents.state_document.StateDocument`
        :return: LRS Response object with saved state as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="PUT",
            resource="activities/state",
            content=state.content,
        )
        if state.content_type is not None:
            request.headers["Content-Type"] = state.content_type
        else:
            request.headers["Content-Type"] = "application/octet-stream"

        if state.etag is not None:
            request.headers["If-Match"] = state.etag

        request.query_params = {
            "stateId": state.id,
            "activityId": state.activity.id,
            "agent": state.agent.to_json(self.version)
        }
        lrs_response = self._send_request(request)
        lrs_response.content = state

        return self._send_request(request)

    def _delete_state(self, activity, agent, state_id=None, registration=None, etag=None):
        """Private method to delete a specified state from the LRS

        :param activity: Activity object of state to be deleted
        :type activity: :class:`tincan.activity.Activity`
        :param agent: Agent object of state to be deleted
        :type agent: :class:`tincan.agent.Agent`
        :param state_id: UUID of state to be deleted
        :type state_id: str | unicode
        :param registration: registration UUID of state to be deleted
        :type registration: str | unicode
        :param etag: etag of state to be deleted
        :type etag: str | unicode
        :return: LRS Response object with deleted state as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(
            method="DELETE",
            resource="activities/state"
        )

        if etag is not None:
            request.headers["If-Match"] = etag

        request.query_params = {
            "activityId": activity.id,
            "agent": agent.to_json(self.version)
        }
        if state_id is not None:
            request.query_params["stateId"] = state_id

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self._send_request(request)

        return lrs_response

    def delete_state(self, state):
        """Delete a specified state from the LRS

        :param state: State document to be deleted
        :type state: :class:`tincan.documents.state_document.StateDocument`
        :return: LRS Response object
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        return self._delete_state(
            activity=state.activity,
            agent=state.agent,
            state_id=state.id,
            etag=state.etag
        )

    def clear_state(self, activity, agent, registration=None):
        """Clear state(s) with specified activity and agent

        :param activity: Activity object of state(s) to be deleted
        :type activity: :class:`tincan.activity.Activity`
        :param agent: Agent object of state(s) to be deleted
        :type agent: :class:`tincan.agent.Agent`
        :param registration: registration UUID of state(s) to be deleted
        :type registration: str | unicode
        :return: LRS Response object
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        return self._delete_state(
            activity=activity,
            agent=agent,
            registration=registration
        )

    def retrieve_activity_profile_ids(self, activity, since=None):
        """Retrieve activity profile id(s) with the specified parameters

        :param activity: Activity object of desired activity profiles
        :type activity: :class:`tincan.activity.Activity`
        :param since: Retrieve activity profile id's since this time
        :type since: str | unicode
        :return: LRS Response object with list of retrieved activity profile id's as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(
            method="GET",
            resource="activities/profile"
        )
        request.query_params["activityId"] = activity.id

        if since is not None:
            request.query_params["since"] = since

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = json.loads(lrs_response.data)

        return lrs_response

    def retrieve_activity_profile(self, activity, profile_id):
        """Retrieve activity profile with the specified parameters

        :param activity: Activity object of the desired activity profile
        :type activity: :class:`tincan.activity.Activity`
        :param profile_id: UUID of the desired profile
        :type profile_id: str | unicode
        :return: LRS Response object with an activity profile doc as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(
            method="GET",
            resource="activities/profile",
            ignore404=True
        )
        request.query_params = {
            "profileId": profile_id,
            "activityId": activity.id
        }
        lrs_response = self._send_request(request)

        if lrs_response.success:
            doc = ActivityProfileDocument(
                id=profile_id,
                content=lrs_response.data,
                activity=activity
            )
            headers = lrs_response.response.getheaders()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.timestamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_activity_profile(self, profile):
        """Save an activity profile doc to the LRS

        :param profile: Activity profile doc to be saved
        :type profile: :class:`tincan.documents.activity_profile_document.ActivityProfileDocument`
        :return: LRS Response object with the saved activity profile doc as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="PUT",
            resource="activities/profile",
            content=profile.content
        )
        if profile.content_type is not None:
            request.headers["Content-Type"] = profile.content_type
        else:
            request.headers["Content-Type"] = "application/octet-stream"

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        request.query_params = {
            "profileId": profile.id,
            "activityId": profile.activity.id
        }
        lrs_response = self._send_request(request)
        lrs_response.content = profile

        return lrs_response

    def delete_activity_profile(self, profile):
        """Delete activity profile doc from LRS

        :param profile: Activity profile document to be deleted
        :type profile: :class:`tincan.documents.activity_profile_document.ActivityProfileDocument`
        :return: LRS Response object
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="DELETE",
            resource="activities/profile"
        )
        request.query_params = {
            "profileId": profile.id,
            "activityId": profile.activity.id
        }

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        return self._send_request(request)

    def retrieve_agent_profile_ids(self, agent, since=None):
        """Retrieve agent profile id(s) with the specified parameters

        :param agent: Agent object of desired agent profiles
        :type agent: :class:`tincan.agent.Agent`
        :param since: Retrieve agent profile id's since this time
        :type since: str | unicode
        :return: LRS Response object with list of retrieved agent profile id's as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(
            method="GET",
            resource="agents/profile"
        )
        request.query_params["agent"] = agent.to_json(self.version)

        if since is not None:
            request.query_params["since"] = since

        lrs_response = self._send_request(request)

        if lrs_response.success:
            lrs_response.content = json.loads(lrs_response.data)

        return lrs_response

    def retrieve_agent_profile(self, agent, profile_id):
        """Retrieve agent profile with the specified parameters

        :param agent: Agent object of the desired agent profile
        :type agent: :class:`tincan.agent.Agent`
        :param profile_id: UUID of the desired agent profile
        :type profile_id: str | unicode
        :return: LRS Response object with an agent profile doc as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(
            method="GET",
            resource="agents/profile",
            ignore404=True
        )
        request.query_params = {
            "profileId": profile_id,
            "agent": agent.to_json(self.version)
        }

        lrs_response = self._send_request(request)

        if lrs_response.success:
            doc = AgentProfileDocument(
                id=profile_id,
                content=lrs_response.data,
                agent=agent
            )
            headers = lrs_response.response.getheaders()
            if "lastModified" in headers and headers["lastModified"] is not None:
                doc.timestamp = headers["lastModified"]
            if "contentType" in headers and headers["contentType"] is not None:
                doc.content_type = headers["contentType"]
            if "etag" in headers and headers["etag"] is not None:
                doc.etag = headers["etag"]

            lrs_response.content = doc

        return lrs_response

    def save_agent_profile(self, profile):
        """Save an agent profile doc to the LRS

        :param profile: Agent profile doc to be saved
        :type profile: :class:`tincan.documents.agent_profile_document.AgentProfileDocument`
        :return: LRS Response object with the saved agent profile doc as content
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="PUT",
            resource="agents/profile",
            content=profile.content,
        )
        if profile.content_type is not None:
            request.headers["Content-Type"] = profile.content_type
        else:
            request.headers["Content-Type"] = "application/octet-stream"

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        request.query_params = {
            "profileId": profile.id,
            "agent": profile.agent.to_json(self.version)
        }
        lrs_response = self._send_request(request)
        lrs_response.content = profile

        return lrs_response

    def delete_agent_profile(self, profile):
        """Delete agent profile doc from LRS

        :param profile: Agent profile document to be deleted
        :type profile: :class:`tincan.documents.agent_profile_document.AgentProfileDocument`
        :return: LRS Response object
        :rtype: :class:`tincan.lrs_response.LRSResponse`
        """
        request = HTTPRequest(
            method="DELETE",
            resource="agents/profile"
        )
        request.query_params = {
            "profileId": profile.id,
            "agent": profile.agent.to_json(self.version)
        }

        if profile.etag is not None:
            request.headers["If-Match"] = profile.etag

        return self._send_request(request)

    @property
    def endpoint(self):
        """The endpoint of the Remote LRS

        :setter: Tries to convert to unicode.  Appends a "/" if necessary. Prepends http:// if necessary.
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        if value is not None:
            if not isinstance(value, str):
                value = str(value)
            if not value.endswith("/"):
                value += "/"
            if not value.startswith("http"):
                value = "http://" + value

        self._endpoint = value

    @property
    def version(self):
        """Version being used for remote LRS communication

        :setter: Tries to convert to unicode.  Must be a supported
        version. Setting to None defaults to the latest version.
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._version

    @version.setter
    def version(self, value):
        if value is not None:
            if not isinstance(value, str):
                str(value)
            if value not in Version.supported:
                raise Exception("Unsupported Version")
        else:
            value = Version.latest

        self._version = value

    @property
    def auth(self):
        """Authority being used for remote LRS communication

        :setter: Tries to convert to unicode.
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._auth

    @auth.setter
    def auth(self, value):
        if value is not None and not isinstance(value, str):
            str(value)
        self._auth = value

    def get_endpoint_server_root(self):
        """Parses RemoteLRS object's endpoint and returns its root

        :return: Root of the RemoteLRS object endpoint
        :rtype: unicode
        """
        parsed = urlparse(self._endpoint)
        root = parsed.scheme + "://" + parsed.hostname

        if parsed.port is not None:
            root += ":" + str(parsed.port)

        return root
