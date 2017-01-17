from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/media', null=True, blank=True)
    affiliate = models.CharField(max_length=128)
    info = models.TextField()
    country = models.CharField(max_length=128)

    # Premium User - can create WOD's for Athletes and give feedbacks on their scores

class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/media', null=True, blank=True)
    box = models.CharField(max_length=128)
    info = models.TextField()
    country = models.CharField(max_length=128)
    birth_date = models.DateField(null=True, blank=True)

    # Regular User - can subscribe to Coach's WODs orcreate PersonalWODs

class WOD_amrap(models.Model):
    pass

class WOD_emom(models.Model):
    pass

class WOD_interval(models.Model):
    pass

class WOD_tabata(models.Model):
    pass

class WODpersonal(models.Model):
    pass