from django.db import models
from django.contrib.auth.models import User



def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, default='default-user.png',verbose_name=u'Imagen de perfil')
    biografy = models.TextField(null=True, blank=True,default="Por definir",max_length=700,verbose_name=u'Biografía')
    rol_company = models.TextField(null=True, blank=True, default="Por definir",verbose_name=u'Cargo')

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return 'Perfil ' + str(self.user)




class Avatar(models.Model):
    avatar_img = models.ImageField( upload_to='profiles/', default='default-user.png')

    def __str__(self):
        return 'Avatar ' + str(self.avatar_img)
