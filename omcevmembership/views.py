# -*- coding: utf-8 -*-

#from omcevmembership.models import DBSession
#from omcevmembership.models import MyModel
from pyramid.view import view_config
from pyramid.threadlocal import get_current_request

import deform
#from deform import Form
from deform import (
    ValidationFailure,
    ZPTRendererFactory,
    )
#import formencode

#from translationstring import TranslationStringFactory
from pyramid.i18n import TranslationStringFactory
from pkg_resources import resource_filename


def renderer_factory(request=None):
    translator = request.translate
    renderer_factory = ZPTRendererFactory(
        #search_path=search_path,
        translator=translator)
    return renderer_factory


class Form(deform.Form):

    def __init__(self, request, *args, **kwargs):
        kwargs['renderer'] = renderer_factory(request)
        deform.Form.__init__(self, *args, **kwargs)

_ = TranslationStringFactory('OMCeVmembership')


def translator(term):
    print("this is def translator")
    print(term)
    return get_localizer(get_current_request()).translate(term)

deform_template_dir = resource_filename('omcevmembership', 'templates/')

zpt_renderer = deform.ZPTRendererFactory(
    [deform_template_dir], translator=translator)

# the zpt_renderer above is referred to within the demo.ini file by dotted name

from fdfgen import forge_fdf
#from datetime import datetime

from pyramid.i18n import (
    get_localizer,
    get_locale_name,
    )

DEBUG = True


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

#from pyramid.threadlocal import get_current_request

import colander
from webhelpers import constants


def generate_pdf(appstruct):

    fields = [
        ('Name', appstruct['lastname']),
        ('Surname', appstruct['surname']),
        ('Street', appstruct['address1']),
        ('PostCodeCity', appstruct['address2']),
        ('Telephone', appstruct['phone']),
        ('Email', appstruct['email']),
        ]
    #generate fdf string
    fdf = forge_fdf("", fields, [], [], [])
    # write to file
    my_fdf_filename = "fdf.fdf"
    import os
    fdf_file = open(my_fdf_filename, "w")
    # fdf_file.write(fdf.encode('utf8'))
    fdf_file.write(fdf)
    fdf_file.close()

    os.popen('pdftk pdftk/beitrittserklaerung.pdf fill_form %s output formoutput.pdf flatten'% (my_fdf_filename))

    # combine
    # print "combining with bank account form"
    # print os.popen(
    #  'pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf').read()
    os.popen('pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf')
    # print "combined personal form and bank form"

    # return a pdf file
    from pyramid.response import Response
    response = Response(content_type='application/pdf')
    response.app_iter = open("combined.pdf", "r")
    return response


@view_config(renderer='templates/join.pt',
             route_name='join',
             )
def join_membership(request):

    locale_name = get_locale_name(request)
    _ = TranslationStringFactory('OMCeVmembership')
    if DEBUG:  # pragma: no cover
        #print("dir(request): " + str(dir(request)))
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
                                      widget=deform.widget.SelectWidget(
                                          values=constants.country_codes()),)
        _LOCALE_ = colander.SchemaNode(colander.String(),
                                       widget=deform.widget.HiddenWidget(),
                                       default=locale_name)
        #print "locale_name: " + str(locale_name)

    schema = Membership()
    #deform.Form.set_default_renderer(zpt_renderer)
    #print dir(deform.Form)
    form = deform.Form(schema,
                       #buttons=(_('Submit'),), use_ajax=True)
                       buttons=[deform.Button('submit', _('Submit'))],
                       #use_ajax=True
                       )

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)

            print "the controls: " + str(controls)
            print "the appstruct: " + str(appstruct)
        except ValidationFailure, e:
            print(e)
            #import pdb
            #pdb.set_trace()
            return{'form': e.render(),
                   'foo': 'bar'}

        print "form was submitted and validated OK."
        return generate_pdf(appstruct)
        #return {'form':'OK'}

    #import pdb
    #pdb.set_trace()

    #renderer = zpt_renderer  # settings['omcevmembership.renderer']
    # renderer = config.maybe_dotted(renderer)

    #dir(form)
    #print dir(form.set_zpt_renderer(zpt_renderer))
    #return {'form': form.render()}
    #return {'form': form.renderer('omcevmembership:templates/join.pt')}

    #print("Nachname: " + translator('Surname'))
    #print("dir(_): " + str(dir(_)))
    print("_(Surname)): " + _('Surname'))
    form = form.render()
    return {'form': form}
