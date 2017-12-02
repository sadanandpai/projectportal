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


#General
def index(request):
	if request.user.is_authenticated:
		return redirect('/portal/signin/')
	return render(request, 'signin.html')

def signin(request):
	if request.user.is_authenticated:
		if request.user.userinfo.usertype == 'g':
			return redirect('/portal/students/')
		elif user.userinfo.usertype == 's':
			return redirect('/portal/profile/')
	elif request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if user.userinfo.usertype == 'g':
					return render(request, 'forms/studentsManagement.html', {"last_login" : user.last_login})
				elif user.userinfo.usertype == 's':
					return redirect('/portal/students/')
	return render(request, 'signin.html')

def signout(request):
	logout(request)
	return redirect('/')




#Management
@login_required
def guidesManagement(request):
	return render(request, 'forms/guidesManagement.html')

@login_required
def guideProfile(request, username):
	return render(request, 'forms/guideProfile.html')

@login_required
def studentsManagement(request):
	return render(request, 'forms/studentsManagement.html')

@login_required
def studentProfile(request, username):
	return render(request, 'forms/studentProfile.html')

@login_required
def projectsManagement(request):
	return render(request, 'forms/projectsManagement.html')

@login_required
def projectProfile(request, username):
	return render(request, 'forms/projectProfile.html')




#Guides
@login_required
def guides(request, username = False):
	if username == False:
		return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 'g'), use_natural_foreign_keys=True))
	else:
		return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user__username = username), use_natural_foreign_keys=True))

@login_required
def addGuide(request):
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
		user.userinfo.usertype = 'g'
		user.userinfo.branch = body['branch']
		user.userinfo.year = body['year']
		user.save()
		return HttpResponse("Ok")
	else:
		return HttpResponse("Not Ok")

@login_required
def updateGuide(request):
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
def deleteGuide(request, username):
	user = User.objects.get(username = username)
	user.delete()
	return HttpResponse("OK")




#Students
@login_required
def students(request, username = False):
	if username == False:
		return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 's'), use_natural_foreign_keys=True))
	else:
		return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user__username = username), use_natural_foreign_keys=True))

@login_required
def addStudent(request):
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
def updateStudent(request):
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
def deleteStudent(request, username):
	user = User.objects.get(username = username)
	user.delete()
	return HttpResponse("OK")




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
def addProject(request):
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
def updateProject(request):
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
def deleteProject(request, project_id):
	project = Project.objects.get(project_id = project_id)
	project.delete()
	return HttpResponse("OK")


#Profile
@login_required
def profile(request):
	return render(request, 'forms/profile.html')

@login_required
def studentProjectMap(request, username):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		user = User.objects.get(username = username)
		project_id =  body['project_id']
		if project_id == "0":
			user.userinfo.project_id = None
			user.save()
			return HttpResponse("Project unmapped successfully")
		else:
			user.userinfo.project_id = Project.objects.get(project_id = body['project_id'])
			user.save()
			return HttpResponse("Project mapped successfully")
	else:
		return HttpResponse("Invalid attempt. Try again")

@login_required
def changePassword(request):
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

@login_required
def dp_upload(request):
	if request.method == 'POST':
		user = User.objects.get(username = request.POST['username'])
		photo = user.userinfo.photo if user.userinfo.photo.name != "" else ""
		form = ImageUploadForm(request.POST, request.FILES, instance=user.userinfo)
		if form.is_valid():
			form.save()
			if photo:
				photo.delete(save=False)
			return redirect('/portal/students/' + user.username)
		else:
			return redirect('/portal/students/' + user.username)
	return HttpResponseForbidden('Invalid attempt is detected')
