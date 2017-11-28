import json
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from .models import Project
from .models import UserInfo

from .forms import StudentForm
from .forms import SigninForm


def index(request):
    return render(request, 'forms/signin.html')


def signin(request):
	if request.user.is_authenticated:
		if user.userinfo.usertype == 'g':
			return redirect('/portal/guide/students/crud/')
		elif user.userinfo.usertype == 's':
			return redirect('/portal/students/')
	elif request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if user.userinfo.usertype == 'g':
					return redirect('/portal/guide/students/crud/')
				elif user.userinfo.usertype == 's':
					return redirect('/portal/students/')
	return render(request, 'forms/signin.html')


def signout(request):
	logout(request)
	return redirect('/')




@login_required
def studentsPage(request):
    return render(request, 'forms/addStudent.html')


@login_required
def students(request):
    return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user__username = 'guide')))



def addStudents(request):
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			username = request.POST['stud_id']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = 'username@email.com'
			password = username
			user = User.objects.create_user(username, email, password)

			user.first_name = first_name
			user.last_name = last_name
			user.userinfo.usertype = 'g'
			user.userinfo.branch = request.POST['branch']
			user.userinfo.year = request.POST['year']
			user.save()

			return render(request, 'forms/addStudent.html')
	else:
		return render(request, 'forms/addStudent.html')


@login_required
def updateStudents(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		student = User.objects.get(pk=body['pk'])
		student.first_name = body['first_name']
		student.last_name = body['last_name']
		student.branch = body['branch']
		student.year = body['year']
		student.save();
		return HttpResponse("Ok")
	return HttpResponse("Not OK")


@login_required
def deleteStudents(request, pk):
	student = Student.objects.get(pk=pk)
	student.delete()
	return HttpResponse("OK")



@login_required
def studentsProfile(request):
    return render(request, 'studentProfile.html')


def projects(request):
    return HttpResponse(serializers.serialize("json", Project.objects.all()))