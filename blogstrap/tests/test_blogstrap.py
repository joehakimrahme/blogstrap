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
import tempfile
import unittest

import blogstrap


class BlogstrapTest(unittest.TestCase):

    def setUp(self):
        super(BlogstrapTest, self).setUp()
        self.application = blogstrap.create_app()
        self.application.config['TESTING'] = True
        self.config = self.application.config
        self.app = self.application.test_client()

    def test_root(self):
        response = self.app.get("/")
        self.assertEqual(204, response.status_code)

    def test_get_article(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        # default type is markdown, so we shouldn't get 'html'
        self.assertNotIn(b'html', response.data)

    def test_get_html_article(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertEqual(200, response.status_code)
        self.assertIn(b'html', response.data)

    def test_get_hidden(self):
        # files starting with '.' are off limit
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix=".blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(404, response.status_code)
        self.assertNotIn(b'html', response.data)

    def test_get_html_hidden(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix=".blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertEqual(404, response.status_code)
        self.assertIn(b'html', response.data)

    def test_get_nonexistent(self):
        response = self.app.get("nonexistent")
        self.assertEqual(404, response.status_code)
        self.assertNotIn(b'html', response.data)

    def test_get_html_nonexistent(self):
        response = self.app.get("nonexistent", headers={
            'Accept': 'text/html'})
        self.assertEqual(404, response.status_code)
        self.assertIn(b'html', response.data)

    def test_overshadow(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        html_filename = self.tempfile.name + ".html"
        with open(html_filename, "w") as f:
            f.write("htmltest")
        markdown_filename = self.tempfile.name + ".md"
        with open(markdown_filename, "w") as f:
            f.write("markdowntest")
        blogpost = os.path.basename(self.tempfile.name)

        response = self.app.get(blogpost, headers={'Accept': 'text/html'})
        self.assertIn(b'htmltest', response.data)
        response = self.app.get(blogpost, headers={'Accept': 'text/markdown'})
        self.assertIn(b'markdowntest', response.data)
        response = self.app.get(blogpost)
        self.assertIn(b'markdowntest', response.data)

        # deleting the extra files
        os.remove(html_filename)
        os.remove(markdown_filename)

    def test_trailing_slashe(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        blogpost = os.path.basename(self.tempfile.name) + "/"
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)

    def test_homepage(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-homepage-")
        self.application.config['HOMEPAGE'] = os.path.basename(
            self.tempfile.name)
        response = self.app.get("/")
        self.assertEqual(302, response.status_code)
        self.assertIn('Location', response.headers)
        response = self.app.get(response.headers['Location'])
        self.assertEqual(200, response.status_code)

    def test_toc(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        with open(self.tempfile.name, "w") as f:
            f.write("{{ toc }}")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertNotIn(b"{{ toc }}", response.data)


if __name__ == '__main__':
    unittest.main()
