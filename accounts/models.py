from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username