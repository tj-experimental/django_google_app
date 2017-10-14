from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from easy_maps.models import Address
from oauth2client.contrib.django_util.models import CredentialsField


@python_2_unicode_compatible
class UserTokens(models.Model):
    """User token model use for google Oauth authentication."""
    user = models.OneToOneField(User, primary_key=True)
    access_token = models.TextField(null=True)
    authorized_url = models.URLField(null=True)

    def __str__(self):
        return 'UserToken Model'


@python_2_unicode_compatible
class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()

    def __str__(self):
        return 'Credential Model'
