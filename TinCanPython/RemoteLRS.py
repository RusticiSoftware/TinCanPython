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
            if self.endpoint[-1] == "/":
                url = self.endpoint + request.resource
            else:
                url = self.endpoint + "/" + request.resource

        parsed = urlparse(url)

        headers = {"X-Experience-API-Version": self.version}

        if self.auth is not None:
            #TODO: take another look at this
            headers["Authorization"] = self.auth

        headers.update(request.headers)

        #TODO: unnecessary?
        for k, v in request.query_params:
            request.query_params[k] = unicode(v).encode('utf-8')

        request.query_params = urllib.urlencode(request.query_params)

        if parsed.scheme == "https":
            web_req = httplib.HTTPSConnection(parsed.hostname)
        else:
            web_req = httplib.HTTPConnection(parsed.hostname)

        #TODO: needs an added '?' for query parameters?
        web_req.request(request.method, parsed.path, request.query_params, request.headers)

        if request.content is not None:
            web_req.send(request.content)

        response = web_req.getresponse()

        if (200 <= response.status < 300) or (response.status == 404 and request.ignore404):
            success = True
        elif 300 <= response.status < 400:
            #TODO: throw exception here?
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
