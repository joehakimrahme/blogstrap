[![Build Status](https://api.travis-ci.org/joehakimrahme/blogstrap.png)](https://api.travis-ci.org/joehakimrahme/blogstrap)
Blogstrap - A dumb blogging platform
====================================

Blogstrap is a simple blogging platform based on a few core principles:

* **Version control management tools implement a lot of useful features for
  blogging**

Blogstrap doesn't provide an admin application. Instead it expects the user to manage the underlying file system. It is recommended, but not required, to use version control systems which provide features like draft publishing (access control), code review, or history.

I use git and it's worked well for me. So far.

* **Readers aren't always visiting in a browser**.

Blogstrap puts forward markup languages that emphasise human readability, and
serve html only when html is needed.

* **HTML rendering should be done client-side**.

It doesn't make sense for your blog to hold both the markup file and its html
counterpart. The repo hold the info once, the client can decide how to display
it. 


Hard Dependencies
-----------------

* [Flask](http://flask.pocoo.org/)

Soft Dependencies
-----------------
Blogstrap uses strapdown's javascript files straight from their CDN.

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


Creating a blog with Blogstrap
-----------------------------

Initialize your blog using:

```
$ blogstrap init --target blog
```

This should generate some directories and files:

```
$ tree -a newblog
newblog
├── .blogstrap.conf
├── articles
└── wsgi.py

1 directory, 2 files

```

Create a new article `helloworld.md` in `newblog/articles/`.

```markdown
# My new blog!

This is my new blog!
```

Run the app in the development server

```
$ python newblog/wsgi.py
```

Note that you can use `curl` to get the markdown version

```
curl http://127.0.0.1:5000/helloworld
```

How do I publish my newly created blog?
---------------------------------------

Blogstrap is built on top of Flask and as such you can use any
method that flask [supports](http://flask.pocoo.org/docs/0.10/deploying/).

How do I configure my blog?
---------------------------

The initialization command created a `.blogstrap.conf` which you can
adjust based on your needs.
