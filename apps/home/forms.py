from  apps.idea.models import ExternalIdea
from django import forms


class FormIdeaRegisterExternal(forms.ModelForm):
	class Meta:
		model = ExternalIdea
		fields=['title','description','external_name','external_email','conditions']
		widgets = {
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Dale un gran nombre a tu idea',
					'id':'title' }),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'placeholder':'¿Cómo nació esta idea? ¿Qué problema o necesidad esta resolviendo?',
					'id':'description',
					'rows':4, 
					'cols':15,}),
   
            'external_name':forms.TextInput(
                            attrs={
                                'class':'form-control',
                                'id':'title' }),
            
            'external_email':forms.TextInput(
                            attrs={
                                'class':'form-control',
                                'id':'title' }),
			}