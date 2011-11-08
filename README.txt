OMCeVmembership README

setup
=====

create a virtualenv, preferrably with the python 2.7 variant:

$ virtualenv --no-site-packages .

get ready for development:

$ bin/python setup.py develop

this will take a little while and install all necessary dependencies.


run (in development mode)
=========================

$ bin/paster serve development.ini --reload


run (in production mode)
========================

$ bin/paster serve production.ini
