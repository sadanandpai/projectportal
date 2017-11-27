from django.contrib import admin
from .models import Project
from .models import Student
from .models import Guide

admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Guide)

