from django.core.exceptions import ValidationError

def validar_peso_maximo(value):
	peso_archivo= value.size
	limite_megas = 1024 * 1024
	if peso_archivo > limite_megas:
		raise ValidationError("El tamaño máximo del archivo es de 1 mega")
