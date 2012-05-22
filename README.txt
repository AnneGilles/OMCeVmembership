OMCeVmembership README

setup
=====

create a virtualenv, preferrably with the python 2.7 variant:

$ virtualenv env

activate your new virtualenv:

$ . env/bin/activate

get ready for development:

$ python setup.py develop

this will take a little while and install all necessary dependencies.


run (in development mode)
=========================

$ pserve development.ini --reload


run (in production mode)
========================

$ pserve production.ini
