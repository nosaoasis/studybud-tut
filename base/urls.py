from django.urls import path
from .views import (
  home, 
  room, 
  create_room, 
  update_room, 
  delete_room, 
  loginPage, 
  logoutPage, 
  register_user,
)

app_name = 'base'

urlpatterns = [
  path('', home, name='home'),
  path('login/', loginPage, name='login'),
  path('logout/', logoutPage, name='logout'),
  path('register/', register_user, name='register'),
  path('room/<str:pk>/', room, name='room'),
  path('create-room/', create_room, name='create-room'),
  path('update-room/<str:pk>/', update_room, name='update-room'),
  path('delete-room/<str:pk>/', delete_room, name='delete-room'),
]