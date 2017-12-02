from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin/$', views.signin),
    url(r'^signout/$', views.signout),

    url(r'^students/$', views.studentsProfile),
    url(r'^students/(?P<username>[A-z0-9]+)/$', views.students),
    url(r'^students/changePassword/$', views.studentChangePassword),

    url(r'^guide/students/$', views.students),
    url(r'^guide/students/crud/$', views.studentsPage),
    url(r'^guide/students/add/$', views.addStudents),
    url(r'^guide/students/delete/(?P<username>[A-z0-9]+)/$', views.deleteStudents),
    url(r'^guide/students/update/$', views.updateStudents),
    url(r'^guide/students/(?P<username>[A-z0-9]+)/$', views.viewstudentsProfile),


    url(r'^guide/projects/$', views.projects),
    url(r'^guide/projects/crud/$', views.projectsPage),
    url(r'^guide/projects/add/$', views.addProjects),
    url(r'^guide/projects/delete/(?P<project_id>[A-z0-9]+)/$', views.deleteProjects),
    url(r'^guide/projects/update/$', views.updateProjects),
    url(r'^guide/projects/(?P<project_id>[A-z0-9]+)/$', views.viewProjectsProfile),

    url(r'^upload/$', views.simple_upload),


    url('^', include('django.contrib.auth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
