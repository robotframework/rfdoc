# Copyright 2009-2013 Nokia Siemens Networks Oyj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from io import StringIO

from rfdoc.rfdocapp.views.upload import LibraryData, InvalidXmlError


VALID_SPEC = '''
<keywordspec generated="20090428 20:43:40" type="library" name="TestLibrary">
<version>1.0</version>
<doc>This is documentation</doc>
<init>
<doc>Init Doc</doc>
<arguments>
<arg>arg1</arg>
<arg>arg2=default</arg>
</arguments>
</init>
<kw name="KW 1">
<doc>Kw doc</doc>
<arguments>
<arg>arg</arg>
</arguments>
</kw>
<kw name="Keyword 2">
<doc></doc>
<arguments>
</arguments>
</kw>
<kw name="Another Keyword">
<doc></doc>
<arguments>
<arg>arg1</arg>
<arg>arg2=default</arg>
<arg>*args</arg>
</arguments>
</kw>
</keywordspec>
'''


class TestLibraryData(unittest.TestCase):

    def test_parsing_library_data(self):
        data = LibraryData(self._create_input(VALID_SPEC))
        self.assertEqual(data.name, 'TestLibrary')
        self.assertEqual(data.doc, 'This is documentation')
        self.assertEqual(data.version, '1.0')

    def test_parsing_keyword_data(self):
        data = LibraryData(self._create_input(VALID_SPEC))
        expected = [('KW 1', 'Kw doc', 'arg'),
                    ('Keyword 2', '', ''),
                    ('Another Keyword', '', 'arg1, arg2=default, *args')]
        self.assertEqual(len(data.kws), 3)
        for kw, (name, doc, args) in zip(data.kws, expected):
            self.assertEqual(kw.name, name)
            self.assertEqual(kw.doc, doc)
            self.assertEqual(kw.args, args)

    def test_parsing_init_data(self):
        data = LibraryData(self._create_input(VALID_SPEC))
        self.assertEqual(len(data.inits), 1)
        self.assertEqual(data.inits[0].doc, 'Init Doc')
        self.assertEqual(data.inits[0].args, 'arg1, arg2=default')
        self.assertEqual(data.inits[0].name, '<init>')

    def test_parsing_empty_documentations(self):
        data = LibraryData(self._create_input('''
<keywordspec type="library" name="Test">
<doc></doc>
<kw name="KW 1"><doc></doc><arguments/></kw>
</keywordspec>'''))
        self.assertEqual(data.doc, '')
        self.assertEqual(data.kws[0].doc, '')

    def test_parsing_spec_with_incomplete_data_fails(self):
        self._assert_parsing_fails('<keywordspec/>')

    def test_parsing_spec_without_keywords_fails(self):
        self._assert_parsing_fails('<keywordspec type="library" name="Test">'
                                   '<doc></doc></keywordspec>')

    def test_iterating_spec_with_incomplete_keyword_data_fails(self):
        self._assert_parsing_fails('''
<keywordspec name="LibName">
<doc></doc>
<kw name="Another Keyword">
</kw>
</keywordspec>''')

    def test_parsing_non_xml_fails(self):
        self._assert_parsing_fails('This is not xml')

    def test_parsing_invalid_xml_fails(self):
        self._assert_parsing_fails('<invalid_root_tag/>')

    def test_parsing_old_style_library_data(self):
        data = LibraryData(self._create_input('''
<keywordspec type="library" name="Test">
<doc>No version here</doc>
<keywords><kw name="KW 1"><doc>KW 1 doc</doc><arguments/></kw></keywords>
</keywordspec>'''))
        self.assertEqual(data.name, 'Test')
        self.assertEqual(data.doc, 'No version here')
        self.assertEqual(data.version, '<unknown>')
        self.assertEqual(len(data.kws), 1)
        self.assertEqual(data.kws[0].name, 'KW 1')
        self.assertEqual(data.kws[0].doc, 'KW 1 doc')
        self.assertEqual(data.kws[0].args, '')

    def _assert_parsing_fails(self, data):
        self.assertRaises(InvalidXmlError, LibraryData, self._create_input(data))

    def _create_input(self, data):
        return StringIO('<?xml version="1.0" encoding="UTF-8"?>\n' + data.strip())


if __name__ == '__main__':
    unittest.main()

