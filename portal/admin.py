from django.contrib import admin
from .models import Project
from .models import Student
from .models import Guide
from .models import ProjectGuide

admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Guide)
admin.site.register(ProjectGuide)

