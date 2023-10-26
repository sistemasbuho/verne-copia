from django.urls import path
from .views import *

urlpatterns = [
    path ('profile/', UserProfileView, name='user_profile'),
    path ('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path ('profile/list_avatar/', ListAvatars, name='edit_avatar'),
    path ('profile/update_avatar/', UpdateAvatar, name='update_avatar'),
    path ('profile/edit_user/<int:pk>/', EditDataProfile.as_view(), name='edit_data'),


]