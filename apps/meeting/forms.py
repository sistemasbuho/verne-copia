from django import forms
from .models import *
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget



class RegisterComment(forms.ModelForm):
	class Meta:
		model = UserVotes
		fields = ['vote','vote_priority','message']

		widgets = {
      


		'vote':forms.RadioSelect(
				attrs={'class':'checks row',
           				'id' : 'id_vote'}),
					
		'vote_priority':forms.RadioSelect(
				attrs={'class':'checks row',
           				'id' : 'id_vote_priority'}),
  
  		'message':forms.Textarea(
			attrs={'class':'form-control',
					'placeholder':'¿Porqué tomaste esta decisión?',
     				'id' : 'id_message'})

  
				}
		

class RegisterMeetingForm(forms.ModelForm):
	class Meta:
		model = Meeting
		fields = ['name','place','id_idea','user_comitte','date','start_time','end_time']
		widgets = {
			'name':forms.TextInput(
				attrs={	'class':'form-control',
					    'id':'name'}),

			'place':forms.TextInput(
				attrs={
					'class':'form-control',
					}),

			'date':forms.DateInput(
				attrs={'class':'form-control',}),

			'start_time':forms.TimeInput(
				attrs={'class':'form-control',}),

			'end_time':forms.TimeInput(
				attrs={'class':'form-control',}),
}
		
class FileForm(forms.ModelForm):
	class Meta:
		model = Meeting
		fields = ['document_act',]


class MeetingUpdateForm(forms.ModelForm):
	class Meta:
		model=Meeting
		fields = ['name','link_documentation','place','id_idea','user_comitte','date','start_time','end_time']

		widgets = {
			'name':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'name',
					}),

			'link_documentation':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'link_documentation',
					}),

			'place':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'place',
					}),

			'feedback':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'feedback',
					'rows':5, 
					}),	

			'date':forms.DateInput(
				attrs={'class':'form-control',}),

			'start_time':forms.TimeInput(
				attrs={'class':'form-control',}),

			'end_time':forms.TimeInput(
				attrs={'class':'form-control',}),

			

			}

	def __init__(self,*args, **kwargs):
		super(MeetingUpdateForm, self).__init__(*args, **kwargs)
		self.fields['user_comitte'].queryset =  User.objects.none()
		self.fields['id_idea'].queryset = Idea.objects.none()
