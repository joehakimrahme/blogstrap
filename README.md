[![Build Status](https://api.travis-ci.org/joehakimrahme/blogstrap.png)](https://api.travis-ci.org/joehakimrahme/blogstrap)
Blogstrap - A dumb blogging platform
====================================

Blogstrap is a simple blogging platform based on a few core principles:

* **Version control management tools implement a lot of useful features for
  blogging**

I want to publish my articles the same way I publish source code. Draft review
and Pull Request follow the same workflow and the same tools should be reused.

* **Readers aren't always visiting in a browser**.

Blogstrap puts forward markup languages that emphasise human readability, and
serve html only when html is needed.

* **HTML rendering should be done client-side**.

It doesn't make sense for your blog to hold both the markup file and its html
counterpart. The repo hold the info once, the client can decide how to display
it.


Dependencies
------------

Blogstrap depends on the following 2 projects:

* [Flask](http://flask.pocoo.org/)
* [Strapdown.js](http://strapdownjs.com/)


Installation
------------

* Available on PyPI:

```
pip install blogstrap
```

* It's still changing fast so I recommend installing from source:

```
python setup.py install
```

It's recommended that you install Blogstrap inside a virtualenv or in a
dedicated virtual machine (or cloud instance).


Publish a blog with Blogstrap
-----------------------------

After installing Blogstrap on your machine, here's how you can use it for
blogging. There are multiple ways to host and serve your Flask application, here
I'm showing an example of how to do it with `gunicorn`.

* Create a new directory `articles`
* Inside that directory create a file called `wsgi.py`

```python
from blogstrap.blogstrap import create_app
application = create_app("/path/to/articles/.blogstrap.conf")
```

* Inside that directory create a file called `.blogstrap.conf`

```python
BLOGROOT="/path/to/articles"
BLOGTITLE="My super blog published with Blogstrap"
THEME="simplex"
```

* Create a markdown file in `articles`. Call it `helloworld.md`

*  Serve it over the network:

```
$ gunicorn wsgi:application -b '0.0.0.0'
```

* Open article in a web browser, at the location `http://<gunicorn_address>/heblloworld`

* Note that you can use `curl` to get the markdown version

```
curl http://<gunicorn_address>/helloworld
```
