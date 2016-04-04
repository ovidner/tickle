# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('payments', '0001_initial'),
        ('organizers', '0002_organizer_admins'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Cart', verbose_name='cart'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizers.Organizer', verbose_name='organizer'),
        ),
    ]