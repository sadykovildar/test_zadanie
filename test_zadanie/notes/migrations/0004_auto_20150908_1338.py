# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20150908_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Дата публикации', default=datetime.datetime(2015, 9, 8, 13, 38, 37, 671463)),
        ),
    ]
