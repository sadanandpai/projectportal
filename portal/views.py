import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
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
from .forms import ImageUploadForm
from django.core.mail import send_mail

from django.conf import settings
from django.core.files.storage import FileSystemStorage


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
					return render(request, 'forms/addStudent.html', {"last_login" : user.last_login})
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
def students(request, username = False):
    if username == False:
    	return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 's'), use_natural_foreign_keys=True))
    else:
    	return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user__username = username), use_natural_foreign_keys=True))

    


@login_required
def addStudents(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		username = body['username']
		first_name = body['first_name']
		last_name = body['last_name']
		email = body['email']
		password = username
		user = User.objects.create_user(username, email, password)

		user.first_name = first_name
		user.last_name = last_name
		user.userinfo.usertype = 's'
		user.userinfo.branch = body['branch']
		user.userinfo.year = body['year']
		user.save()
		return HttpResponse("Ok")
	else:
		return HttpResponse("Not Ok")


@login_required
def updateStudents(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		user = User.objects.get(username = body['username'])
		user.first_name = body['first_name']
		user.last_name = body['last_name']
		user.userinfo.branch = body['branch']
		user.userinfo.year = body['year']
		user.save()
		return HttpResponse("Ok")
	return HttpResponse("Not OK")


@login_required
def deleteStudents(request, username):
	user = User.objects.get(username = username)
	user.delete()
	return HttpResponse("OK")
	#send_mail('Password reset','Project Portal details','keerthiniab@gmail.com',['sadypai@gmail.com'], fail_silently=False,)



@login_required
def viewstudentsProfile(request, username):
    return render(request, 'studentProfile.html')



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



#Projects
@login_required
def projectsPage(request):
    return render(request, 'forms/addProject.html')


@login_required
def projects(request, project_id = False):
    if project_id == False:
    	return HttpResponse(serializers.serialize("json", Project.objects.all()))
    else:
    	return HttpResponse(serializers.serialize("json", Project.objects.filter(project_id = project_id)))


@login_required
def addProjects(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		project_id = body['project_id']
		name = body['name']
		description = body['description']
		branch = body['branch']
		year =  body['year']
		Project.objects.create(project_id = project_id, name = name, description = description, branch = branch, year = year)
		return HttpResponse("Ok")
	else:
		return HttpResponse("Not Ok")


@login_required
def updateProjects(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		project = Project.objects.get(project_id = body['project_id'])
		project.name = body['name']
		project.description = body['description']
		project.branch = body['branch']
		project.year =  body['year']
		project.save()
		return HttpResponse("Ok")
	return HttpResponse("Not OK")


@login_required
def deleteProjects(request, project_id):
	project = Project.objects.get(project_id = project_id)
	project.delete()
	return HttpResponse("OK")


@login_required
def viewProjectsProfile(request, username):
	return render(request, 'studentProfile.html')



def simple_upload(request):
	if request.method == 'POST':
		user = User.objects.get(username = request.POST['username'])

		photo = user.userinfo.photo if user.userinfo.photo.name != "" else ""

		form = ImageUploadForm(request.POST, request.FILES, instance=user.userinfo)
		if form.is_valid():
			form.save()
			if photo:
				photo.delete(save=False)
			return redirect('/portal/guide/students/' + user.username)
		else:
			return redirect('/portal/guide/students/' + user.username)
	return HttpResponseForbidden('Invalid attempt is detected')