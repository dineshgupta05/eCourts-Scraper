from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/states/', views.api_states, name='api_states'),
    path('api/districts/', views.api_districts, name='api_districts'),
    path('api/complexes/', views.api_complexes, name='api_complexes'),
    path('api/courts/', views.api_courts, name='api_courts'),
    path('api/download/', views.api_download, name='api_download'),
]
