# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.CharField(default='note', max_length=200, choices=[('TODO', 'TODO'), ('note', 'Заметка'), ('memo', 'Памятка'), ('link', 'Ссылка')])),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('uuid_boolean', models.BooleanField(default=False)),
                ('header', models.CharField(verbose_name='Заголовок', max_length=200)),
                ('text', models.TextField(verbose_name='Заметка', null=True, blank=True)),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации', default=datetime.datetime(2015, 9, 8, 13, 16, 59, 372184))),
                ('chosen', models.BooleanField(verbose_name='Избранная', default=False)),
                ('category', models.ForeignKey(verbose_name='Категория', to='notes.Category')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notes',
            },
        ),
    ]
