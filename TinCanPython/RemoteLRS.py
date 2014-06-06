import httplib
import urllib
from urlparse import urlparse
import LRSResponse
import HTTPRequest


class RemoteLRS(object):
    """
    This class implements the LRS communication.
    """

    #TODO: set default version value, endpoint=None
    def __init__(self, endpoint, version="1.0.1", username=None, password=None, auth=None):
        self.endpoint = endpoint
        self.version = version

        if auth is not None:
            self.auth = auth
        elif username is not None and password is not None:
            self.auth = {username: password}

    def send_request(self, request):

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

        return LRSResponse.LRSResponse(success, request, response)

    def about(self):
        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, resource="about", method="GET")
        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: set lrs response from response content from JSON
            pass

        return lrs_response

    def save_statement(self, statement):
        #TODO: verify is instance of statement? (can't do yet)

        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, resource="statements", method="POST")

        if statement.id is not None:
            request.method = "PUT"
            request.query_params["statementId"] = statement.id

        request.headers["Content-Type"] = "application/json"
        #request.content = #JSON encoded statement

        lrs_response = self.send_request(request)

        if lrs_response.success:
            if statement.id is not None:
                #TODO: set statement id from lrs response
                pass
            lrs_response.content = statement

        return lrs_response

    def save_statements(self, statements):
        #TODO: verify all statements are instances of statements and versioned to this.version

        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, resource="statements", method="POST")
        request.headers["Content-Type"] = "application/json"
        #request.content = #JSON encoded statements

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: set id for each statement form lrs response
            lrs_response.content = statements

        return lrs_response

    def retrieve_statement(self, id):
        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
        request.query_params["statementId"] = id

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: set response content = statement from response
            pass

        return lrs_response

    def retrieve_voided_statement(self, id):
        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
        request.query_params["voidedStatementId"] = id

        lrs_response = self.send_request(request)

        if lrs_response.success:
            #TODO: set response content = statement from response
            pass

        return lrs_response

    def query_statements(self, query):
        params = {}

        other_params = ["registration", "since", "until", "limit", "ascending", "related_activities",
                        "related_agents", "format", "attachments"]

        for k,v in query.items():
            if v is not None:
                if k == "agent":
                    pass
                    #TODO: params[k] = #JSON version encoded v (agent)
                elif k == "verb" or k == "activity":
                    pass
                    #TODO: params[k] = v.id
                elif k in other_params:
                    params[k] = v

            request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, method="GET", resource="statements")
            request.query_params = params

            lrs_response = self.send_request(request)

            if lrs_response.success:
                pass
                #TODO: lrs_response.content = #StatementsResult from response content from JSON

            return lrs_response

    def more_statements(self, more_url):
        #TODO: if more_url is a StatementsResult obj, more_url = more_url.more_url
        more_url = self.get_endpoint_server_root() + more_url

        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, method="GET", resource=more_url)

        lrs_response = self.send_request(request)

        if lrs_response.success:
            pass
            #TODO: lrs_response.content = #StatementsResult from response content from JSON

        return lrs_response

    def get_endpoint_server_root(self):
        parsed = urlparse(self.endpoint)
        root = parsed.scheme + "://" + parsed.hostname

        if parsed.port is not None:
            root += ":" + str(parsed.port)

        return root








