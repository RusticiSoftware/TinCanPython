import json
"""
.. module:: TinCanBaseObject
   :synopsis: A Base level object that provides common functionality to other TinCan object

.. moduleauthor:: Rustici Software

"""
class TinCanBaseObject(object):

   def fromJSON(self, json_data):
       """Tries to convert a JSON representation to an object of the same type as self

       A class can provide a _fromJSON implementation in order to do specific type
       checking or other custom implementation details

       :param json_data: The JSON string to convert
       "type json_data: str

       """
       data = json.loads(json_data)
       self.__init__(**data)
       if "_fromJSON" in dir(self):
           self._fromJSON()

   def asVersion(self, version):
       """Returns an object that has been modified based on versioning \
       in order to be represented in JSON properly

       A class can provide an _asVersion(self, result, version) implementation \
       in order to tailor a more specific representation

       :param version: the relevant version. This allows for variance between versions
       :type version: str

       """
       result = self
       if "_asVersion" in dir(self):
           self._asVersion(result, version)
       return result
