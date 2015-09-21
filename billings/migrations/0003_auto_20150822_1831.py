# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0002_auto_20150822_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountbilling',
            old_name='billing_fact',
            new_name='sign',
        ),
    ]
