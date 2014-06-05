import unittest
from TinCanObjects.Verb import Verb
from TinCanObjects.LanguageMap import LanguageMap
from TinCanObjects.Errors.LanguageMapInitError import LanguageMapInitError

class TestVerb(unittest.TestCase):

   def test_VerbInitEmpty(self):
       verb = Verb()
       self.assertEqual(verb.id, '')
       self.assertIsNone(verb.display)

   def test_VerbInitId(self):
       verb = Verb('test')
       self.assertEqual(verb.id, 'test')
       self.assertIsNone(verb.display)

   def test_VerbInitEmptyDisplay(self):
       verb = Verb('test', {})
       self.assertEqual(verb.id, 'test')
       self.assertIsNone(verb.display)

   def test_VerbInitAnonDisplay(self):
       verb = Verb('test', {"test":"test"})
       self.assertEqual(verb.id, 'test')
       self.assertIsInstance(verb.display, LanguageMap)
       self.assertEqual(len(vars(verb.display)), 1)
       self.assertIn('test', verb.display.__dict__)

   def test_VerbInitLanguageMapDisplay(self):
       verb = Verb('test', LanguageMap({"test":"test"}))
       self.assertEqual(verb.id, 'test')
       self.assertIsInstance(verb.display, LanguageMap)
       self.assertEqual(len(vars(verb.display)), 1)
       self.assertIn('test', vars(verb.display))

   def test_VerbInitEmptyLanguageMapDisplay(self):
       verb = Verb('test', LanguageMap({}))
       self.assertEqual(verb.id, 'test')
       self.assertIsNone(verb.display)

   def test_VerbInitUnpack(self):
       obj = {"id": "test", "display": {"test": "test"}}
       verb = Verb(**obj)
       self.assertEqual(verb.id, 'test')
       self.assertEqual(len(vars(verb.display)), 1)
       self.assertIn('test', vars(verb.display))

   def test_VerbInitExceptionUnpackFlatDisplay(self):
       obj = {"id":"test", "display": "test"}
       try:
           verb = Verb(**obj)
       except LanguageMapInitError:
           self.assertTrue(1)
       else:
           self.assertTrue(0)

   def test_VerbFromJSONExceptionEmpty(self):
       verb = Verb()
       try:
           verb.fromJSON('')
       except ValueError:
           self.assertTrue(1)
       else:
           self.assertTrue(0)

   def test_VerbFromJSONId(self):
       verb = Verb()
       verb.fromJSON('{"id":"test"}')
       self.assertEqual(verb.id, 'test')
       self.assertIsNone(verb.display)

   def test_VerbFromJSONExceptionFlatDisplay(self):
       verb = Verb()
       try:
           verb.fromJSON('{"id":"test", "display":"test"}')
       except LanguageMapInitError:
           self.assertTrue(1)
       else:
           self.assertTrue(0)

   def test_VerbFromJSON(self):
       verb = Verb()
       verb.fromJSON('{"id":"test", "display": {"test":"test"}}')
       self.assertEqual(verb.id, 'test')
       self.assertIsInstance(verb.display, LanguageMap)
       self.assertEqual(len(vars(verb.display)), 1)
       self.assertIn('test', vars(verb.display))

   def test_VerbAsVersion(self):
       verb = Verb()
       verb2 = verb.asVersion("1.0.0")
       self.assertEqual(verb2, verb)

suite = unittest.TestLoader().loadTestsFromTestCase(TestVerb)
unittest.TextTestRunner(verbosity = 2).run(suite)
