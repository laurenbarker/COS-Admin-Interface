from database import get_all_drafts, get_schema, get_draft, get_draft_obj, get_approval_obj

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_user, login as auth_login, views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import urlsafe_base64_decode

import json
import utils
import httplib as http

from modularodm import Q

from utils import submodule_path, mfr_path, serialize_draft_registration, serialize_draft_registration_approval
import sys
sys.path.insert(0, submodule_path('utils.py'))
from framework.auth.core import User as osf_user
from website.project.model import MetaSchema, DraftRegistrationApproval
from framework.mongo.utils import get_or_http_error

from adminInterface.forms import RegistrationForm, LoginForm
from adminInterface.models import AdminUser
import logging

def get_prereg_users():
	reviewers = []
	users = User.objects.all()
	for reviewer in users:
		if (is_in_prereg_group(reviewer)):
			reviewers.append(str(reviewer.username))
	return reviewers

def is_in_prereg_group(user):
	return user.groups.filter(name='prereg_group').exists()

def is_in_general_administrator_group(user):
	return user.groups.filter(name='general_administrator_group').exists()

@login_required
def home(request):
	context = {'user': request.user}
	return render(request, 'home.html', context)

def register(request):
	if request.user.is_authenticated():
		return redirect('/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = User.objects.create_user(username=username,
				email=email, password=password)
			user.save()
			admin_user = AdminUser(user=user)
			admin_user.save()
			admin_user = authenticate(username=username, password=password)
			auth_login(request, admin_user)
			return redirect('/')
		else:
			context = {'form': form}
			return render(request, 'registration/register.html', context)
	else:
		''' User not submitting form, show blank registrations form '''
		form = RegistrationForm()
		context = {'form': form}
		return render(request, 'registration/register.html', context)

def login(request):
	if request.user.is_authenticated():
		return redirect('/')
	form = LoginForm(request.POST or None)
	if request.POST and form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		admin_user = authenticate(username=username, password=password)
		if admin_user:
			auth_login(request, admin_user)
			return redirect('/')
		else:
			return redirect('/login/')
	context = {'form': form}
	return render(request, 'login.html', context)

def logout(request):
	logout_user(request)
	return redirect('/login/')

def password_reset_done(request, **kwargs):
	messages.success(request, 'You have successfully reset your password and activated your admin account. Thank you')
	return login(request)

def password_reset_confirm_custom(request, **kwargs):
	response = views.password_reset_confirm(request, **kwargs)
	# i.e. if the user successfully resets their password
	if response.status_code == 302:
		try:
			uid = urlsafe_base64_decode(kwargs['uidb64'])
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			pass
		else:
			user.is_active = True
			user.save()
	return response

@login_required
@user_passes_test(is_in_general_administrator_group)
def users(request):
	context = {}
	return render(request, 'users.html', context)

@login_required
@user_passes_test(is_in_prereg_group)
def prereg(request):
	prereg_admin = request.user.has_perm('auth.prereg_admin')
	user = {'username': str(request.user.username), 'admin': json.dumps(prereg_admin)}
	reviewers = get_prereg_users()

	context = {'user_info': user, 'reviewers': reviewers, 'user': request.user}
	return render(request, 'prereg/prereg.html', context)

@login_required
def prereg_form(request, draft_pk):
	draft = get_draft(draft_pk)
	context = {'data': json.dumps(draft)}
	return render(request, 'prereg/edit_draft_registration.html', context)

@login_required
def get_drafts(request):
	all_drafts = get_all_drafts()
	return HttpResponse(json.dumps(all_drafts), content_type='application/json')

@login_required
def get_schemas(request):
	schema = get_schema()
	return HttpResponse(json.dumps(schema), content_type='application/json')

@login_required
@csrf_exempt
def approve_draft(request, draft_pk):

	draft = get_draft_obj(draft_pk)

	# TODO[lauren]: add proper authorizers to DraftRegistrationApproval
	# params for approve function = self, user, and token
	# user should be the admin
	user = osf_user.load('dsmpw')
	draftRegistrationApproval = draft[0].approval

	draftRegistrationApproval.add_authorizer(user)
	token = draftRegistrationApproval.approval_state[user._id]['approval_token']
	draftRegistrationApproval.approve(user, token)
	draftRegistrationApproval.save()

	response = serialize_draft_registration_approval(draftRegistrationApproval)
	return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
@csrf_exempt
def reject_draft(request, draft_pk):
	draft = get_draft_obj(draft_pk)

	# TODO[lauren]: add proper authorizers to DraftRegistrationApproval
	# need to pass self, user, and token
	# user should be the admin
	user = osf_user.load('dsmpw')
	draftRegistrationApproval = draft[0].approval

	draftRegistrationApproval.add_authorizer(user)
	token = draftRegistrationApproval.approval_state[user._id]['rejection_token']

	draftRegistrationApproval.reject(user, token)
	draftRegistrationApproval.save()

	response = serialize_draft_registration_approval(draftRegistrationApproval)
	return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
@csrf_exempt
def update_draft(request, draft_pk):

	get_schema_or_fail = lambda query: get_or_http_error(MetaSchema, query)

	data = json.load(request)

	draft = get_draft_obj(draft_pk)

	schema_data = data['schema_data']

	schema_name = data['schema_name']
	schema_version = data['schema_version']

	if schema_name:
	    meta_schema = get_schema_or_fail(
	        Q('name', 'eq', schema_name) &
	        Q('schema_version', 'eq', schema_version)
	    )

	    existing_schema = draft[0].registration_schema
	    if (existing_schema.name, existing_schema.schema_version) != (meta_schema.name, meta_schema.schema_version):
	        draft[0].registration_schema = meta_schema

	try:
		draft[0].update_metadata(schema_data)
	except (NodeStateError):
	    raise HTTPError(http.BAD_REQUEST)
	response = serialize_draft_registration(draft[0], draft[1])
	return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
@csrf_exempt
def view_file(request, file_name):

	context = {'mfr_path': mfr_path('utils.py'), 'file_name': file_name}
	return render(request, 'prereg/view_file.html', context)
