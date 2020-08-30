# Copyright 2015 Joe H. Rahme <joehakimrahme@gmail.com>
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
import os
import os.path
import six
import tempfile
import unittest

import blogstrap


def is_html(response):
    # if the response data is served as HTML, then the beginning of
    # the response should be `<html>`.
    return b'html' in response.data


def create_tempfile(prefix="blogstrap-test-", content=None):
    # Helper utility function to create test articles based on the
    # tempfile module.
    _tempfile = tempfile.NamedTemporaryFile(
        dir=".",
        prefix=prefix)
    if content:
        with open(_tempfile.name, "w") as f:
            f.write(content)
    return _tempfile


class BaseTest(unittest.TestCase):

    def setUp(self):
        super(BaseTest, self).setUp()
        self.application = blogstrap.create_app()
        self.config = self.application.config
        self.config['TESTING'] = True
        self.app = self.application.test_client()


class BlogstrapTest(BaseTest):

    def test_root(self):
        response = self.app.get("/")
        self.assertEqual(204, response.status_code)

    def test_get_article(self):
        self.tempfile = create_tempfile()
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        # default type is markdown, so we shouldn't get 'html'
        self.assertFalse(is_html(response))

    def test_get_html_article(self):
        self.tempfile = create_tempfile()
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertEqual(200, response.status_code)
        self.assertTrue(is_html(response))

    def test_get_hidden(self):
        # files starting with '.' are off limit
        self.tempfile = create_tempfile(prefix=".blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(404, response.status_code)
        self.assertFalse(is_html(response))

    def test_get_html_hidden(self):
        self.tempfile = create_tempfile(prefix=".blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertEqual(404, response.status_code)
        self.assertTrue(is_html(response))

    def test_get_nonexistent(self):
        response = self.app.get("nonexistent")
        self.assertEqual(404, response.status_code)
        self.assertFalse(is_html(response))

    def test_get_html_nonexistent(self):
        response = self.app.get("nonexistent", headers={
            'Accept': 'text/html'})
        self.assertEqual(404, response.status_code)
        self.assertTrue(is_html(response))

    def test_trailing_slashe(self):
        self.tempfile = create_tempfile()
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        blogpost = os.path.basename(self.tempfile.name) + "/"
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)

    def test_homepage(self):
        self.tempfile = create_tempfile()
        self.config['HOMEPAGE'] = os.path.basename(
            self.tempfile.name)
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)

    def test_metadata(self):
        self.tempfile = create_tempfile(
            content="# key: value\ncontent")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertNotIn(b"key", response.data)


class OvershadowTest(BaseTest):
    def test_overshadow(self):
        self.tempfile = create_tempfile()
        html_filename = self.tempfile.name + ".html"
        with open(html_filename, "w") as f:
            f.write("htmltest")
        self.addCleanup(os.remove, html_filename)
        markdown_filename = self.tempfile.name + ".md"
        with open(markdown_filename, "w") as f:
            f.write("markdowntest")
        self.addCleanup(os.remove, markdown_filename)
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertIn(b'htmltest', response.data)
        response = self.app.get(blogpost, headers={'Accept': 'text/markdown'})
        self.assertIn(b'markdowntest', response.data)
        response = self.app.get(blogpost)
        self.assertIn(b'markdowntest', response.data)


class TOCTest(BaseTest):
    def test_toc(self):
        self.tempfile = create_tempfile(content="{{ toc }}")
        blogpost = os.path.basename(self.tempfile.name)
        articles = []
        # Create 3 temporary articles and make sure they appear in the
        # {{ toc }}
        for i in range(3):
            _tempfile = open("blogstrap-toc-test-%s" % i, "w")
            _tempfile.close()
            self.addCleanup(os.remove, _tempfile.name)
            _base_name = os.path.basename(_tempfile.name)
            articles.append(_base_name)
        response = self.app.get(blogpost)
        self.assertNotIn(b"{{ toc }}", response.data)
        for name in articles:
            if not six.PY2:
                _name = bytes(name, encoding="utf-8")
            else:
                _name = name
            self.assertIn(_name, response.data)

    def test_toc_hidden(self):
        self.tempfile = create_tempfile(content="{{ toc }}")
        blogpost = os.path.basename(self.tempfile.name)
        _tempfile = open(".blogstrap-toc-test", "w")
        _tempfile.close()
        self.addCleanup(os.remove, _tempfile.name)
        response = self.app.get(blogpost)
        self.assertNotIn(b"{{ toc }}", response.data)
        self.assertNotIn(b".blogstrap-toc-test", response.data)


if __name__ == '__main__':
    unittest.main()
