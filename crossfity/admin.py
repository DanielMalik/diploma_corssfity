from django.contrib import admin
from django.contrib.auth.models import User
from crossfity.models import CoachApplication, Coach, Athlete, Movement, Element, WOD, WODpersonal
# Register your models here.

@admin.register(CoachApplication)
class CoachApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'certification', 'e_mail', 'phone_number',
                    'description', 'application_date', 'status')

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):

    list_display = ('user', 'avatar')

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'box')

@admin.register(Movement)
class Movement_Admin(admin.ModelAdmin):

    list_display= ('move_name', 'tool', 'kg', 'lbs', 'poods', 'height_meters', 'height_ft', 'distance_meters',
                   'distance_miles', 'calories', 'category')

@admin.register(Element)
class Element_Admin(admin.ModelAdmin):
    list_display = ('title', 'brief')

@admin.register(WOD)
class WOD_Admin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(WODpersonal)
class WOD_personal_Admin(admin.ModelAdmin):
    pass
