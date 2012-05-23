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
    """
    very basic tests for the main views
    """
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
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

#     def test_join_membership_view_nosubmit(self):
#         from omcevmembership.views import join_membership
#         request = testing.DummyRequest(
#             params={
#                 '_LOCALE_': 'en',  # this stopped working with the newly
#                 }  # #              # introduced #  zpt_renderer :-/
#             )
#         print(str(dir(request)))
#         print("request.params: " + str(request.params.get('_LOCALE_')))
#         result = join_membership(request)
#         self.assertTrue('form' in result)

#     def test_join_membership_non_validating(self):
#         from omcevmembership.views import join_membership
#         request = testing.DummyRequest(
#             post={
#                 'submit': True,
#                 '_LOCALE_': 'de'
#                 # lots of values missing
#                 },
#             )
#         result = join_membership(request)

#         self.assertTrue('form' in result)
#         self.assertTrue('There was a problem with your submission'
#                         in str(result))

    def test_join_membership_validating(self):
        """
        check that valid input to the join form produces a pdf
        - with right content type of response
        - with a certain size
        - with appropriate content (form details)
        and a mail would be sent
        """
        from omcevmembership.views import join_membership
        from pyramid_mailer import get_mailer
        request = testing.DummyRequest(
            post={
                'submit': True,
                'lastname': 'LastName',
                'surname': 'SurName',
                'address1': 'Address1',
                'address2': 'Address2',
                'email': 'email@example.com',
                'phone': 'phone',
                '_LOCALE_': 'de',
                'country': 'AF',
                }
            )
        mailer = get_mailer(request)
        # skip test iff pdftk is not installed
        import subprocess
        from subprocess import CalledProcessError
        try:
            res = subprocess.check_call(["which", "pdftk"])
            if res == 0:
                # go ahead with the tests
                result = join_membership(request)

                self.assertEquals(result.content_type,
                                  'application/pdf')
                #print("size of pdf: " + str(len(result.body)))
                # check pdf size
                self.assertTrue(81000 > len(result.body) > 78000)

                # check pdf contents
                content = ""
                from StringIO import StringIO
                resultstring = StringIO(result.body)

                import slate
                content = slate.PDF(resultstring)

                self.assertTrue('LastName' in str(content))
                self.assertTrue('SurName' in str(content))
                self.assertTrue('Address1' in str(content))
                self.assertTrue('Address2' in str(content))
                self.assertTrue('email@example.com' in str(content))
                self.assertTrue('phone' in str(content))
#                self.assertTrue('Afgahnistan' in str(content))

                # check outgoing mails
                self.assertTrue(len(mailer.outbox) == 1)
                self.assertTrue(
                    mailer.outbox[0].subject == "[OMC membership] new member")

        except CalledProcessError, cpe:  # pragma: no cover
            print("pdftk not installed. skipping test!")
            print(cpe)
