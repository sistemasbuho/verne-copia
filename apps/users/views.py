from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from .models import *
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse



class EditProfileView(PermissionRequiredMixin,UpdateView):
    model = Profile
    form_class=FormUser
    permission_required = 'idea.add_idea'
    template_name = 'users/change_avatar.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self):
        profile,created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class EditDataProfile(PermissionRequiredMixin,UpdateView):
    model = Profile
    form_class=FormUserData
    permission_required = 'idea.add_idea'
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:user_profile')
	

@login_required()
@permission_required('idea.add_idea', raise_exception=True)
def UserProfileView(request):

    if Profile.objects.filter(user=request.user).exists():
        pass
    else:
        Profile.objects.filter(user=request.user, avatar__isnull=True).create(
            user=request.user,
            avatar = 'default-user.png',
            biografy= "Por definir",
            rol_company= "Por definir",
        )

    return render(request, 'users/user_profile.html',
	{'data': Profile.objects.filter(user=request.user),})


@login_required()
@permission_required('idea.add_idea', raise_exception=True)
def ListAvatars(request):
    query=Avatar.objects.all()
    return render(request, 'users/user_avatar.html',
	{'query': query})


@login_required()
@permission_required('idea.add_idea', raise_exception=True)
def UpdateAvatar(request):
	if request.method == 'GET':
		result = request.GET.get('result', None)
		# Any process that you want
	else:
		dato = request.POST['premio_name']
		Profile.objects.filter(user=request.user).update(        
            avatar = dato,
        )
	
	return HttpResponseRedirect(reverse('users:user_profile')) 
  
