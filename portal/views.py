from django.core import serializers
from django.contrib.auth.decorators import login_required

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


def projects(request):
    return HttpResponse(serializers.serialize("json", Project.objects.all()))


def guides(request):
    return HttpResponse(serializers.serialize("json", Guide.objects.all()))


def projectguide(request):
    return HttpResponse(serializers.serialize("json", ProjectGuide.objects.raw('SELECT * FROM portal_projectguide join portal_project on portal_projectguide.project = portal_project.name')))
