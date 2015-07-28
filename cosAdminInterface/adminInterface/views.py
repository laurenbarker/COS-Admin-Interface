from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as logout_user, login as auth_login
from django.shortcuts import render
from adminInterface.forms import RegistrationForm, LoginForm
from adminInterface.models import AdminUser
import logging


def home(request):
	context = {}
	if request.user.is_authenticated():
		context = {'user': request.user}
	return render(request, 'base.html', context)

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
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
			return HttpResponseRedirect('/')
		else:
			#TODO refactor custom validations
			context = {'form': form}
			return render(request, 'register.html', context)
	else:
		''' User not submitting form, show blank registrations form '''
		form = RegistrationForm()
		context = {'form': form}
		return render(request, 'register.html', context)


def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			admin_user = authenticate(username=username, password=password)
			if admin_user is not None:
				auth_login(request, admin_user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/login/')
	form = LoginForm()
	context = {'form': form}
	return render(request, 'login.html', context)

def logout(request):
	logout_user(request)
	return HttpResponseRedirect('/login/')


def prereg(request):
	return render(request, 'prereg/prereg.html', {})

# def analytics(request):
# 	return render(request, 'analytics.html', {})
