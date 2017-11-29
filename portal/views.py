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
from django.core.mail import send_mail


def index(request):
	if request.user.is_authenticated:
		return redirect('/portal/signin/')
	return render(request, 'forms/signin.html')


def signin(request):
	if request.user.is_authenticated:
		if request.user.userinfo.usertype == 'g':
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
    return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 's'), use_natural_foreign_keys=True))


@login_required
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
			user.userinfo.usertype = 's'
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
		user = User.objects.get(username = body['pk'])

		return HttpResponse("Ok")
	return HttpResponse("Not OK")


@login_required
def deleteStudents(request, username):
	user = User.objects.get(username = username)
	user.delete()
	return HttpResponse("OK")
	#send_mail('Password reset','Project Portal details','keerthiniab@gmail.com',['sadypai@gmail.com'], fail_silently=False,)



@login_required
def studentsProfile(request):
    return render(request, 'studentProfile.html')


@login_required
def studentChangePassword(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		if request.user.check_password(body['oldpassword']):
			request.user.set_password(body['password'])
			request.user.save()
			return HttpResponse("Password changed successfully")
		else:
			return HttpResponse("Old password field is not right")
	else:
		return HttpResponse("Not a valid POST request")



def projects(request):
    return HttpResponse(serializers.serialize("json", Project.objects.all()))
