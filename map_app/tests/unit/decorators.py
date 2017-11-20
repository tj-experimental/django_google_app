from __future__ import unicode_literals, absolute_import

from unittest import skip

from django.contrib.sites.models import Site
from mock import Mock
from django.conf import settings

from .base import BaseTestCase
from ...decorators import OAuth2Decorator


class OAuth2DecoratorTestCase(BaseTestCase):

    def setUp(self):
        self.oauth_decorator = OAuth2Decorator(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            settings.FUSION_TABLE_SCOPE
        )

    @skip('To Implement')
    def test_oauth_required_decorator(self):
        pass
