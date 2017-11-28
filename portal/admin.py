from django.contrib import admin

from .models import Project
from .models import UserInfo

admin.site.register(Project)
admin.site.register(UserInfo)
