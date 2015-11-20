import os.path
import tempfile
import unittest

import blogstrap


class BlogstrapTest(unittest.TestCase):

    def setUp(self):
        super(BlogstrapTest, self).setUp()
        application = blogstrap.create_app(".blogstrap.conf")
        self.app = application.test_client()

    def test_success(self):
        # This is just a base test
        response = self.app.get("/")
        self.assertIn(b"SUCCESS", response.data)

    def test_get_article(self):
        # Create a tempfile and GET its url
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        self.assertNotIn(b"SUCCESS", response.data)
        self.tempfile.close()

if __name__ == '__main__':
    unittest.main()
