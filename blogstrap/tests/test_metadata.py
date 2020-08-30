# Copyright 2020 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import collections
import unittest

from blogstrap.utils import parse_metadata


expected_default = {
    "metadata": {"key1": "value1", "key2": "value2"},
    "content": "lorem zouzou\n"
}
Case = collections.namedtuple('Case', 'name case expected')

ALL_CASES = []


# This is the "base" case. Simple headers are laid out at the top of the file.
case_base = """
# key1: value1
# key2: value2

lorem zouzou
"""
ALL_CASES.append(Case("base", case_base, expected_default))


# Empty case, for sanity
case_empty = ""
expected_empty = {'content': '', 'metadata': {}}
ALL_CASES.append(Case("empty", case_empty, expected_empty))


# In this case, we test that unexpected whitespaces won't break the parser.
case_whitespace = """

#  key1 :   value1

 # key2:         value2
lorem zouzou
"""
ALL_CASES.append(Case("whitespace", case_whitespace, expected_default))


# Metadata should be defined at the top of the file. Any line formatted in a
# metadata pattern within the content should be treated as part of the content
# and not have any metadata significance.
case_trailing_metadata = """
# key1: value1
# key2: value2

lorem zouzou
# key3: value3
"""
expected_trailing_metadata = {
    "metadata": {"key1": "value1", "key2": "value2"},
    "content": "lorem zouzou\n# key3: value3\n"
}
ALL_CASES.append(Case("trailing_metadata",
                      case_trailing_metadata, expected_trailing_metadata))

# Making sure that any trailing metadata doesn't split the input at
# the wrong place.
case_no_metadata_trailing_meta = """
lorem zouzou
# key: value
"""
expected_no_metadata_trailing_meta = {
    "metadata": {},
    "content": "lorem zouzou\n# key: value\n"
}
ALL_CASES.append(Case("no_metadata_trailing_meta",
                      case_no_metadata_trailing_meta,
                      expected_no_metadata_trailing_meta))


# A single misformed metadata should interrupt metadata parsing and insert the
# rest of the file in the content.
case_malformed_metadata = """
# key1: value1
# key2 value2
# key3: value3

lorem zouzou
"""
expected_malformed_metadata = {
    "metadata": {"key1": "value1"},
    "content": "# key2 value2\n# key3: value3\n\nlorem zouzou\n"
}
ALL_CASES.append(Case("malformed_metadata",
                      case_malformed_metadata, expected_malformed_metadata))

# Making sure that no_metadata is okay
case_no_metadata = """lorem zouzou
"""
expected_no_metadata = {
    "metadata": {},
    "content": "lorem zouzou\n"
}
ALL_CASES.append(Case("no_metadata", case_no_metadata, expected_no_metadata))


# Key has to be one word. Value can be multiple words
case_multiple_words = """
# key1: value 1
# key 2: value 2
lorem zouzou
"""
expected_multiple_words = {
    "metadata": {'key1': 'value 1'},
    "content": "# key 2: value 2\nlorem zouzou\n"
}
ALL_CASES.append(
    Case("multiple_words", case_multiple_words, expected_multiple_words))


# Checking that multi-line content is supported
case_multiline_content = """
# key: value
lorem
zouzou
"""
expected_multiline_content = {
    "metadata": {"key": "value"},
    "content": "lorem\nzouzou\n"
}
ALL_CASES.append(Case("multiline_content", case_multiline_content,
                      expected_multiline_content))


class MetadataParserTest(unittest.TestCase):
    # In order to avoid repetition, this class will be populated dynamically at
    # the bottom of this file.
    pass


def test_generator(string, expected):
    def test(self):
        result = parse_metadata(string)
        self.assertEqual(result, expected, result)
    return test


# Dynamically turn all elements of the ALL_CASES list into `test_*` methods of
# our `unittest.TestCase` subclass.
for case in ALL_CASES:
    test_name = 'test_%s' % case.name
    test = test_generator(case.case, case.expected)
    setattr(MetadataParserTest, test_name, test)


if __name__ == "__main__":
    unittest.main()
