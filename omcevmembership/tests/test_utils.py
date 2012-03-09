import unittest
from pyramid import testing

from omcevmembership.models import DBSession


def _initTestingDB():
    from sqlalchemy import create_engine
    from omcevmembership.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session


class TestUtilities(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        DBSession.remove()
        self.session = _initTestingDB()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_generate_pdf(self):
        """
        Test pdf generation
        and resulting pdf size
        """
        from omcevmembership.views import generate_pdf

        mock_appstruct = {
            'lastname': 'Gilles',
            'surname': 'Anne',
            'address1': 'Sonnenhang 23',
            'address2': '12345 Musterstadt',
            'phone': '0123 456789',
            'email': 'foo@example.com'
            }

        # a skipTest iff pdftk is not installed
        import subprocess
        from subprocess import CalledProcessError
        try:
            res = subprocess.check_call(["which", "pdftk"], stdout=None)
            if res == 0:
                # go ahead with the tests
                result = generate_pdf(mock_appstruct)

                self.assertEquals(result.content_type,
                                  'application/pdf')
                #print("size of pdf: " + str(len(result.body)))
                # check pdf size
                self.assertTrue(81000 > len(result.body) > 78000)

        except CalledProcessError, cpe:  # pragma: no cover
            print("pdftk not installed. skipping test!")
            print(cpe)

    def test_accountant_mail(self):
        """
        test encryption of email payload
        """
        from omcevmembership.utils import accountant_mail
        my_appstruct = {
            'lastname': 'Doe',
            'surname': 'John',
            'address1': 'In the Middle',
            'address2': 'Of Nowhere',
            'email': 'john@example.com',
            'phone': '007 123 456',
            'country': 'af',
            }
        result = accountant_mail(my_appstruct)
        from pyramid_mailer.message import Message

        self.assertTrue(isinstance(result, Message))
        self.assertTrue('c@openmusiccontest.org' in result.recipients)
        self.assertTrue('-----BEGIN PGP MESSAGE-----' in result.body)
        self.assertTrue('-----END PGP MESSAGE-----' in result.body)
        self.assertTrue('[OMC membership] new member' in result.subject)
        self.assertEquals('noreply@c-3-s.org', result.sender)
