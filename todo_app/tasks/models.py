from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from todo_app.base.models import BaseMixin


# Create your models here.
class Task(BaseMixin):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')
    title = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('updated',)
