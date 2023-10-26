from django import forms
from .models import *

class RegisterActivityForm(forms.ModelForm):
	class Meta:
		model = Activity
		fields = ('name','tool','date','description','score', 'id_user', 'id_idea')
		widgets = {
			'name':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'¿Cúal es el nombre de la actividad?',
					}),

			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'placeholder':'¿Cómo será el desarrollo de la actividad?',
					'rows':4, 
					'cols':15,}),

			'tool':forms.TextInput(
				attrs={
					'class':'form-control',}),

			'date':forms.DateInput(
				attrs={
					'class':'form-control',}),

			'score':forms.NumberInput(
				attrs={
					'class':'form-control',
					'id':'score'}),
			}
			
class FormUpdateActivity(forms.ModelForm):
	class Meta:
		model = Activity
		fields = ('name','tool','date','description','score', 'id_user', 'id_idea','link_documentation')
		widgets = {
			'name':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'¿Cúal es el nombre de la actividad?',
					}),

			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'placeholder':'¿Cómo será el desarrollo de la actividad?',
					'rows':4, 
					'cols':15,}),

			'tool':forms.TextInput(
				attrs={
					'class':'form-control',}),

			'date':forms.DateInput(
				attrs={
					'class':'form-control',}),

			'score':forms.NumberInput(
				attrs={
					'class':'form-control',
					'id':'score'}),

			'link_documentation':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'link_documentation',
					'placeholder':'Ingresa el link de la documentación',
					}),
			}
			

class FileForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('annexed', )
	

class TaskCreateForm(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			('', 'Todos..'),
			(True, 'Completado'),
			(False, 'Por hacer')
		)

		model = Task
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_crear',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_crear',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskCreateForm, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		
		self.fields['complete'].widget.attrs['id'] = "complete_crear"

		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_crear"
		self.fields['user'].queryset =  User.objects.none()


class TaskUpdateForm(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			('', 'Todos..'),
			(True, 'Completado'),
			(False, 'Por hacer')
		)

		model = Task
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_editar',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_editar',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskUpdateForm, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		self.fields['description'].required = True
		

		self.fields['complete'].widget.attrs['id'] = "complete_editar"

		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_editar"
		self.fields['user'].queryset =  User.objects.none()
