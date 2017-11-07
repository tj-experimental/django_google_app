from __future__ import unicode_literals, absolute_import

import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.http import HttpRequest
from django.test import TestCase

from eval_project import settings as default_settings
from ...models import Address, UserTokens


class BaseTestCase(TestCase):

    def setUp(self):
        # Set the required env vars
        os.environ['CLIENT_ID'] = 'test_123'
        os.environ['PROJECT_ID'] = 'test'
        os.environ['CLIENT_SECRET'] = 'rrniqrnqi13'


class BaseViewTestCase(BaseTestCase):
    create_address = False
    maxDiff = None

    def setUp(self):
        super(BaseViewTestCase, self).setUp()
        self.request = HttpRequest()
        self.request.session = {}
        self.request.user = self.create_test_superuser()
        self.anonymous_user = AnonymousUser()
        self.request.META.update({'SERVER_NAME': 'localhost',
                                  'SERVER_PORT': '8000'})
        self.message_middleware = MessageMiddleware()
        if self.create_address:
            self.address = 'Ontario'
            self.address_object = (
                self._create_test_address(self.address)
            )

    def tearDown(self):
        # Revert the settings.SITE_ID
        settings.SITE_ID = default_settings.SITE_ID

        if (self.create_address
           and self.address_object
           and self.address_object.pk is not None):
            self.address_object.delete()

    @staticmethod
    def _create_test_address(address_str):
        address_object = Address.objects.create(address=address_str)
        return address_object

    @staticmethod
    def create_test_superuser():
        user = User.objects.create(
            username='test_user',
            password='testuser',
            is_active=True
        )
        user.save()
        return user

    def get_user_token(self, user=None):
        user = user or self.request.user
        try:
            return UserTokens.objects.get(
                user=user)
        except(UserTokens.DoesNotExist,
               UserTokens.MultipleObjectsReturned):
            return None
