# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-03 21:37
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='static/media')),
                ('box', models.CharField(max_length=128)),
                ('info', models.TextField()),
                ('country', models.CharField(max_length=128)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='static/media')),
                ('affiliate', models.CharField(max_length=128)),
                ('info', models.TextField()),
                ('country', models.CharField(max_length=128)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('sms_code', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoachApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('surname', models.CharField(max_length=128)),
                ('certification', models.CharField(max_length=128)),
                ('e_mail', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('description', models.TextField()),
                ('application_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.NullBooleanField()),
                ('pass_mail', models.CharField(blank=True, max_length=64, null=True)),
                ('pass_phone', models.CharField(blank=True, max_length=64, null=True)),
                ('pass_coach_added', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('brief', models.CharField(blank=True, max_length=128, null=True)),
                ('category', models.CharField(choices=[('OLY', 'OLY - Olympic Weightlifting'), ('GYM', 'GYM Gymnastics'), ('METCON', 'METCON Met-Con')], max_length=15)),
                ('kind', models.CharField(choices=[('AMRAP', 'AMRAP As Many Rounds As Possible'), ('EMOM', 'EMOM Every Minute On Minute'), ('INTERVAL', 'Interval reounds: work:rest'), ('21-15-9', '21-15-9 formula'), ('DIST_ROW', 'Row for time'), ('1RM OLY', '1RM max in OLY movement')], max_length=15)),
                ('rounds', models.SmallIntegerField(blank=True, null=True)),
                ('time_cap', models.SmallIntegerField(blank=True, null=True)),
                ('reps_01', models.SmallIntegerField(blank=True, null=True)),
                ('reps_02', models.SmallIntegerField(blank=True, null=True)),
                ('reps_03', models.SmallIntegerField(blank=True, null=True)),
                ('reps_04', models.SmallIntegerField(blank=True, null=True)),
                ('reps_05', models.SmallIntegerField(blank=True, null=True)),
                ('reps_06', models.SmallIntegerField(blank=True, null=True)),
                ('reps_07', models.SmallIntegerField(blank=True, null=True)),
                ('reps_08', models.SmallIntegerField(blank=True, null=True)),
                ('reps_09', models.SmallIntegerField(blank=True, null=True)),
                ('reps_10', models.SmallIntegerField(blank=True, null=True)),
                ('reps_11', models.SmallIntegerField(blank=True, null=True)),
                ('reps_12', models.SmallIntegerField(blank=True, null=True)),
                ('reps_13', models.SmallIntegerField(blank=True, null=True)),
                ('reps_14', models.SmallIntegerField(blank=True, null=True)),
                ('reps_15', models.SmallIntegerField(blank=True, null=True)),
                ('emom_interval_work', models.SmallIntegerField(blank=True, null=True)),
                ('emom_interval_rest', models.SmallIntegerField(blank=True, null=True)),
                ('score', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_name', models.CharField(max_length=128)),
                ('tool', models.CharField(blank=True, max_length=128, null=True)),
                ('kg', models.FloatField(blank=True, null=True)),
                ('lbs', models.SmallIntegerField(blank=True, null=True)),
                ('poods', models.CharField(blank=True, max_length=32, null=True)),
                ('height_meters', models.CharField(blank=True, max_length=32, null=True)),
                ('height_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('distance_meters', models.SmallIntegerField(blank=True, null=True)),
                ('distance_miles', models.SmallIntegerField(blank=True, null=True)),
                ('calories', models.SmallIntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('OLY', 'OLY - Olympic Weightlifting'), ('GYM', 'GYM Gymnastics'), ('METCON', 'METCON Met-Con')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='WOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_publish', models.DateTimeField(blank=True, null=True)),
                ('score', models.CharField(blank=True, max_length=128, null=True)),
                ('athletes', models.ManyToManyField(blank=True, to='crossfity.Athlete')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crossfity.Coach')),
                ('element_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='WODpersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_publish', models.DateTimeField(blank=True, null=True)),
                ('score', models.CharField(blank=True, max_length=128, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crossfity.Athlete')),
                ('element_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('element_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='crossfity.Element')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='movement',
            unique_together=set([('move_name', 'tool', 'kg', 'lbs', 'poods', 'height_meters', 'height_ft', 'distance_meters', 'distance_miles', 'calories')]),
        ),
        migrations.AddField(
            model_name='element',
            name='move_01',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 01+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_02',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 02+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_03',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 03+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_04',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 04+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_05',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 05+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_06',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 06+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_07',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 07+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_08',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 08+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_09',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 09+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_10',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 10+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_11',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 11+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_12',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 12+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_13',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 13+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_14',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 14+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='move_15',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mov 15+', to='crossfity.Movement'),
        ),
        migrations.AddField(
            model_name='element',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
