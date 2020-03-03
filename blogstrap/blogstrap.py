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
import argparse
import os

import flask
import mimerender
import six
if six.PY2:
    from exceptions import IOError
    import sys
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')

    import builder
else:
    import blogstrap.builder as builder


class ArticleNotFound(IOError):
    pass


class ArticleHidden(Exception):
    pass


class ArticleReader(object):

    def __init__(self, path):
        try:
            with open(path) as f:
                self.content = "".join(f.readlines())
                self.metadata = {}
        except IOError:
            raise ArticleNotFound(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class DefaultConfig(object):
    AUTHOR = "Blogstrap"
    DESCRIPTION = "Powered By Blogstrap"
    DEBUG = True
    BLOGROOT = "."
    BLOGTITLE = "Powered by Blogstrap"
    DEFAULT_LANG = "en"


# Registering markdown as a valid MIME.
# More info: https://tools.ietf.org/html/rfc7763
mimerender.register_mime('markdown', ('text/markdown',))
mimerender = mimerender.FlaskMimeRender()


def create_app(config_file=None):
    app = flask.Flask(__name__)
    app.config.from_object(DefaultConfig)
    if config_file:
        app.config.from_pyfile(config_file)

    def _context(message=None):
        context = {
            "author": app.config['AUTHOR'],
            "description": app.config['DESCRIPTION'],
            "lang": app.config['DEFAULT_LANG'],
            "title": app.config['BLOGTITLE']
        }
        if message:
            context.update(message['metadata'])
        return context

    def render_html(message):
        return flask.render_template("index.html",
                                     text=message['content'],
                                     **_context(message))

    def render_html_exception(exception):
        return flask.render_template('404.html',
                                     **_context())

    def render_markdown(message):
        return flask.render_template("index.md",
                                     text=message['content'],
                                     **_context(message))

    def render_md_exception(exception):
        return flask.render_template('404.md',
                                     **_context())

    @app.route("/")
    def nothing():
        if 'HOMEPAGE' in app.config:
            return flask.redirect(
                flask.url_for('serve_blog',
                              blogpost=app.config['HOMEPAGE']))
        # no homepage defined return HTTP 204 No Content
        return ('', 204)

    @app.route("/<blogpost>", strict_slashes=False)
    @mimerender.map_exceptions(
        mapping=(
            (ArticleNotFound, '404 Article Not Found'),
            (ArticleHidden, '404 Article Hidden'),
        ),
        default='markdown',
        markdown=render_md_exception,
        html=render_html_exception,
    )
    @mimerender(
        default='markdown',
        html=render_html,
        markdown=render_markdown)
    def serve_blog(blogpost):
        if blogpost.startswith("."):
            raise ArticleHidden()
        root_directory = app.config['BLOGROOT']

        blogpost = "/".join((root_directory, blogpost))
        accept_header = flask.request.headers.get('Accept', [])
        suffix = ""
        if "text/html" in accept_header:
            if os.path.exists(blogpost + ".html"):
                suffix = ".html"
        else:
            if os.path.exists(blogpost + ".md"):
                suffix = ".md"

        blogpost += suffix
        with ArticleReader(blogpost) as article:
            return {
                'message': {
                    'content': article.content,
                    'metadata': article.metadata,
                }
            }
    return app


def build_parser():
    """Builds the argument parser."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Blogstrap commands')
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize the Blogstrap directory')
    init_parser.set_defaults(func=init)
    init_parser.add_argument('-t', '--target',
                             dest='target',
                             type=str,
                             default='.',
                             help='Target folder to generate files in')
    init_parser.add_argument('--no-homepage',
                             action='store_true',
                             default=False,
                             help='if specified, no homepage will be created')
    run_parser = subparsers.add_parser(
        'run', help="Run the Flask development server")
    run_parser.set_defaults(func=run)
    run_parser.add_argument('-c', '--config',
                            dest='config',
                            type=str,
                            default=None,
                            help='path to a config file')

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


def init(args):
    builder.build(args)


def run(args):
    # identify which config file to use first
    config = args.config

    if config is not None:
        # make sure any relative path is resolved relative to the
        # current working dir
        if not os.path.isabs(config):
            config = os.path.join(os.getcwd(), config)
    else:
        # if no config file are defined on the cli, try to look for one
        # in the default location ".blogstrap/blogstrap.conf"
        default_config_path = os.path.join(os.getcwd(),
                                           ".blogstrap/blogstrap.conf")
        if os.path.exists(default_config_path):
            config = default_config_path
    application = create_app(config)
    application.run()
