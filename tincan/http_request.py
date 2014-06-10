class HTTPRequest(object):
    def __init__(self, endpoint=None, method=None, resource=None, headers=None,
                 query_params=None, content=None, ignore404=False):
        self.endpoint = endpoint
        self.method = method
        self.resource = resource
        self.content = content
        self.ignore404 = ignore404

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

        if query_params is None:
            self.query_params = {}
        else:
            self.query_params = query_params