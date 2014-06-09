import httplib
import urllib
import json
import base64

from urlparse import urlparse
from lrs_response import LRSResponse
from http_request import HTTPRequest
from agent import Agent
from statement import Statement
from activity import Activity
from statements_result import StatementsResult
from about import About
from versions import Version
from document import Document

"""
.. module:: remote_lrs
   :synopsis: The RemoteLRS objects implements LRS communication.
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
        :type request: HTTPRequest
        :returns: LRS Response object
        :rtype: LRSResponse
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
            path += "?"

        web_req.request(request.method, path, params, headers)

        if request.content is not None:
            web_req.send(request.content)

        response = web_req.getresponse()

        if (200 <= response.status < 300) or (response.status == 404 and request.ignore404):
            success = True
        else:
            success = False

        return LRSResponse(success, request, response)

    def about(self):
        """Gets about response from LRS

        :return: LRS Response object with the returned LRS about object as content
        :rtype: LRSResponse
        """
        request = HTTPRequest(endpoint=self._endpoint, resource="about", method="GET")
        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = About.from_json(lrs_response.response.read())

        return lrs_response

    def save_statement(self, statement):
        """Save statement to LRS and update statement id if necessary

        :param statement: Statement object to be saved
        :type statement: Statement
        :return: LRS Response object with the saved statement as content
        :rtype: LRSResponse
        """
        if not isinstance(statement, Statement):
            statement = Statement(statement)

        request = HTTPRequest(self._endpoint, "statements", "POST")

        if statement.id is not None:
            request.method = "PUT"
            request.query_params["statementId"] = statement.id

        request.headers["Content-Type"] = "application/json"
        request.content = statement.to_json(self._version)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            if statement.id is None:
                statement.id = (Statement.from_json(lrs_response.response.read())).id
            lrs_response.content = statement

        return lrs_response

    def save_statements(self, statements):
        """Save statements to LRS and update their statement id's

        :param statements: A list of statement objects to be saved
        :type statements: list
        :return: LRS Response object with the saved list of statements as content
        :rtype: LRSResponse
        """
        #TODO: verify all statements are instances of statements and versioned to this.version

        request = HTTPRequest(self._endpoint, "statements", "POST")
        request.headers["Content-Type"] = "application/json"
        #TODO: request.content = #JSON encoded statements

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: set id for each statement form lrs response
            lrs_response.content = statements

        return lrs_response

    def retrieve_statement(self, statement_id):
        """Retrieve a statement from the server from its id

        :param statement_id: The UUID of the desired statement
        :type statement_id: str
        :return: LRS Response object with the retrieved statement as content
        :rtype: LRSResponse
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
        :rtype: LRSResponse
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
        :rtype: LRSResponse
        """
        params = {}

        param_keys = ["registration", "since", "until", "limit", "ascending", "related_activities",
                        "related_agents", "format", "attachments"]

        for k, v in query.items():
            if v is not None:
                if k == "agent":
                    params[k] = v.to_json(self._version)
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
        :rtype: LRSResponse
        """
        if isinstance(more_url, StatementsResult):
            more_url = more_url.more

        more_url = self.get_endpoint_server_root() + more_url

        request = HTTPRequest(self._endpoint, "GET", more_url)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult.from_json(lrs_response.response.read())

        return lrs_response

    def retrieve_state_ids(self, activity, agent, registration=None, since=None):
        """Retrieve state id's from the LRS with the provided parameters

        :param activity: Activity object of desired states
        :type activity: Activity
        :param agent: Agent object of desired states
        :type agent: Agent
        :param registration: Registration UUID of desired states
        :type registration: str
        :param since: Retrieve state id's since this time
        :type since: str
        :return: LRS Response object with the retrieved state id's as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "activities/state")
        request.query_params = {"activityId": activity.id, "agent": agent.to_json(self._version)}

        if registration is not None:
            request.query_params["registration"] = registration
        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO:look more into this decoding the ids
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
        :return: LRS Response object with retrieved state as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "GET", "activities/state", ignore404=True)

        request.query_params = {"activityId": activity.id, "agent": agent.to_json(self._version), "stateId": state_id}

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: populate state object and set to content of lrs_response (see PHP RemoteLRS 438-459)
            pass

        return lrs_response

    def save_state(self, activity, agent, state_id, content, content_type="application/octet-stream",
                   etag=None, registration=None):
        """Save a state doc to the LRS

        :param activity: Activity object of state to be saved
        :type activity: Activity
        :param agent: Agent object of state to be saved
        :type agent: Agent
        :param state_id: UUID of state to be saved
        :type state_id: str
        :param content: Content of the state to be saved
        :param content_type: content type of state's content; defaults to "application/octet-stream"
        :type content_type: str
        :param etag: etag of state to be saved
        :type etag: str
        :param registration: registration UUID of state to be saved
        :type registration: str
        :return: LRS Response object with saved state as content
        :rtype: LRSResponse
        """
        #TODO: need :type content: for documentation? If so, is it a str, bytearray, or something else?

        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "PUT", "activities/state")

        request.query_params = {"activityId": activity.id, "agent": agent.to_json(self._version), "stateId": state_id}

        if registration is not None:
            request.query_params["registration"] = registration

        request.content = content

        request.headers["Content-Type"] = content_type

        if etag is not None:
            request.headers["If-Match"] = etag

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: populate state object and set to content of lrs_response (see PHP RemoteLRS 505-522)
            pass

        return lrs_response

    def _delete_state(self, activity, agent, state_id=None, registration=None):
        """Private method to delete a specified state from the LRS

        :param activity: Activity object of state to be deleted
        :type activity: Activity
        :param agent: Agent object of state to be deleted
        :type agent: Agent
        :param state_id: UUID of state to be deleted
        :type state_id: str
        :param registration: registration UUID of state to be deleted
        :type registration: str
        :return: LRS Response object with deleted state as content
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "DELETE", "activities/state")

        request.query_params = {"activityId": activity.id, "agent": agent.to_json(self._version)}

        if state_id is not None:
            request.query_params["stateId"] = state_id

        if registration is not None:
            request.query_params["registration"] = registration

        lrs_response = self.send_request(request)

        return lrs_response

    def delete_state(self, activity, agent, state_id):
        """Delete a specified state from the LRS

        :param activity: Activity object of state to be deleted
        :type activity: Activity
        :param agent: Agent object of state to be deleted
        :type agent: Agent
        :param state_id: UUID of state to be deleted
        :type state_id: str
        :return: LRS Response object
        :rtype: LRSResponse
        """
        return self._delete_state(activity, agent, state_id)

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

        return self._delete_state(activity, agent, registration)

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
            #TODO: look more into this parsing
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
            #TODO: build activity profile from response content
            pass

        return lrs_response

    def save_activity_profile(self, activity, profile_id, content, content_type="application/octet-stream", etag=None):
        """Save an activity profile doc to the LRS

        :param activity: Activity object of the activity profile to be saved
        :type activity: Activity
        :param profile_id: UUID of the profile to be saved
        :type profile_id: str
        :param content: content of the activity profile to be saved
        :param content_type: content type of activity profile's content; defaults to "application/octet-stream"
        :type content_type: str
        :param etag: etag of activity profile to be saved
        :type etag: str
        :return: LRS Response object with the saved activity profile doc as content
        :rtype: LRSResponse
        """
        #TODO: need :type content: for documentation? If so, is it a str, bytearray, or something else?

        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(self._endpoint, "PUT", "activities/profile", content=content)

        request.query_params = {"profileId": profile_id, "activityId": activity.id}

        request.headers["Content-Type"] = content_type

        if etag is not None:
            request.headers["If-Match"] = etag

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: build activity profile from response
            pass

        return lrs_response

    def delete_activity_profile(self, activity, profile_id):
        """Delete activity profile doc from LRS

        :param activity: Activity object of activity profile to be deleted
        :type activity: Activity
        :param profile_id: UUID of activity profile to be deleted
        :type profile_id: str
        :return: LRS Response object
        :rtype: LRSResponse
        """
        if not isinstance(activity, Activity):
            activity = Activity(activity)

        request = HTTPRequest(self._endpoint, "DELETE", "activities/profile")

        request.query_params = {"profileId": profile_id, "activityId": activity.id}

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

        request.query_params["agent"] = agent.to_json()

        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: look more into this parsing
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

        request.query_params = {"profileId": profile_id, "agent": agent.to_json()}

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: build agent profile from response content
            pass

        return lrs_response

    def save_agent_profile(self, agent, profile_id, content, content_type="application/octet-stream", etag=None):
        """Save an agent profile doc to the LRS

        :param agent: Agent object of the agent profile to be saved
        :type agent: Agent
        :param profile_id: UUID of the profile to be saved
        :type profile_id: str
        :param content: content of the agent profile to be saved
        :param content_type: content type of agent profile's content; defaults to "application/octet-stream"
        :type content_type: str
        :param etag: etag of agent profile to be saved
        :type etag: str
        :return: LRS Response object with the saved agent profile doc as content
        :rtype: LRSResponse
        """
        #TODO: need :type content: for documentation? If so, is it a str, bytearray, or something else?

        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "PUT", "agents/profile", content=content)

        request.query_params = {"profileId": profile_id, "agent": agent.to_json()}

        request.headers["Content-Type"] = content_type

        if etag is not None:
            request.headers["If-Match"] = etag

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: build agent profile from response
            pass

        return lrs_response

    def delete_agent_profile(self, agent, profile_id):
        """Delete agent profile doc from LRS

        :param agent: Agent object of agent profile to be deleted
        :type agent: Agent
        :param profile_id: UUID of agent profile to be deleted
        :type profile_id: str
        :return: LRS Response object
        :rtype: LRSResponse
        """
        if not isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(self._endpoint, "DELETE", "agents/profile")

        request.query_params = {"profileId": profile_id, "agent": agent.to_json()}

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
            self._auth = "Basic " + base64.b64encode(username) + ":" + base64.b64encode(password)
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