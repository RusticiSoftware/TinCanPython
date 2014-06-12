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

from urlparse import urlparse
from lrs_response import LRSResponse
from http_request import HTTPRequest
from agent import Agent
from statement import Statement
from activity import Activity
from statements_result import StatementsResult
from about import About
"""
.. module:: remote_lrs
   :synopsis: The RemoteLRS objects implements LRS communication.
"""


class RemoteLRS(object):

    #TODO: set default version value, endpoint=None
    def __init__(self, endpoint, version="1.0.1", username=None, password=None, auth=None):
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
        self.endpoint = endpoint
        self.version = version

        if auth is not None:
            self.auth = auth
        elif username is not None and password is not None:
            self.auth = {username: password}

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
            url = self.endpoint
            if not url.endswith("/"):
                url += "/"
            url += request.resource

        parsed = urlparse(url)

        headers = {"X-Experience-API-Version": self.version}

        if self.auth is not None:
            #TODO: take another look at this
            headers["Authorization"] = self.auth

        headers.update(request.headers)

        params = request.query_params
        params = {k: unicode(params[k]).encode('utf-8') for k in params.keys()}
        params = urllib.urlencode(params)

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
        :rtype: :mod:`tincan.lrs_response`
        """
        request = HTTPRequest(endpoint=self.endpoint, resource="about", method="GET")
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

        request = HTTPRequest(endpoint=self.endpoint, resource="statements", method="POST")

        if statement.id is not None:
            request.method = "PUT"
            request.query_params["statementId"] = statement.id

        request.headers["Content-Type"] = "application/json"
        request.content = statement.to_json(self.version)

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
        :rtype: :mod:`tincan.lrs_response`
        """
        #TODO: verify all statements are instances of statements and versioned to this.version

        request = HTTPRequest(endpoint=self.endpoint, resource="statements", method="POST")
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
        :rtype: :mod:`tincan.lrs_response`
        """
        request = HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
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
        request = HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
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

        param_keys = ["registration", "since", "until", "limit", "ascending", "related_activities",
                        "related_agents", "format", "attachments"]

        for k, v in query.items():
            if v is not None:
                if k == "agent":
                    params[k] = v.to_json(self.version)
                elif k == "verb" or k == "activity":
                    params[k] = v.id
                elif k in param_keys:
                    params[k] = v

        request = HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
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

        request = HTTPRequest(endpoint=self.endpoint, method="GET", resource=more_url)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            lrs_response.content = StatementsResult.from_json(lrs_response.response.read())

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
        if isinstance(activity, Activity):
            activity = Activity(activity)

        if isinstance(agent, Agent):
            agent = Agent(agent)

        request = HTTPRequest(endpoint=self.endpoint, method="GET", resource="activities/state")
        request.query_params = {"activityId": activity.id, "agent": agent.to_json(self.version)}

        if registration is not None:
            request.query_params["registration"] = registration
        if since is not None:
            request.query_params["since"] = since

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO:look more into this decoding the ids
            lrs_response.content = json.load(lrs_response.response.read())

        return lrs_response

    def get_endpoint_server_root(self):
        """Parses RemoteLRS object's endpoint and returns its root

        :return: Root of the RemoteLRS object endpoint
        :rtype: str
        """
        parsed = urlparse(self.endpoint)
        root = parsed.scheme + "://" + parsed.hostname

        if parsed.port is not None:
            root += ":" + str(parsed.port)

        return root