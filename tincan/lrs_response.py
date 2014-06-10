class LRSResponse(object):
    """
    Defines the LRSResponse class which is received from LRS communication.
    """
    def __init__(self, success, request, response, data=None):
        self.success = success
        self.request = request
        self.response = response
        if data is not None:
            for k, v in data:
                setattr(self, k, v)

    def load(self, data):
        for k, v in data:
            setattr(self, k, v)