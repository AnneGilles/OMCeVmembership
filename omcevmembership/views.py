from omcevmembership.models import DBSession
from omcevmembership.models import MyModel

import formencode
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from fdfgen import forge_fdf
from datetime import datetime

from pyramid.i18n import (
    get_localizer,
    get_locale_name,
    )

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


class MembershipSchema(formencode.Schema):
    """
    formencode schema for membership application form
    """
    allow_extra_fields = True
    lastname = formencode.validators.PlainText(not_empty = True)
    surname  = formencode.validators.String(not_empty = True)
    lastname = formencode.validators.String(not_empty = True)
    address1 = formencode.validators.String(not_empty = True)
    address2 = formencode.validators.String(not_empty = True)
    email =  formencode.validators.Email(not_empty = True)
    phone =  formencode.validators.String(not_empty = True)


def join_membership(request):

    locale = get_localizer(request)

    print "-- locale: " + str(locale)
    #print "-- dir(locale): " + str(dir(locale))
    #print "-- help(locale): " + str(help(locale))
    print "-- locale.locale_name: " + locale.locale_name

    locale_name = get_locale_name(request)
    print "-- locale_name: " + str(locale_name)
    #print "-- dir(locale_name): " + str(dir(locale_name))
    #print "-- help(locale): " + str(help(locale))
    #print "-- locale_name.locale_name: " + locale.locale_name


    form = Form(request, schema = MembershipSchema)

    if form.validate():
        print "the form validated OK"

    if 'form.submitted' in request.POST and form.validate():
        print "form was submitted and validated OK."
        print "membership_type: " + str(form.data['membership_type'])
        if 'supporter' in form.data['membership_type']:
            print "found 'supporter'"
            membership_fee = 42
            FoerderMitglied = True
            OrdentlichesMitglied = False
        else:
            print "'supporter' not found"
            membership_fee = 23
            FoerderMitglied = 'Off'
            OrdentlichesMitglied = 'On'

        #print "request.POST: " + str(request.POST)

        fields = [
            ('Name', form.data['lastname']),
            ('Surname', form.data['surname']),
            ('Street', form.data['address1']),
            ('PostCodeCity', form.data['address2']),
            ('Telephone', form.data['phone']),
            ('Email', form.data['email']),
            ('OrdentlichesMitglied', OrdentlichesMitglied), # not working
            ('FoerderMitglied', FoerderMitglied), # not working. < ToDo ^
            ]
        #generate fdf string
        fdf = forge_fdf("", fields, [], [], [])
        # write to file
        my_fdf_filename = "fdf.fdf"
        import os
        fdf_file = open(my_fdf_filename , "w")
        # fdf_file.write(fdf.encode('utf8'))
        fdf_file.write(fdf)
        fdf_file.close()

        print os.popen('pdftk pdftk/beitrittserklaerung.pdf fill_form %s output formoutput.pdf flatten'% (my_fdf_filename)).read()

        #print os.popen('pwd').read()
        #print os.popen('ls').read()

        # combine
        print "combining with bank account form"
        print os.popen('pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf').read()
        print "combined personal form and bank form"


        # return a pdf file
        from pyramid.response import Response
        response = Response(content_type='application/pdf')
        response.app_iter = open("combined.pdf", "r")
        return response




    return {
        'form': FormRenderer(form)
        }
