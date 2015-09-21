# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0004_accountbilling_transaction_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValitedTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('tranzaction_id', models.CharField(max_length=500)),
                ('is_validated', models.BooleanField()),
            ],
        ),
    ]
