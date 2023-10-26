from django import forms
from .models import *
from django.forms import ModelForm


class AssignedLeguas(forms.ModelForm):
	class Meta:
		model=Action
		fields=('id_user','id_idea','description','name','score','date')
		
		widgets = {
		'name':forms.TextInput(
			attrs={
			'class':'form-control',
					}),
  
  		'date':forms.DateInput (
			attrs={
			'class':'form-control',
					}),

		'score':forms.NumberInput(
				attrs={
					'class':'form-control',
					'id':'score'}),

		'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'placeholder':'Cuéntanos un poco más',
					'id':'description',
					'rows':4, 
					'cols':15,}),
		}



class RegisterPrizeAjax(forms.ModelForm):
	class Meta:
		model = AssignedPrize
		fields = ['id_prize','id_user', ]

		widgets = {			
			#estó aplica para los campos FK no con los manytomany
			'id_prize':forms.Select(
				attrs={
					'class':'form-control',
					'placeholder':'Ingrese el Score',
					'id':'id_prize_crear'
				}
			),
		}

		labels = {
			'id_prize': "Nombre del premio",
			'id_user': "¿A quién vas a asignar el premio?",
		}

	def __init__(self, *args, **kwargs):
		super(RegisterPrizeAjax, self).__init__(*args, **kwargs)
		
		self.fields['id_prize'].required = True
		self.fields['id_user'].queryset = User.objects.none()
		self.fields['id_user'].required = True
		#aplica para los manytomany
		self.fields['id_user'].widget.attrs['id'] = "id_user_crear"
		self.fields['id_user'].widget.attrs['class'] = "form-control"