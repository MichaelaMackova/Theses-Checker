from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files.storage import default_storage
from django.conf import settings


from .bl.theses_checker import Checker
from .bl import auxiliary_functions
import os





def index(request):
    """
    Returns main web page as HTTP Response.
    """
    return render(request, 'theses_checker/index.html')



def checkPDF(request):
    """
    Annotates document given through form and redirects to 'show_annotated'.
    """
    original_pdf_path = default_storage.save(os.path.join(settings.BASE_DIR, 'files', request.FILES['file'].name), request.FILES['file'])
    pdf_name = os.path.basename(original_pdf_path)[:-4]
    pdf_dir = os.path.join(settings.BASE_DIR, 'static')

    pdf_name = auxiliary_functions.generateUniqueFileName(pdf_dir,pdf_name,'pdf')
    
    try:
        checker = Checker(original_pdf_path)
    except:
        exception = "File '" + request.FILES['file'].name + "' could not be opened. Check if your file isn't corrupted."
        return render(request, '500.html', {'exception': exception})
    
    if checker.isFileEmpty():
        exception = "File '" + request.FILES['file'].name + "' could not be parsed. Document does not contain any pages."
        return render(request, '500.html', {'exception': exception})
    
    checker.annotate(os.path.join(pdf_dir, pdf_name))
    del checker
    os.remove(original_pdf_path)
    return HttpResponseRedirect(reverse('show_annotated', args={pdf_name}))



def show_annotated(request, pdf_name):
    """
    Returns web page, where annotated document is shown, as HTTP Response.

    Args:
        pdf_name (str): Name of annotated document, that will be shown.
    """
    return render(request, 'theses_checker/annotated.html', {
        'pdf_name': pdf_name
    })


# X-Frame-Options configured thank to [1], Function taken from [2] and edited
@xframe_options_exempt
def view_annotated(request, pdf_name):
    """
    Returns a PDF file as HTTP Response.

    Args:
        pdf_name (str): Name of the viewed document.
    """
    pdf_path = os.path.join(settings.BASE_DIR, 'static/', pdf_name)
    with open(pdf_path, 'rb') as f:
        pdf_contents = f.read()
    os.remove(pdf_path)
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    return response



def error_404(request, exception):
    """
    Returns an error 404 web page as HTTP Response.
    """
    return render(request, '404.html')



def error_500(request):
    """
    Returns an error 500 web page as HTTP Response.
    """
    return render(request, '500.html')



def error_403(request, exception):
    """
    Returns an error 403 web page as HTTP Response.
    """
    return render(request, '403.html')



def error_400(request, exception):
    """
    Returns an error 400 web page as HTTP Response.
    """
    return render(request, '400.html')






#***************************************************************************************
#    [1]
# 
#    Title: How to configure X-Frame-Options in Django to allow iframe embedding of one view?
#    Author: iankit
#    Last updated: 21.10.2015
#    Cited: 30.3.2022
#    Availability: https://stackoverflow.com/a/33267908
#    Code license: CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/)
#
#***************************************************************************************

#***************************************************************************************
#    [2]
# 
#    Title: Download a file on Django and delete it after return
#    Author: Matthew Pava
#    Last updated: 15.11.2017
#    Cited: 30.3.2022
#    Availability: https://groups.google.com/g/django-users/c/Da8HvVts9pI/m/fwgaFj8RAAAJ
#
#***************************************************************************************
