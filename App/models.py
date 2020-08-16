from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=16)
    location = models.CharField(max_length=255)
