from django.urls import path

from . import views

#app_name = 'theses-checker'
urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.checkPDF, name='checkPDF'),
    path('<str:pdf_name>', views.show_annotated, name='show_annotated'),
    # path('view/<str:pdf_name>', views.view_annotated, name='view_annotated'), # Use if you in case of small storage - deletes annotated pdf file after user is done with loading that file
]

handler404 = 'theses_checker.views.error_404'
handler500 = 'theses_checker.views.error_500'
handler403 = 'theses_checker.views.error_403'
handler400 = 'theses_checker.views.error_400'
