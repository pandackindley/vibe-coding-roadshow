# credits/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('select-user/', views.select_user, name='select_user'),
    path('login/<str:username>/', views.login_user, name='login_user'),
    path('landing/', views.landing, name='landing'),
    path('add-cpe/', views.add_cpe_experience, name='add_cpe_experience'),
    path('edit-cpe/<int:pk>/', views.edit_cpe_experience, name='edit_cpe_experience'),
]
