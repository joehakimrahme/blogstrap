[![Build Status](https://api.travis-ci.org/joehakimrahme/blogstrap.png)](https://api.travis-ci.org/joehakimrahme/blogstrap)


Blogstrap - An opinionated blogging platform
============================================

Blogstrap is a simple blogging platform based on a few core principles:

* **A blog is just a collection of text files**

A Blogstrap blog is just a directory that contains articles. It should
be readable using common text reading tools, and easily browsable in a
terminal the way that any directory of files can. Blogstrap avoids
complicated directory structures, databases and any other construct
that sacrifices readability of the source.

The only exception is made for Hidden Files, allowing the inclusion of
different configuration files in the directory without turning them
into articles. In particular, it expects a hidden directory
`.blogstrap` that holds the Blogstrap-specific configuration.

* **Version control management tools implement a lot of useful
  features for blogging**

Blogstrap doesn't provide the traditional blogging, like posting an
article or managing user permissions. Instead it expects the user to
manage the files on disk directly and push them to the server using
their favorite tools. It is recommended, but not required, to use
version control systems which provide features like draft publishing
(access control), article review, or history.

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

Blogstrap is a [Flask](https://flask.pocoo.org/) application that
serves static files over the web. The files are expected to be written
in markdown. If the client requests html explicitly, Blogstrap wraps
the file in HTML tags, along with some javascript based on
[Showdown.js](https://showdownjs.com/) to handle client-side conversion
of the text into HTML, as well as some frontend artefacts based on
[Bootstrap](https://getbootstrap.com) to make the page beautitful.


Installation
------------

* Available on PyPI:

```
$ pip install blogstrap
```

* It's still changing fast so I recommend installing from source:

```
$ python setup.py install
```

It's recommended that you install Blogstrap inside a virtualenv or in a
dedicated virtual machine (or cloud instance).


Blogstrap Quickstart
--------------------

Initialize your blog using:

```
$ blogstrap init --target /tmp/newblog
```

This will create the `newblog` directory if it doesn't exist, and use
it as a root for your blog. It should generate a bunch of files.

```
$ tree -a newblog
newblog
├── .blogstrap
│   ├── blogstrap.conf
│   └── wsgi.py
└── homepage_blogstrap

1 directory, 3 files

```

* **homepage_blogstrap** is the first page in your blog and Blogstrap
  is configured to serve it as your homepage.

* **wsgi.py** is the WSGI entry point to your blog. If you don't know
  what this is, it's the file required by web servers to locate your
  content. In practice you will almost never need to modify it.

* **blogstrap.conf** holds the configuration options to manage aspects
  of Blogstrap behavior.


Let's take a closer look at the config file:

```
$ cat newblog/.blogstrap/blogstrap.conf
# The path of a directory that holds the markdown articles
BLOGROOT = "/tmp/newblog"
# The title will be added to the top banner in every page
BLOGTITLE = "Generated with BlogStrap"
# Make the app more verbose when necessary. Don't use in production.
DEBUG = False

# NAVBAR_LINKS = []   # Insert link to these pages in the navbar
# TOC_BLACKLIST = []  # Exclude these pages from the TOC
# STATIC_DIR = "images"
# This page will be displayed at the blog root
HOMEPAGE = homepage_blogstrap
```

Now let's add an article. Create a new file `helloworld` inside the
`newblog` directory you've just created:

```markdown
$ cat helloworld
# My new blog!

This is my new blog!
```

Run the app in the development server:

```
$ blogstrap run
```

You can now access the article using `curl`:

```
$ curl http://127.0.0.1:5000/helloworld
```

Note that if you access `http://127.0.0.1:5000/helloworld` from your
web browser, Blogstrap will generate an html version of the article
instead of the markdown version.


Features
--------

* **Hidden files**: Blogstrap will return a 404 if requesting an
  article with a filename starting with `.`. This should allow you to
  commit dot configuration files like `.git` or `.gitconfig`. without
  fearing them getting accessed. It also ensures that nothing in the
  blogstrap configuration directory (`.blogstrap`) is going to be
  served.

* **Page Variables**: Blogstrap presents page variables that can be
  inserted in your articles. At the time of this writing only `{{ toc
  }}` is available and gets replaced by a Table of Contents

* **Overshadow**: Makes it possible to serve different content for
  markdown and html. If a file exists with the same name and
  `.html`/`.md` suffix, it will be served in priority when requested.

**Overshadow Examples**:

```
.
├── article
└── article.html
```

If `text/html` is requested then `article.html` will be served.
`article` will be served in any other case.

```
.
├── article
└── article.md
```

In this case, if `text/html` is requested then `article` will be
served. `article.md` will be served in any other case.

```
.
├── article
├── article.html
└── article.md
```

In this case, `article` will never be served.

* **Navbar Links**: The optional configuration variable
  **NAVBAR_LINKS** takes a dictionary of link:URL as values and allows
  the creation of links (both internal and external) to be inserted on
  the navbar on every page.

* **TOC blacklist**: The optional configuration variable
  **TOC_BLACKLIST** allows to explicitly remove some pages from the
  `toc` variable.

Serving media files
-------------------

Media files (images, videos, music, ...) should all be hosted inside a
subdir *STATIC_DIR*, by default `images`. It is possible to configure
this directory in the configuration file.

How do I publish my newly created blog?
---------------------------------------

A Blogstrap blog is most likely going to be a source code repository
and should be distributed as such. Readers can download Blogstrap
locally in case they want to read it in their browser.

It's also possible to host your own instance of Blogstrap over the
web. Since it is built on top of Flask you can use any method that
Flask [supports](http://flask.pocoo.org/docs/0.10/deploy).
