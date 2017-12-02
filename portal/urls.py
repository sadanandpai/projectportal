from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin/$', views.signin),
    url(r'^signout/$', views.signout),



    url(r'^guides/$', views.guidesManagement),
    url(r'^guides/(?P<project_id>[A-z0-9]+)/$', views.guideProfile),
    url(r'^students/$', views.studentsManagement),
    url(r'^students/(?P<username>[A-z0-9]+)/$', views.studentProfile),    
    url(r'^projects/$', views.projectsManagement),
    url(r'^projects/(?P<project_id>[A-z0-9]+)/$', views.projectProfile),

    url(r'^profile/$', views.profile),
    url(r'^upload/$', views.dp_upload),



    #RESTful APIs
    url(r'^rest/guides/$', views.guides),
    url(r'^rest/guides/add/$', views.addGuide),
    url(r'^rest/guides/update/$', views.updateGuide),
    url(r'^rest/guides/delete/(?P<username>[A-z0-9]+)/$', views.deleteGuide),
    url(r'^rest/guides/(?P<username>[A-z0-9]+)/$', views.guides),

    url(r'^rest/students/$', views.students),
    url(r'^rest/students/add/$', views.addStudent),
    url(r'^rest/students/update/$', views.updateStudent),
    url(r'^rest/students/delete/(?P<username>[A-z0-9]+)/$', views.deleteStudent),
    url(r'^rest/students/(?P<username>[A-z0-9]+)/$', views.students),

    url(r'^rest/projects/$', views.projects),
    url(r'^rest/projects/add/$', views.addProject),
    url(r'^rest/projects/update/$', views.updateProject),
    url(r'^rest/projects/delete/(?P<project_id>[A-z0-9]+)/$', views.deleteProject),
    url(r'^rest/projects/(?P<project_id>[A-z0-9]+)/$', views.projects),

    url(r'^rest/changePassword/$', views.changePassword),
    url(r'^rest/studentProjectMap/(?P<username>[A-z0-9]+)/$', views.studentProjectMap),



    url('^', include('django.contrib.auth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
