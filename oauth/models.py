from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserCodeChefAuth(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()

    def __str__(self):
        return self.user.username