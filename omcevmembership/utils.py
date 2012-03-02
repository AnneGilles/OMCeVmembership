from fdfgen import forge_fdf

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
