from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.users.models import Profile


class FormUser(forms.ModelForm):
	class Meta:
		model = Profile
		fields=['avatar']


class FormUserData(forms.ModelForm):
	class Meta:
		model = Profile
		fields=['biografy','rol_company']

		widgets = {
			'biografy':forms.Textarea(
				attrs={
				'class':'form-control',
						}),
	
			'rol_company':forms.TextInput (
				attrs={
				'class':'form-control',
						}),
		}

	
