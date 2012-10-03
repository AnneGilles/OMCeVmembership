# -*- coding: utf-8  -*-
import subprocess
from fdfgen import forge_fdf

from pyramid_mailer.message import Message
from pyramid_mailer.message import Attachment

DEBUG = False


def generate_pdf(appstruct):

    DEBUG = False

    fields = [
        ('Name', appstruct['lastname']),
        ('Surname', appstruct['surname']),
        ('Street', appstruct['address1']),
        ('PostCodeCity', appstruct['address2']),
        ('Telephone', appstruct['phone']),
        ('Email', appstruct['email']),
        ('mitgliedschaftstyp', 1 if appstruct[
                'membership_type'] == 'member' else 2)
        ]
    #generate fdf string
    fdf = forge_fdf("", fields, [], [], [])
    # write to file
    my_fdf_filename = "fdf.fdf"
    import os
    fdf_file = open(my_fdf_filename, "w")
    # fdf_file.write(fdf.encode('utf8'))
    if DEBUG:  # pragma: no cover
        print("== PDFTK: write fdf")
    fdf_file.write(fdf)
    if DEBUG:  # pragma: no cover
        print("== PDFTK: close fdf file")
    fdf_file.close()

    if DEBUG:  # pragma: no cover
        print("== PDFTK: fill_form & flatten")

        print("running pdftk...")
    pdftk_output = subprocess.call([
            'pdftk',
            'pdftk/beitrittserklaerung.pdf',  # input pdf with form fields
            'fill_form', my_fdf_filename,  # fill in values
            'output', 'formoutput.pdf',  # output filename
            'flatten',  # make form read-only
            #'verbose'  # be verbose?
            ])

    if DEBUG:  # pragma: no cover
        print("===== pdftk output ======")
        print(pdftk_output)

    # combine
    if DEBUG:  # pragma: no cover
        print "== PDFTK: combining with bank account form"
    # print os.popen(
    #  'pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf').read()
    os.popen('pdftk formoutput.pdf pdftk/bankaccount.pdf output combined.pdf')
    if DEBUG:  # pragma: no cover
        print "== PDFTK: combined personal form and bank form"
        print("== PDFTK: delete pdf with user data")
    try:
        os.unlink('formoutput.pdf')
        if DEBUG:  # pragma: no cover
            print("== PDFTK: success: deleted formoutput.pdf")
    except OSError, ose:  # pragma: no cover
        print ose
        print("== PDFTK: file not found while trying to delete")
    if DEBUG:  # pragma: no cover
        print("== PDFTK: delete fdf with user data: " + my_fdf_filename)
    try:
        os.unlink(my_fdf_filename)
        if DEBUG:  # pragma: no cover
            print("== PDFTK: success: deleted fdf file")
    except:  # pragma: no cover
        print("== PDFTK: error while trying to delete fdf file")
    # return a pdf file
    from pyramid.response import Response
    response = Response(content_type='application/pdf')
    response.app_iter = open("combined.pdf", "r")
    return response


def generate_csv(appstruct):
    from datetime import date
    # prepare a csv with the supplied data and attach it to the email
    # to ease import of new data sets
    #
    csv = u"%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
        date.today().strftime("%Y-%m-%d"),  # date, e.g. 2012-09-02
        ' ',  # place of signature
        ' ',  # has signature
        unicode(appstruct['lastname']),
        unicode(appstruct['surname']),
        unicode(appstruct['address1']),
        unicode(appstruct['address2']),
        unicode(appstruct['email']),
        unicode(appstruct['phone']),
        unicode(appstruct['country']),
        2 if appstruct['membership_type'] == 'supporter' else 1
        )
    return csv


from omcevmembership.gnupg_encrypt import encrypt_with_gnupg


def accountant_mail(appstruct):

    unencrypted = u"""
we got a new member through the membership form: \n

lastname:   \t\t %s
surname:    \t\t %s
address1:   \t\t %s
address2:   \t\t %s
email:      \t\t %s
phone:      \t\t %s
country:    \t\t %s
type of membership: %s

that's it.. bye!""" % (
        unicode(appstruct['lastname']),
        unicode(appstruct['surname']),
        unicode(appstruct['address1']),
        unicode(appstruct['address2']),
        unicode(appstruct['email']),
        unicode(appstruct['phone']),
        unicode(appstruct['country']),
        unicode(appstruct['membership_type'])
        )

    #print(unencrypted)
    #print(str(type(unencrypted)))

    message = Message(
        subject="[OMC membership] new member",
        sender="noreply@openmusiccontest.org",
        recipients=["c@openmusiccontest.org"],
        body=str(encrypt_with_gnupg((unencrypted)))
        )

    attachment = Attachment("foo.gpg", "application/gpg-encryption",
                            unicode(encrypt_with_gnupg(u"foo to the bär!")))
    # TODO: make attachment contents a .csv
    message.attach(attachment)

    return message
