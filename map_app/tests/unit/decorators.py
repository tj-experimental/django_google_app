from __future__ import unicode_literals, absolute_import

from unittest import skip

from django.contrib.sites.models import Site
from mock import Mock
from django.conf import settings

from .base import BaseTestCase
from ...decorators import update_site_info, OAuth2Decorator


class SiteInfoDecoratorsTestCase(BaseTestCase):

    @staticmethod
    def _get_site(site_id):
        try:
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            site = None
        return site

    def test_update_site_info_decorator_updates_the_site_id(self):
        func = Mock(name='test_func')

        default_site = self._get_site(settings.SITE_ID)

        # Change the site name and domain
        settings.SITE_NAME = 'test.com'
        settings.SITE_DOMAIN = 'test.com'

        update_site_info(func)()

        new_site = self._get_site(settings.SITE_ID)

        self.assertIsNotNone(new_site)
        self.assertNotEqual(default_site.id, settings.SITE_ID)
        self.assertEqual(new_site.id, settings.SITE_ID)
        func.assert_called_once_with()


class OAuth2DecoratorTestCase(BaseTestCase):

    def setUp(self):
        self.oauth_decorator = OAuth2Decorator(
            settings.CLIENT_ID,
            settings.SECRET,
            settings.FUSION_TABLE_SCOPE
        )

    @skip('To Implement')
    def test_oauth_required_decorator(self):
        pass
