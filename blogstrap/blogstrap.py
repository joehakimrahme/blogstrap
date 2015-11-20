import exceptions

from flask import abort
from flask import Flask
from flask import render_template
from flask import request


class ArticleNotFound(exceptions.IOError):
    pass


class ArticleReader(object):

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        try:
            with open(self.path) as f:
                return ''.join(f.read())
        except IOError:
            raise ArticleNotFound(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def create_app(config_file=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    @app.route("/")
    def nothing():
        return "SUCCESS"

    @app.route("/<blogpost>")
    def serve_blog(blogpost):
        user_agent = request.headers.get('User-Agent')
        if user_agent:
            iscurl = user_agent.lower().startswith('curl')
        else:
            iscurl = False
        root_directory = app.config['BLOGROOT']
        blogpost = "/".join((root_directory, blogpost))
        try:
            with ArticleReader(blogpost) as article:
                if iscurl:
                    return article
                else:
                    return render_template("strapdown.html",
                                           theme=app.config['THEME'],
                                           text=article,
                                           title=app.config['BLOGTITLE'])
        except ArticleNotFound:
            # need better support for curl
            abort(404)
    return app

if __name__ == "__main__":
        app = create_app('.blogstrap.conf')
        app.run()
