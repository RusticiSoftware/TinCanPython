from Verb import Verb
from LanguageMap import LanguageMap
test = Verb()
langMap = LanguageMap()
#json_data = '{ \
#               "id": "testId", \
#               "display": { "en-US": { "multi": "part", "object": { "testing": "complete" } } } }'
#json_data = '{ \
#               "id": "testID", \
#               "display": { "en-US": "tested" } \
#             }'
print test
json_data = '{ "id": "testID" }'
test.fromJSON(json_data)
print test
#print test.asVersion("1.0.0")
test2 = Verb('tested', langMap)
print test2
langMap2 = LanguageMap({"en-US":"tested!"})
test2 = Verb('testedAgain', langMap2)
print test2
