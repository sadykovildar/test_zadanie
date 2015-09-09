# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20150908_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 8, 20, 38, 19, 887030, tzinfo=utc), verbose_name='Дата публикации'),
        ),
    ]
