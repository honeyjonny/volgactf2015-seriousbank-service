# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBilling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid', models.IntegerField(default=None)),
                ('billing_fact', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='accountbillings',
            name='user',
        ),
        migrations.DeleteModel(
            name='AccountBillings',
        ),
    ]
