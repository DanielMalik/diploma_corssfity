from django.contrib import admin
from django.contrib.auth.models import User
from crossfity.models import CoachApplication, Coach, Athlete, WOD_amrap, WOD_emom, WOD_interval, WOD_tabata, WODpersonal

# Register your models here.

@admin.register(CoachApplication)
class CoachApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'certification', 'e_mail', 'phone_number', 'description', 'application_date', 'status')

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):

    list_display = ('user', 'avatar')

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'box')

@admin.register(WOD_amrap)
class WOD_amrap_Admin(admin.ModelAdmin):
    pass

@admin.register(WOD_emom)
class WOD_emom_Admin(admin.ModelAdmin):
    pass

@admin.register(WOD_interval)
class WOD_interval_Admin(admin.ModelAdmin):
    pass

@admin.register(WOD_tabata)
class WOD_tabata_Admin(admin.ModelAdmin):
    pass

@admin.register(WODpersonal)
class WOD_personal_Admin(admin.ModelAdmin):
    pass
