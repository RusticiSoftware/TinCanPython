from TinCanBaseObject import TinCanBaseObject
from Errors.LanguageMapInitError import LanguageMapInitError
"""
.. module:: LanguageMap
   :synopsis: A simple wrapper for a map containing language mappings

.. moduleauthor:: Rustici Software

"""
class LanguageMap(TinCanBaseObject):

   def __init__(self, map = None):
       """Initializes a LanguageMap with the given mapping

       :param map: The intended language mapping
       :type map: dict

       """
       if map is not None and isinstance(map, dict):
           for k, v in map.iteritems():
               setattr(self, k, v)
       else:
           raise LanguageMapInitError("Arguments cannot be coerced into a LanguageMap")

   def __repr__(self):
       return '%s' % (self.__dict__)
