from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('search/<text>', views.resultSearch, name="result")
]
