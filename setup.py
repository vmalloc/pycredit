import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "pycredit", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIRES = [
    "BeautifulSoup4",
    "Logbook",
    "requests",
    "URLObject",
]

setup(name="pycredit",
      classifiers = [
          "Programming Language :: Python :: 3",
          ],
      description="Library providing programmatic access to credit card statement by multiple providers",
      license="BSD3",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/vmalloc/pycredit",

      install_requires=_INSTALL_REQUIRES,
      scripts=[],
      namespace_packages=[]
      )
