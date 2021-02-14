import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.3'
PACKAGE_NAME = 'pandaserd'
AUTHOR = 'Nabila Abraham'
AUTHOR_EMAIL = 'nabila.abraham@gmail.com'
URL = 'https://github.com/nabsabraham/pandas-erd'

LICENSE = 'MIT License'
DESCRIPTION = 'Create ERD diagrams from pandas dataframes.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pandas'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )