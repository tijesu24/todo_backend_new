import re
from django.urls import path, re_path
from . import views
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api2/users', views.UserCreate.as_view(), name='account-create'),
]
