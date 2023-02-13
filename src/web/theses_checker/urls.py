from django.urls import path

from . import views

#app_name = 'theses-checker'
urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.checkPDF, name='checkPDF'),
    path('<str:pdf_name>', views.show_annotated, name='show_annotated'),
    path('view/<str:pdf_name>', views.view_annotated, name='view_annotated'),
]
