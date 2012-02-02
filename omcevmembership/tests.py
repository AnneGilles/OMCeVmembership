import unittest
#from pyramid.config import Configurator
from pyramid import testing

from omcevmembership.models import DBSession


def _initTestingDB():
    from sqlalchemy import create_engine
    from omcevmembership.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session


class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        DBSession.remove()
        self.session = _initTestingDB()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_home_view(self):
        from omcevmembership.views import home_view
        request = testing.DummyRequest()
        info = home_view(request)
        self.assertEqual(info['project'], 'OMCeVmembership')

    def test_why_view(self):
        from omcevmembership.views import why_view
        request = testing.DummyRequest()
        info = why_view(request)
        self.assertEqual(info['project'], 'OMCeVmembership')

    def test_types_view(self):
        from omcevmembership.views import types_view
        request = testing.DummyRequest()
        info = types_view(request)
        self.assertEqual(info['project'], 'OMCeVmembership')

    def test_generate_pdf(self):
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
            res = subprocess.check_call(["which", "pdftk"])
            if res == 0:
                # go ahead with the tests
                result = generate_pdf(mock_appstruct)                

                self.assertEquals(result.content_type,
                                  'application/pdf')
                print("size of pdf: " + str(len(result.body)))
                # self.assertTrue(81000 > len(result.body) > 80500)

        except CalledProcessError, cpe:
            print("pdftk not installed. skipping test!")



#    def test_join_membership(self)
