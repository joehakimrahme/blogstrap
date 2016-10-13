from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
]

templates_path = ['_templates']

source_suffix = '.md'

master_doc = 'index'

project = u'Blogstrap'
copyright = u'2016, Joe H. Rahme'
author = u'Joe H. Rahme'

version = '0.4.0'
release = '0.4.0'

language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'Blogstrapdoc'
latex_elements = {



}
latex_documents = [
    (master_doc, 'Blogstrap.tex', u'Blogstrap Documentation',
     u'Joe H. Rahme', 'manual'),
]
man_pages = [
    (master_doc, 'blogstrap', u'Blogstrap Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'Blogstrap', u'Blogstrap Documentation',
     author, 'Blogstrap', 'One line description of project.',
     'Miscellaneous'),
]
