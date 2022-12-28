from django.shortcuts import render
from django.http import HttpResponse

from .bl import hyphen
from django.contrib.staticfiles import finders


def index(request):
    hyphen.main(finders.find('document.pdf'))
    return render(request, 'theses_checker/index.html', {'text': "Hello world! This is my bachelors theses"})
