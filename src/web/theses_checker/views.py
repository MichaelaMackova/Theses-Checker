import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .bl import hyphen
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
import os
from django.conf import settings


def index(request):
    return render(request, 'theses_checker/index.html', {'text': "Hello world! This is my bachelors theses"})

def checkPDF(request):
    original_pdf_path = default_storage.save(os.path.join(settings.BASE_DIR, 'files', request.FILES['file'].name), request.FILES['file'])
    pdf_name = os.path.basename(original_pdf_path)

    hyphen.annotate(original_pdf_path, os.path.join(settings.BASE_DIR, 'static/'))
    os.remove(original_pdf_path)
    return HttpResponseRedirect(reverse('show_annotated', args={pdf_name}))

def show_annotated(request, pdf_name):
    return render(request, 'theses_checker/annotated.html', {'text': "Hello world! This is my bachelors theses\nThe pdf name is: " + pdf_name})