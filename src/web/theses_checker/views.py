from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'theses_checker/index.html', {'text': "Hello world! This is my bachelors theses"})
