from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField()
    api_token = models.CharField(max_length=1000, null=True)

    USERNAME_FIELD = 'id'  
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
