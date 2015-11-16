"""A dumb blogging platform based on Strapdown.js
"""

from setuptools import setup

setup(
    name='Blogstrap',
    author="Joe H. Rahme",
    author_email="joehakimrahme@gmail.com",
    version='0.1.1',
    description="A dumb blogging platform based on Strapdown.js",
    long_description=__doc__,
    packages=['blogstrap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
