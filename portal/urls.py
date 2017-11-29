from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin/$', views.signin),
    url(r'^signout/$', views.signout),

    url(r'^students/$', views.studentsProfile),
    url(r'^students/changePassword/$', views.studentChangePassword),

    url(r'^guide/students/$', views.students),
    url(r'^guide/students/crud/$', views.studentsPage),
    url(r'^guide/students/add/$', views.addStudents),
    url(r'^guide/students/delete/(?P<pk>[0-9]+)/$', views.deleteStudents),
    url(r'^guide/students/update/$', views.updateStudents),

    url('^', include('django.contrib.auth.urls')),
]
