from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.utils import timezone


# Create your models here.

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certification_level1 = models.CharField(max_length=128),
    certification_level2 = models.CharField(max_length=128, null=True, blank=True),
    certification_level3 = models.CharField(max_length=128, null=True, blank=True),
    certification_level4 = models.CharField(max_length=128, null=True, blank=True),
    avatar = models.ImageField(upload_to='static/media', null=True, blank=True)
    affiliate = models.CharField(max_length=128)
    info = models.TextField()
    country = models.CharField(max_length=128)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    # application = models.OneToOneField('CoachApplication')


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

class CoachApplication(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    surname = models.CharField(max_length=128, null=False, blank=False)
    certification = models.CharField(max_length=128, null=False, blank=False)
    e_mail = models.EmailField(max_length=254, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    application_date = models.DateTimeField(default=timezone.now)
    status = models.NullBooleanField()
    pass_mail = models.CharField(max_length=64, null=True, blank=True)
    pass_phone = models.CharField(max_length=64, null=True, blank=True)

