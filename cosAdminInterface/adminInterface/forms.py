from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from adminInterface.models import AdminUser

class RegistrationForm(ModelForm):
	username = forms.CharField(label=(u'User Name'))
	email = forms.EmailField(label=(u'Email Address'))
	password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = AdminUser
		exclude = ('user',)

class LoginForm(forms.Form):
	username = forms.CharField(label=(u'User Name'))
	password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))