[![Build Status](https://api.travis-ci.org/joehakimrahme/blogstrap.png)](https://api.travis-ci.org/joehakimrahme/blogstrap)


Blogstrap - A dumb blogging platform
====================================

Blogstrap is a simple blogging platform based on a few core principles:

* **Version control management tools implement a lot of useful
  features for blogging**

Blogstrap doesn't provide an admin application. Instead it expects the user to
manage the underlying file system. It is recommended, but not required, to use
version control systems which provide features like draft publishing (access
control), code review, or history.

I use git and it's worked well for me. So far.

* **HTML belongs in the browser only**.

HTML is a format that belongs only inside the browser. There's no reason to
generate, store or serve HTML outside it. Unless specifically requested,
Blogstrap will generally serve raw markdown content. However if the client
requests HTML (with the `Accept: text/html` header, all popular browsers use
this by default), Blogstrap will serve a Javascript library along the markdown
content so that the html conversion is done on the client side.


How does it work?
-----------------

Blogstrap is a [Flask](http://flask.pocoo.org/) application that serves static
files over the web. It serves raw Markdown files formatted to fit
[Strapdown.js](http://strapdownjs.com/) requirements.

Strapdown.js is downloaded from their CDN and executes the HTML conversion
client side.


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

Create a new file `helloworld` inside the `articles` directory you've just
created:

```markdown
# My new blog!

This is my new blog!
```

Run the app in the development server:

```
$ python newblog/wsgi.py
```

Note that you can use `curl` to get the markdown version:

```
curl http://127.0.0.1:5000/helloworld
```

How do I publish my newly created blog?
---------------------------------------

Blogstrap is built on top of Flask and as such you can use any
method that Flask [supports](http://flask.pocoo.org/docs/0.10/deploying/).

How do I configure my blog?
---------------------------

The initialization command created a `.blogstrap.conf` which you can
adjust based on your needs.
