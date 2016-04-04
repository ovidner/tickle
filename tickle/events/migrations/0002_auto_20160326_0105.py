# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainevent',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organizers.Organizer', verbose_name='organizer'),
        ),
        migrations.AlterUniqueTogether(
            name='mainevent',
            unique_together=set([('organizer', 'name'), ('organizer', 'slug')]),
        ),
    ]