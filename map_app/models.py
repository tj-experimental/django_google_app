from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from easy_maps.models import Address


@python_2_unicode_compatible
class UserTokens(models.Model):
    user = models.OneToOneField(User, unique=True)
    access_token = models.TextField(null=False)
    refresh_token = models.TextField(null=False)

