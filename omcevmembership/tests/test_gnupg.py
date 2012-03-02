import unittest
from pyramid import testing

from omcevmembership.models import DBSession


def _initTestingDB():
    from sqlalchemy import create_engine
    from omcevmembership.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session


class TestGnuPG(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        DBSession.remove()
        self.session = _initTestingDB()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_encrypt_with_gnupg(self):
        from omcevmembership.gnupg_encrypt import encrypt_with_gnupg
        result = encrypt_with_gnupg('foo')
        print ("the result: " + str(result))
        self.assertTrue('-----BEGIN PGP MESSAGE-----' in str(result))
        self.assertTrue('-----END PGP MESSAGE-----' in str(result))
