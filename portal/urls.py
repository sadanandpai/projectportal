from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/get/', views.getStudents),
    url(r'^students/add/', views.addStudents),
    url(r'^students/update/$', views.updateStudents),
    url(r'^students/delete/(?P<pk>[0-9]+)/$', views.deleteStudents),

    url(r'^projects/', views.projects),
    url(r'^guides/', views.guides),
    url(r'^projectguide', views.projectguide),
    url(r'^projects/', views.projects),
]
