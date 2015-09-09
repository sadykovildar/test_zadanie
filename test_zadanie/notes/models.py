# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone


class Category(models.Model):
    category = models.CharField(max_length=200,
                                default='Заметка',
                                blank=False,
                                null=False)

    def __str__(self):
        return '%s' % self.category

    def create(cat):
        return Category(category=cat)


class Note(models.Model):
    class Meta:
        db_table = 'notes'
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid_boolean = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    header = models.CharField('Заголовок', max_length=200)
    text = models.TextField("Заметка", blank=True, null=True)
    pub_date = models.DateTimeField(u'Дата публикации', default=timezone.now())
    category = models.ForeignKey(Category, verbose_name='Категория')
    chosen = models.BooleanField(u'Избранная', default=False)

    def __str__(self):
        return '%s' % self.header

    def get_absolute_url(self):
        return reverse('one_note', args=[str(self.uuid)])

    def display_my_safefield(self):
        return mark_safe(self.text)

    def get_username(self):
        return str(self.username)

    def as_dict(self):
        return {
            'uuid': str(self.uuid),
            'user': str(self.user),
            'header': self.header,
            'text': self.text,
            'pub_date': self.StringToDate(),        # in templates can use {{ note.pub_date||date:"j E Y, H:i" }}
            'category': str(self.category),
            'chosen': self.chosen,
        }

    def StringToDate(self):
        from django.utils import formats
        formatted_datetime = formats.date_format(self.pub_date, "SHORT_DATETIME_FORMAT")
        return formatted_datetime
