# Copyright 2014 Rustici Software
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import json
import unittest

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import Attachment, LanguageMap


class AttachmentTest(unittest.TestCase):
    def test_AttachmentInitEmpty(self):
        attachment = Attachment()
        self.assertIsNone(attachment.usage_type)
        self.assertIsNone(attachment.display)
        self.assertIsNone(attachment.content_type)
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)

    def test_AttachmentInitusage_type(self):
        attachment = Attachment(usage_type='test')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertIsNone(attachment.content_type)
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)

    def test_AttachmentInitcontent_type(self):
        attachment = Attachment(usage_type='test', display=None, description=None, content_type='test')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)

    def test_AttachmentInitLength(self):
        attachment = Attachment(usage_type='test', display=None, description=None, content_type='test', length=1)
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertIsNone(attachment.sha2)

    def test_AttachmetInitSha2(self):
        attachment = Attachment(usage_type='test', display=None, description=None, content_type='test', length=1,
                                sha2='test')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')

    def test_AttachmentInitFileURL(self):
        attachment = Attachment(usage_type='test', display=None, description=None, content_type='test', length=1,
                                sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')

    def test_AttachmentInitEmptyDisplay(self):
        attachment = Attachment(usage_type='test', display={}, description=None, content_type='test', length=1,
                                sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsInstance(attachment.display, LanguageMap)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')

    def test_AttachmentInitEmptyDescription(self):
        attachment = Attachment(usage_type='test', display=None, description={}, content_type='test', length=1,
                                sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsInstance(attachment.description, LanguageMap)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')

    def test_AttachmentInitAnonDisplay(self):
        attachment = Attachment(usage_type='test', display={"en-US": "test"}, description=None, content_type='test',
                                length=1, sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')
        self.languageMapVerificationHelper(attachment.display)

    def test_AttachmentInitAnonDescription(self):
        attachment = Attachment(usage_type='test', display=None, description={"en-US": "test"}, content_type='test',
                                length=1, sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')
        self.languageMapVerificationHelper(attachment.description)

    def test_AttachmentInitDisplay(self):
        attachment = Attachment(usage_type='test', display=LanguageMap({"en-US": "test"}), description=None,
                                content_type='test', length=1, sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')
        self.languageMapVerificationHelper(attachment.display)

    def test_AttachmentInitDescription(self):
        attachment = Attachment(usage_type='test', display=None, description=LanguageMap({'en-US': 'test'}),
                                content_type='test', length=1, sha2='test', fileurl='test.com/test.pdf')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')
        self.languageMapVerificationHelper(attachment.description)

    def test_InitUnpackDisplay(self):
        obj = {"display": {"en-US": "test"}}
        attachment = Attachment(**obj)
        self.languageMapVerificationHelper(attachment.display)

    def test_InitUnpackDescription(self):
        obj = {"description": {"en-US": "test"}}
        attachment = Attachment(**obj)
        self.languageMapVerificationHelper(attachment.description)

    def test_InitUnpack(self):
        obj = {"usage_type": "test", "display": {"en-US": "test"}, "description": {"en-US": "test"},
               "content_type": "test", "length": 1, "sha2": "test", "fileurl": "test.com/test.pdf"}
        attachment = Attachment(**obj)
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test.com/test.pdf')
        self.languageMapVerificationHelper(attachment.description)
        self.languageMapVerificationHelper(attachment.display)

    def test_InitExceptionUnpackEmptyusage_type(self):
        obj = {"usage_type": ""}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_InitExceptionUnpackEmptycontent_type(self):
        obj = {"usage_type": "test", "display": {"en-US": "test"}, "description": {"en-US": "test"}, "content_type": ""}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_InitExceptionUnpackEmptySha2(self):
        obj = {"usage_type": "test", "display": {"en-US": "test"}, "description": {"en-US": "test"},
               "content_type": "test", "length": 1, "sha2": ""}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_InitExceptionUnpackEmptyFileurl(self):
        obj = {"usage_type": "test", "display": {"en-US": "test"}, "description": {"en-US": "test"},
               "content_type": "test", "length": 1, "sha2": "test", "fileurl": ""}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_InitExceptionUnpackFlatDisplay(self):
        obj = {"display": "test"}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_InitExceptionUnpackFlatDescription(self):
        obj = {"description": "test"}
        with self.assertRaises(ValueError):
            Attachment(**obj)

    def test_setDisplayExceptionNestedObject(self):
        attachment = Attachment(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(TypeError):
            attachment.display = ({"fr-CA": {"nested": "object"}})
        self.languageMapVerificationHelper(attachment.display)

    def test_setDescriptionExceptionNestedObject(self):
        attachment = Attachment(description=LanguageMap({"en-US": "test"}))
        with self.assertRaises(TypeError):
            attachment.description = ({"fr-CA": {"nested": "object"}})
        self.languageMapVerificationHelper(attachment.description)

    def test_setDisplayExceptionBadMap(self):
        attachment = Attachment(display=LanguageMap({"en-US": "test"}))
        with self.assertRaises(ValueError):
            attachment.display = ({"bad map"})

    def test_setDescriptionExceptionBadMap(self):
        attachment = Attachment(description=LanguageMap({"en-US": "test"}))
        with self.assertRaises(ValueError):
            attachment.description = ({"bad map"})

    def test_FromJSONEmptyObject(self):
        attachment = Attachment.from_json('{}')
        self.assertIsNone(attachment.usage_type)
        self.assertIsNone(attachment.display)
        self.assertIsNone(attachment.description)
        self.assertIsNone(attachment.content_type)
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)
        self.assertIsNone(attachment.fileurl)

    def test_FromJSONExceptionEmpty(self):
        with self.assertRaises(ValueError):
            Attachment.from_json('')

    def test_FromJSONusage_type(self):
        attachment = Attachment.from_json('{"usage_type":"test"}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertIsNone(attachment.description)
        self.assertIsNone(attachment.content_type)
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)
        self.assertIsNone(attachment.fileurl)

    def test_fromJSONcontent_type(self):
        attachment = Attachment.from_json('{"usage_type":"test", "content_type":"test"}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertIsNone(attachment.length)
        self.assertIsNone(attachment.sha2)

    def test_fromJSONLength(self):
        attachment = Attachment.from_json('{"usage_type":"test", "content_type":"test", "length":1}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertIsNone(attachment.sha2)

    def test_fromJSONSha2(self):
        attachment = Attachment.from_json('{"usage_type":"test", "content_type":"test", "length":1, "sha2":"test"}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')

    def test_fromJSONFileUrl(self):
        attachment = Attachment.from_json(
            '{"usage_type":"test", "content_type":"test", "length":1, "sha2":"test", "fileurl":"test"}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertIsNone(attachment.display)
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test')

    def test_fromJSONDisplay(self):
        attachment = Attachment.from_json(
            '{"usage_type":"test", "content_type":"test", "length":1, '
            '"sha2":"test", "fileurl":"test", "display":{"en-US":"test"}}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test')
        self.languageMapVerificationHelper(attachment.display)

    def test_fromJSONDescription(self):
        attachment = Attachment.from_json(
            '{"usage_type":"test", "content_type":"test", "length":1, '
            '"sha2":"test", "fileurl":"test", "display":{"en-US":"test"}, "description":{"en-US":"test"}}')
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test')
        self.languageMapVerificationHelper(attachment.description)
        self.languageMapVerificationHelper(attachment.display)

    def test_AsVersion(self):
        attachment = Attachment()
        attachment2 = attachment.as_version("1.0.0")
        self.assertEqual(attachment2, {})

    def test_ToJSON(self):
        attachment = Attachment(
            **{"usage_type": "test", "content_type": "test", "length": 1, "sha2": "test", "fileurl": "test",
               "display": {"en-US": "test"}, "description": {"en-US": "test"}})
        self.assertEqual(json.loads(attachment.to_json()),
                         json.loads('{"sha2": "test", "contentType": "test", '
                                    '"description": {"en-US": "test"}, '
                                    '"usageType": "test", "length": 1, "fileUrl": "test", '
                                    '"display": {"en-US": "test"}}'))

    def test_ToJSONEmpty(self):
        attachment = Attachment()
        self.assertEqual(attachment.to_json(), '{}')

    def test_ToJSONFromJSON(self):
        json_str = '''{"sha2": "test", "description": {"en-US": "test"}, "usage_type": "test",
        "length": 1, "content_type": "test", "fileurl": "test", "display": {"en-US": "test"}}'''
        attachment = Attachment.from_json(json_str)
        self.assertEqual(attachment.usage_type, 'test')
        self.assertEqual(attachment.content_type, 'test')
        self.assertEqual(attachment.length, 1)
        self.assertEqual(attachment.sha2, 'test')
        self.assertEqual(attachment.fileurl, 'test')
        self.languageMapVerificationHelper(attachment.description)
        self.languageMapVerificationHelper(attachment.display)
        self.assertEqual(
            json.loads(attachment.to_json()),
            json.loads('{"sha2": "test", "contentType": "test", "description": {"en-US": "test"}, '
                       '"usageType": "test", "length": 1, "fileUrl": "test", "display": {"en-US": "test"}}'))

    def languageMapVerificationHelper(self, value):
        self.assertIsInstance(value, LanguageMap)
        self.assertEqual(len(value), 1)
        self.assertIn('en-US', value)
        self.assertEqual(value['en-US'], 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AttachmentTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
