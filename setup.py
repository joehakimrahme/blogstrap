"""A dumb static site generator.
"""

from setuptools import setup

setup(
    name='Blogstrap',
    author="Joe H. Rahme",
    author_email="joehakimrahme@gmail.com",
    version='0.1',
    long_description=__doc__,
    packages=['blogstrap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
