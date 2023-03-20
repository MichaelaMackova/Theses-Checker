from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.exceptions import BadRequest


from .bl.theses_checker import Checker
from .bl import auxiliary_functions
import os





def index(request):
    return render(request, 'theses_checker/index.html')



def checkPDF(request):
    original_pdf_path = default_storage.save(os.path.join(settings.BASE_DIR, 'files', request.FILES['file'].name), request.FILES['file'])
    pdf_name = os.path.basename(original_pdf_path)[:-4]
    pdf_dir = os.path.join(settings.BASE_DIR, 'static')

    pdf_name = auxiliary_functions.generateUniqueFileName(pdf_dir,pdf_name,'pdf')
    
    try:
        checker = Checker(original_pdf_path)
    except:
        raise BadRequest("File '" + request.FILES['file'].name + "' could not be opened or parsed. Check if your file isn't corrupted.")
    
    checker.annotate(os.path.join(pdf_dir, pdf_name))
    del checker
    os.remove(original_pdf_path)
    return HttpResponseRedirect(reverse('show_annotated', args={pdf_name}))



def show_annotated(request, pdf_name):
    return render(request, 'theses_checker/annotated.html', {
        'pdf_name': pdf_name
    })



@xframe_options_exempt
def view_annotated(request, pdf_name):
    pdf_path = os.path.join(settings.BASE_DIR, 'static/', pdf_name)
    with open(pdf_path, 'rb') as f:
        pdf_contents = f.read()
    os.remove(pdf_path)
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    return response



def error_404(request, exception):
    return render(request, '404.html')



def error_500(request):
    return render(request, '500.html')



def error_403(request, exception):
    return render(request, '403.html')



def error_400(request, exception):
    return render(request, '400.html')

