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
            if url.endswith("/"):
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
            web_req = httplib.HTTPSConnection(parsed.hostname)
        else:
            web_req = httplib.HTTPConnection(parsed.hostname)

        path = parsed.path
        if params:
            path += "?"

        web_req.request(request.method, path, params, headers)

        if request.content is not None:
            web_req.send(request.content)

        response = web_req.getresponse()

        if (200 <= response.status < 300) or (response.status == 404 and request.ignore404):
            success = True
        elif 300 <= response.status < 400:
            raise Exception("Bad Response Status Code: " + response.status)
            success = False
        else:
            success = False

        return LRSResponse.LRSResponse(success, request, response)

    def about(self):
        request = HTTPRequest.HTTPRequest(endpoint=self.endpoint, resource="about", method="GET")
        lrs_response = self.send_request(request)

        if lrs_response.success:
            pass
            #TODO:
            #lrs_response.content = lrs_response.response.content (from JSON)

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
                pass
                #lrs_response.id = #JSON decoded statement id
            lrs_response.content = statement

        return lrs_response