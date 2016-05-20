# Copyright 2016 Joe H. Rahme <joehakimrahme@gmail.com>
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
import sys

from gabbi import driver
from gabbi import fixture

import blogstrap


TESTS_DIR = "gabbits"


class ArticlesFixture(fixture.GabbiFixture):
    def start_fixture(self):
        a = open("blogstrap-test", "w")
        b = open(".blogstrap-test", "w")
        a.close()
        b.close()

    def stop_fixture(self):
        os.remove("blogstrap-test")
        os.remove(".blogstrap-test")


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader, host=None,
                              intercept=blogstrap.create_app,
                              fixture_module=sys.modules[__name__])
