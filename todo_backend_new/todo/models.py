from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)


class Todo (models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')

    def _str_(self):
        return self.title
