from tincanbase import TinCanBaseObject
from languagemap import LanguageMap
"""
.. module:: verb
   :synopsis: A Verb object that contains an id and a display

.. moduleauthor:: Rustici Software

"""
class Verb(TinCanBaseObject):

   def __init__(self, id = '', display = None):
       """Verb Object

       :param id: The id of the verb
       :type id: str
       :param display: The LanguageMap indicating how the verb object should be displayed
       :type id: :mod:`LanguageMap`

       """
       if display is not None:
           if not display:
               display = None
           elif not isinstance(display, LanguageMap):
               display = LanguageMap(display)
           elif len(vars(display)) == 0:
               display = None
       self.id = id
       self.display = display

   def __repr__(self):
       return '%s' % (self.__dict__)
