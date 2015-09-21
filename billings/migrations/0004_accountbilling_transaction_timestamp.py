# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0003_auto_20150822_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbilling',
            name='transaction_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 26, 10, 21, 0, 220000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
