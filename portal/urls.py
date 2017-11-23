from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/', views.students),
    url(r'^projects/', views.projects),
    url(r'^guides/', views.guides),
    url(r'^projectguide', views.projectguide),
    url(r'^projects/', views.projects),
]
