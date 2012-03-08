# -*- coding: utf-8 -*-

from omcevmembership.utils import (
    generate_pdf,
    accountant_mail,
    )
from pkg_resources import resource_filename
import colander
from webhelpers import constants
import deform
from deform import (
    ValidationFailure,
    #ZPTRendererFactory,
    )

from pyramid.i18n import (
    #TranslationStringFactory,
    get_localizer,
    get_locale_name,
    )
from pyramid.view import view_config
from pyramid.threadlocal import get_current_request
from pyramid_mailer import get_mailer

from translationstring import TranslationStringFactory

deform_templates = resource_filename('deform', 'templates')
omcevmembership_templates = resource_filename('omcevmembership', 'templates')

my_search_path = (deform_templates, omcevmembership_templates)


#def renderer_factory(request=None):
#    print("=== this is renderer_factory")
#    translator = request.translate
#    renderer_factory = ZPTRendererFactory(
#        search_path=search_path,
#        translator=translator)
#    return renderer_factory


#class Form(deform.Form):
#
#    def __init__(self, request, *args, **kwargs):
#        kwargs['renderer'] = renderer_factory(request)
#        deform.Form.__init__(self, *args, **kwargs)

_ = TranslationStringFactory('OMCeVmembership')


def translator(term):
    #print("=== this is def translator")
    return get_localizer(get_current_request()).translate(term)


my_template_dir = resource_filename('omcevmembership', 'templates/')
deform_template_dir = resource_filename('deform', 'templates/')

zpt_renderer = deform.ZPTRendererFactory(
    [
        my_template_dir,
        deform_template_dir,
        ],
    translator=translator,
    )
# the zpt_renderer above is referred to within the demo.ini file by dotted name

DEBUG = False


def why_view(request):
    return {'project': 'OMCeVmembership'}


def types_view(request):
    return {'project': 'OMCeVmembership'}


def home_view(request):
    """
    front page view,
    display a template with links
    """
    return {'project': 'OMCeVmembership'}


@view_config(renderer='templates/join.pt',
             route_name='join',
             )
def join_membership(request):

    locale_name = get_locale_name(request)

    if DEBUG:  # pragma: no cover
        print "-- locale_name: " + str(locale_name)

    class Membership(colander.MappingSchema):
        """
        colander schema for membership application form
        """
        lastname = colander.SchemaNode(colander.String(),
                                       title=_(u"Lastname"))
        surname = colander.SchemaNode(colander.String(),
                                      title=_(u'Surname'))
        address1 = colander.SchemaNode(colander.String(),
                                       title=_(u'Street & No.'))
        address2 = colander.SchemaNode(colander.String(),
                                       title=_(u'Post Code & City'))
        email = colander.SchemaNode(colander.String(),
                                     title=_(u'Email Address'),
                                     validator=colander.Email())
        phone = colander.SchemaNode(colander.String(), title=_(u'Phone'))
        country = colander.SchemaNode(colander.String(),
                                      title=_(u'Country'),
                                      widget=deform.widget.SelectWidget(
                values=constants.country_codes()),)
        _LOCALE_ = colander.SchemaNode(colander.String(),
                                       widget=deform.widget.HiddenWidget(),
                                       default=locale_name)

    schema = Membership()

    form = deform.Form(schema,
                       buttons=[deform.Button('submit', _('Submit'))],
                       use_ajax=True,
                       renderer=zpt_renderer
                       )

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            print(e)
            return{'form': e.render(), }

        # send mail to accountants
        mailer = get_mailer(request)
        mailer.send(accountant_mail(appstruct))

        return generate_pdf(appstruct)
        #return {'form':'OK'}

    html = form.render()

    return {'form': html, }
