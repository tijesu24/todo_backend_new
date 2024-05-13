from .views import *
from django.urls import path

urlpatterns = [
	path('', home),
	path('task', postTask),
	path('task/delete/<int:pk>/', deleteTask),
	path('task/mark/<int:pk>/', markCompleted)
]
