from django.urls import path

from . import printer

urlpatterns = [
    path('mozilla/categories', printer.printCategories , name='index'),
    path('mozilla/', printer.bienvenidoEclispe , name='index'),
    path('mozilla/', printer.bienvenidoEclispe , name='index'),

]