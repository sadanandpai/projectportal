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
from .forms import ReportUploadForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError


#General
def index(request):
	if request.user.is_authenticated:
		return redirect('/portal/signin/')
	return render(request, 'signin.html')

def signin(request):
	#if user is already signed in
	if request.user.is_authenticated:
		if request.user.userinfo.usertype == 'g':
			return redirect('/portal/students/')
		elif request.user.userinfo.usertype == 's':
			return redirect('/portal/profile/')
		elif request.user.is_staff == True:
			return redirect('/portal/guides/')
	#if user is not signed in
	elif request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if user.userinfo.usertype == 'g':
					return render(request, 'guide/studentsManagement.html', {"last_login" : user.last_login})
				elif user.userinfo.usertype == 's':
					return redirect('/portal/profile/')
				elif request.user.is_staff == True:
					return redirect('/portal/guides/')
	#if there are issues while signing in
	return render(request, 'signin.html')

def signout(request):
	logout(request)
	return redirect('/')




#Management
@login_required
def guidesManagement(request):
	if request.user.is_staff == True:
		return render(request, 'admin/guidesManagement.html')
	return HttpResponseForbidden()

@login_required
def guideProfile(request, guide_id):
	if request.user.is_staff == True:
		return render(request, 'admin/guideProfile.html')

@login_required
def studentsManagement(request):
	if request.user.userinfo.usertype == 'g':
		return render(request, 'guide/studentsManagement.html')
	return HttpResponseForbidden()

@login_required
def studentProfile(request, username):
	return render(request, 'guide/studentProfile.html')

@login_required
def projectsManagement(request):
	return render(request, 'guide/projectsManagement.html')

def search(request):
	return render(request, 'projectSearch.html')

def projectSearch(request):
	project_id = request.GET.get('project_id', '')
	branch = request.GET.get('branch', '')
	name = request.GET.get('name', '')
	year = request.GET.get('year', '')

	querySet = Project.objects.filter(project_id__contains = project_id, branch__contains = branch, name__contains = name, year__contains = year)
	return HttpResponse(serializers.serialize("json", querySet, use_natural_foreign_keys=True))

@login_required
def projectProfile(request, project_id):
	if Project.objects.filter(user = request.user, project_id = project_id).count() > 0:
		return render(request, 'guide/projectProfile.html')
	elif request.user.userinfo.usertype == 's':
		if UserInfo.objects.get(user = request.user).project.project_id == project_id:
			return render(request, 'student/projectProfile.html')
	elif request.user.is_staff == True:
			return render(request, 'admin/projectProfile.html')
	return HttpResponseForbidden()




#Guides
@login_required
def guides(request, username = False):
	if request.user.is_staff == True:
		if username == False:
			return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 'g'), use_natural_foreign_keys=True))
		else:
			return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user__username = username), use_natural_foreign_keys=True))
	return HttpResponseForbidden()

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
	if request.user.userinfo.usertype == 'g':
		if username == False:
			return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(usertype = 's', branch = request.user.userinfo.branch), use_natural_foreign_keys=True))
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
	return render(request, 'guide/addProject.html')

@login_required
def projects(request, project_id = False):
	if request.user.userinfo.usertype == 'g':
		if project_id == False:
			return HttpResponse(serializers.serialize("json", Project.objects.filter(branch = request.user.userinfo.branch, user = request.user), use_natural_foreign_keys=True))
		else:
			if Project.objects.filter(user = request.user, project_id = project_id).count() > 0:
				return HttpResponse(serializers.serialize("json", Project.objects.filter(project_id = project_id), use_natural_foreign_keys=True))
	elif request.user.userinfo.usertype == 's':
		if UserInfo.objects.get(user = request.user).project.project_id == project_id:
			return HttpResponse(serializers.serialize("json", Project.objects.filter(project_id = project_id), use_natural_foreign_keys=True))
	elif request.user.is_staff == True:
		return HttpResponse(serializers.serialize("json", Project.objects.filter(project_id = project_id), use_natural_foreign_keys=True))
	return HttpResponseForbidden()

@login_required
def addProject(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		project_id = body['project_id']
		name = body['name']
		description = body['description']
		branch = body['branch']
		year =  body['year']
		Project.objects.create(project_id = project_id, name = name, description = description, branch = branch, year = year, user = request.user)
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
	if request.user.userinfo.usertype == 'g':
		return render(request, 'guide/guideProfile.html')
	elif request.user.userinfo.usertype == 's':
		return render(request, 'student/studentProfile.html')

@login_required
def profileUser(request):
	return HttpResponse(serializers.serialize("json", UserInfo.objects.filter(user = request.user), use_natural_foreign_keys=True))


@login_required
def studentProjectMap(request, username):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		user = User.objects.get(username = username)
		project_id =  body['project_id']
		if project_id == "0":
			ppp = user.userinfo.project_id
			Project.objects.get(pk = ppp).users.remove(user)
			user.userinfo.project_id = None
			user.save()
			return HttpResponse("Project unmapped successfully")
		else:
			Project.objects.get(project_id = project_id).users.add(user)
			user.userinfo.project_id = Project.objects.get(project_id = project_id)
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
			return redirect('/portal/profile/')
		else:
			return redirect('/portal/students/')
	return HttpResponseForbidden('Invalid attempt is detected')




@login_required
def document_upload(request, project_id):
	if request.method == 'POST' and request.FILES['file']:
		myfile = request.FILES['file']
		fs = FileSystemStorage()
		#To check the format of the file being uploaded
		ext = myfile.name.split(".")[1]
		valid_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xlsx', 'xls', 'ppt', 'pptx']
		if not ext.lower() in valid_extensions:
			return HttpResponse('<h1>Unsupported file extension. Please try with valid file format</h1>')

		filename = fs.save(project_id + "_" + myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
	return redirect('/portal/projects/'+project_id)


@login_required
def documents(request, project_id):
	if request.method == 'GET':
		fs = FileSystemStorage()
		file_list = fs.listdir(settings.MEDIA_ROOT)
		docs = [file for file in file_list[1] if project_id in file]
		return HttpResponse(json.dumps(docs))


@login_required
def documentDelete(request, project_id, doc_name):
	if request.method == 'GET':
		if request.user.userinfo.usertype == 'g':
			if doc_name.startswith(project_id):
				if Project.objects.filter(user = request.user, project_id = project_id).count() > 0:
					fs = FileSystemStorage()
					fs.delete(doc_name)
					return redirect('/portal/projects/'+project_id)
	return HttpResponseForbidden()



#to get all the projects of a guide
def guideProjects(request, guide_id):
	return HttpResponse(serializers.serialize("json", Project.objects.filter(user = User.objects.get(username = guide_id))))