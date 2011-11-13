from omcevmembership.models import DBSession
from omcevmembership.models import MyModel

import deform
from deform import Form
from deform import ValidationFailure
import formencode

from translationstring import TranslationStringFactory
_ = TranslationStringFactory('OMCeVmembership')

from fdfgen import forge_fdf
from datetime import datetime

from pyramid.i18n import (
    get_localizer,
    get_locale_name,
    )

DEBUG = True



def why_view(request):
    return {'project':'OMCeVmembership'}

def types_view(request):
    return {'project':'OMCeVmembership'}

def home_view(request):
    """
    front page view,
    display a template with links
    """
    return {'project':'OMCeVmembership'}


import colander
from webhelpers import constants
class Membership(colander.MappingSchema):
    """
    colander schema for membership application form
    """
    lastname = colander.SchemaNode(colander.String())
    #,
    # validator=colander.PlainText(not_empty = True)
    surname  = colander.SchemaNode(colander.String())
    lastname = colander.SchemaNode(colander.String())
    address1 = colander.SchemaNode(colander.String())
    address2 = colander.SchemaNode(colander.String())
    email =  colander.SchemaNode(colander.String())
    phone =  colander.SchemaNode(colander.String())
    country = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.SelectWidget(values=constants.country_codes()),
        )
    #formencode.validators.String(not_empty = True)

def validate_email(address):
    try:
        valid = formencode.validators.Email(not_empty=True).to_python(address)
        return True
    except Exception as message:
        return unicode(message)

def join_membership(request):

    locale = get_localizer(request)
    #if DEBUG: print "-- locale: " + str(locale)

    schema = Membership()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            form.validate(controls)
        except ValidationFailure, e:
            return{'form': e.render()}
        return {'form':'OK'}

    return {'form': form.render()}
    #     print "form was submitted and validated OK."
    #     print "membership_type: " + str(form.data['membership_type'])
    #     if 'supporter' in form.data['membership_type']:
    #         print "found 'supporter'"
    #         membership_fee = 42
    #         FoerderMitglied = True
    #         OrdentlichesMitglied = False
    #     else:
    #         print "'supporter' not found"
    #         membership_fee = 23
    #         FoerderMitglied = 'Off'
    #         OrdentlichesMitglied = 'On'

    #     #print "request.POST: " + str(request.POST)

    #     fields = [
    #         ('Name', form.data['lastname']),
    #         ('Surname', form.data['surname']),
    #         ('Street', form.data['address1']),
    #         ('PostCodeCity', form.data['address2']),
    #         ('Telephone', form.data['phone']),
    #         ('Email', form.data['email']),
    #         ('OrdentlichesMitglied', OrdentlichesMitglied), # not working
    #         ('FoerderMitglied', FoerderMitglied), # not working. < ToDo ^
    #         ]
    #     #generate fdf string
    #     fdf = forge_fdf("", fields, [], [], [])
    #     # write to file
    #     my_fdf_filename = "fdf.fdf"
    #     import os
    #     fdf_file = open(my_fdf_filename , "w")
    #     # fdf_file.write(fdf.encode('utf8'))
    #     fdf_file.write(fdf)
    #     fdf_file.close()

    #     print os.popen('pdftk pdftk/beitrittserklaerung.pdf fill_form %s output formoutput.pdf flatten'% (my_fdf_filename)).read()

    #     #print os.popen('pwd').read()
    #     #print os.popen('ls').read()

    #     # combine
    #     print "combining with bank account form"
    #     print os.popen('pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf').read()
    #     print "combined personal form and bank form"


    #     # return a pdf file
    #     from pyramid.response import Response
    #     response = Response(content_type='application/pdf')
    #     response.app_iter = open("combined.pdf", "r")
    #     return response

    form = form.render()

    return {'form': form}
