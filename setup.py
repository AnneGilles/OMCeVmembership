import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'zope.sqlalchemy',
    'deform',
    'webhelpers',
    'fdfgen',
    'Babel',
    'lingua',
    'webtest',
    'waitress',
    'python-gnupg',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='OMCeVmembership',
      version='0.1',
      description='OMCeVmembership',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Christoph Scheid',
      author_email='c@openmusiccontest.org',
      url='http://www.openmusiccontest.org',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='omcevmembership',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = omcevmembership:main
      """,
      paster_plugins=['pyramid'],
      message_extractors = { '.': [
            ('**.py',   'lingua_python', None ),
            ('**.pt',   'lingua_xml', None ),
            ]},
      )

