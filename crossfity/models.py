from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager

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
    sms_code = models.CharField(max_length=32, null=True, blank=True)
    # application = models.OneToOneField('CoachApplication')

    def __str__(self):
        return self.user.username
    # Premium User - can create WOD's for Athletes and give feedbacks on their scores

class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/media', null=True, blank=True)
    box = models.CharField(max_length=128)
    info = models.TextField()
    country = models.CharField(max_length=128)
    birth_date = models.DateField(null=True, blank=True)

    # Regular User - can subscribe to Coach's WODs orcreate PersonalWODs

# fields: tag-multi choices for charts; categories: lift, metcon; type AMRAP,EMOM; kind;
# sort; genre, manner; movements; TimeCap; score; redone; date_released; date_performed; author(owner)

CATEGORIES = (
        ('OLY', 'OLY - Olympic Weightlifting'),
        ('GYM', 'GYM Gymnastics'),
        ('METCON', 'METCON Met-Con'),
    )

KINDS = (
    ('AMRAP', 'AMRAP As Many Rounds As Possible'),
    ('EMOM', 'EMOM Every Minute On Minute'),
    ('INTERVAL', 'Interval reounds: work:rest'),
    ('21-15-9', '21-15-9 formula'),
    ('DIST_ROW', 'Row for time'),
    ('1RM OLY', '1RM max in OLY movement')
)

class Movement(models.Model):
    move_name = models.CharField(max_length=128)
    tool = models.CharField(max_length=128, null=True, blank=True)
    kg = models.FloatField(null=True, blank=True)
    lbs = models.SmallIntegerField(null=True, blank=True)
    poods = models.CharField(max_length=32, null=True, blank=True)
    height_meters = models.CharField(max_length=32, null=True, blank=True)
    height_ft = models.CharField(max_length=32, null=True, blank=True)
    distance_meters = models.SmallIntegerField(null=True, blank=True)
    distance_miles = models.SmallIntegerField(null=True, blank=True)
    calories = models.SmallIntegerField(null=True, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORIES)

    def __str__(self):
        return self.move_name

    class Meta:
        unique_together = ('move_name', 'tool', 'kg', 'lbs', 'poods', 'height_meters', 'height_ft', 'distance_meters',
                           'distance_miles', 'calories')

class Element(models.Model):
    title = models.CharField(max_length=128)
    brief = models.CharField(max_length=128, null=True, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    kind = models.CharField(max_length=15, choices=KINDS)
    tags = TaggableManager()
    rounds = models.SmallIntegerField(null=True, blank=True)
    time_cap = models.SmallIntegerField(null=True, blank=True)
    move_01 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 01+')
    reps_01 = models.SmallIntegerField(null=True, blank=True)
    move_02 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 02+')
    reps_02 = models.SmallIntegerField(null=True, blank=True)
    move_03 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 03+')
    reps_03 = models.SmallIntegerField(null=True, blank=True)
    move_04 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 04+')
    reps_04 = models.SmallIntegerField(null=True, blank=True)
    move_05 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 05+')
    reps_05 = models.SmallIntegerField(null=True, blank=True)
    move_06 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 06+')
    reps_06 = models.SmallIntegerField(null=True, blank=True)
    move_07 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 07+')
    reps_07 = models.SmallIntegerField(null=True, blank=True)
    move_08 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 08+')
    reps_08 = models.SmallIntegerField(null=True, blank=True)
    move_09 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 09+')
    reps_09 = models.SmallIntegerField(null=True, blank=True)
    move_10 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 10+')
    reps_10 = models.SmallIntegerField(null=True, blank=True)
    move_11 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 11+')
    reps_11 = models.SmallIntegerField(null=True, blank=True)
    move_12 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 12+')
    reps_12 = models.SmallIntegerField(null=True, blank=True)
    move_13 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 13+')
    reps_13 = models.SmallIntegerField(null=True, blank=True)
    mov_14 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 14+')
    reps_14 = models.SmallIntegerField(null=True, blank=True)
    move_15 = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='mov 15+')
    reps_15 = models.SmallIntegerField(null=True, blank=True)
    emom_interval_work = models.SmallIntegerField(null=True, blank=True)
    emom_interval_rest = models.SmallIntegerField(null=True, blank=True)
    score = models.CharField(max_length=128, null=True, blank=True)

    @property
    def moves(self):
        list = []
        for i in range(0, self.rounds):
            new = models.ForeignKey(Movement, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
            list.append(new)
        return list

    def __str__(self):
        return self.title

class WOD(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    author = models.ForeignKey(Coach, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_publish = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()
    element_1 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True,  related_name='+')
    element_2 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_3 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_4 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_5 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    athletes = models.ManyToManyField(Athlete, null=True, blank=True)
    score = models.CharField(max_length=128, null=True, blank=True)

    @property
    def elms(self):
        list = [self.element_1, self.element_2, self.element_3, self.element_4, self.element_5]
        return list

class WODpersonal(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    author = models.ForeignKey(Athlete, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_publish = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()
    element_1 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_2 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_3 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_4 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    element_5 = models.ForeignKey(Element, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    score = models.CharField(max_length=128, null=True, blank=True)

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
    pass_coach_added = models.BooleanField(default=False)



