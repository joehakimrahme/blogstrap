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
import os
import tempfile
import unittest

import blogstrap
import six


Case = collections.namedtuple('Case', 'name article config expected')
ALL_CASES = []

article_base = """
{{ author }}
"""
config_base = None
expected_base = """Blogstrap
"""
ALL_CASES.append(Case("base", article_base, config_base, expected_base))

article_conf = """
{{ author }}
"""
config_conf = 'test-conf'
expected_conf = """test-conf
"""
ALL_CASES.append(Case("conf", article_conf, config_conf, expected_conf))

article_meta = """
# author: test-meta
{{ author }}
"""
config_meta = 'test-conf'
expected_meta = """test-meta
"""
ALL_CASES.append(Case("meta", article_meta, config_meta, expected_meta))


class PageVariablesTest(unittest.TestCase):
    # In order to avoid repetition, this class will be populated dynamically at
    # the bottom of this file.
    def setUp(self):
        super(PageVariablesTest, self).setUp()
        self.application = blogstrap.create_app()
        self.application.config['TESTING'] = True
        self.config = self.application.config
        self.app = self.application.test_client()


def test_generator(article, config, expected):
    def test(self):
        _tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="pagevar-test-")
        with open(_tempfile.name, "w") as f:
            f.write(article)
        blogpost = os.path.basename(_tempfile.name)
        if config:
            self.config['AUTHOR'] = config
        response = self.app.get(blogpost)
        if not six.PY2:
            # in PY3, strings are NOT arrays of bytes. In order to do
            # the comparison, we need to create a bytes object.
            # In PY2, bytes and str are equivalent
            _expected = bytes(expected, encoding='utf-8')
        else:
            _expected = expected
        self.assertIn(_expected, response.data)
    return test


# Dynamically turn all elements of the ALL_CASES list into `test_*` methods of
# our `unittest.TestCase` subclass.
for case in ALL_CASES:
    test_name = 'test_%s' % case.name
    test = test_generator(case.article, case.config, case.expected)
    setattr(PageVariablesTest, test_name, test)


if __name__ == "__main__":
    unittest.main()
