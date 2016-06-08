from __future__ import unicode_literals

from django.db import models


# Create your models here.
class BaseMixin(models.Model):
    visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
