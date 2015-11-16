Blogstrap - yet another static web generator
============================================

Blogstrap is a simple blogging platform based on a few core principles:

* **Version control management tools like git implement a lot of useful features
  for blogging**

I want to publish my articles the same way I publish source code.

* **Readers aren't always visiting in a browser**.

Blogit puts forward markup languages that emphasise human readability, and serve
html only when html is needed.

* **HTML rendering should be done client-side**.

It doesn't make sense for your blog to hold both the markup file and its html
counterpart.

Dependencies
------------

Blogstrap depends on the following 2 projects:

* Flask
* Strapdown.js


Installation
------------

* Available on PyPI:

```
pip install blogstrap
```

* It's still changing fast so we recommend installing from source:

```
python setup.py instsall
```


It's recommended that you install Blogstrap inside a virtualenv or in a
dedicated virtual machine (or cloud instance)


Publish a blog with Blogstrap
-----------------------------

After installing Blogstrap on your machine, here's how you can use it for
blogging. There are multiple ways to host and serve your Flask application, here
we're showing an example of how to do it with `gunicorn`.

* Create a new directory `articles`
* Inside that directory create a file called `wsgi.py`

```
from blogstrap.blogstrap import create_app
application = create_app("/path/to/articles/.blogstrap.conf")
```

* Inside that directory create a file called `.blogstrap.conf`

```
BLOGROOT="/path/to/articles"
BLOGTITLE="My super blog published with Blogstrap"
THEME="simplex"
```

* Create a markdown file in `articles`. Call it `helloworld.md`

*  Serve it over the network:

```
$ gunicorn wsgi:application
```

* Open article in a web browser, at the location `http://<gunicorn_address>/heblloworld`

* Note that you can use `curl` to get the markdown version

```
curl http://<gunicorn_address>/heblloworld
```
