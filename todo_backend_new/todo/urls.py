import re
from django.urls import path, re_path
from . import views
# This is the TokenRefreshView function
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('api2/users', views.UserCreate.as_view(), name='account-create'),
    path("", views.home, name="index"),


    # Authentication
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    # Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
]
