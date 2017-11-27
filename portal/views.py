import json
from django.core import serializers
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response

from .models import Project
from .models import Student
from .models import Guide

from .forms import StudentForm


def index(request):
    return render(request, 'index.html')


def projects(request):
    return HttpResponse(serializers.serialize("json", Project.objects.all()))


def guides(request):
    return HttpResponse(serializers.serialize("json", Guide.objects.all()))


def projectguide(request):
    return HttpResponse(serializers.serialize("json", ProjectGuide.objects.raw('SELECT * FROM portal_projectguide FULL OUTER JOIN portal_project on portal_projectguide.project_id = portal_project.id')))



#Students
def getStudents(request):
	return HttpResponse(serializers.serialize("json", Student.objects.all()))


def addStudents(request):
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			stud_id = request.POST['stud_id']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			branch = request.POST['branch']
			year = request.POST['year']
			student = Student.objects.create(stud_id=stud_id, first_name=first_name, last_name=last_name, branch=branch, year=year)
			return render(request, 'forms/addStudent.html')
	else:
		return render(request, 'forms/addStudent.html')


def deleteStudents(request, pk):
	student = Student.objects.get(pk=pk)
	student.delete()
	return HttpResponse("OK")


def updateStudents(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		student = Student.objects.get(pk=body['pk'])
		student.first_name = body['first_name']
		student.last_name = body['last_name']
		student.branch = body['branch']
		student.year = body['year']
		student.save();
		return HttpResponse("Ok")
		
	return HttpResponse("Not OK")