from django.core import serializers

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response

from .models import Project
from .models import Student
from .models import Guide
from .models import ProjectGuide


def index(request):
    return render(request, 'index.html')


def students(request):
    return HttpResponse(serializers.serialize("json", Student.objects.all()))

@login_required
def projects(request):
    return HttpResponse(serializers.serialize("json", Project.objects.all()))
