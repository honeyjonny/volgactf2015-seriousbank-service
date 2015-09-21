# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0005_valitedtransaction'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ValitedTransaction',
            new_name='ValidatedTransaction',
        ),
    ]
