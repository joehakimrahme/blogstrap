import os


APP_TEMPLATE = """import os

from blogstrap import create_app

BASE = os.path.dirname(os.path.abspath(__file__))
config = lambda x: os.path.join(BASE, x)

application = create_app(config('.blogstrap.conf'))

if __name__ == '__main__':
    application.run()
"""

CONF_TEMPLATE = """
BLOGROOT = "."
BLOGTITLE = "Generated with BloGstrap"
THEME = "simplex"
DEBUG = True
"""


def build(args):
    app_path = os.path.join(args.target, 'wsgi.py')
    conf_path = os.path.join(args.target, '.blogstrap.conf')

    if not os.path.exists(args.target):
        os.makedirs(args.target)

    with open(app_path, 'w') as f:
        f.write(APP_TEMPLATE)

    with open(conf_path, 'w') as f:
        f.write(CONF_TEMPLATE)
