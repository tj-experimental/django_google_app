from __future__ import absolute_import

import json
import sys

from django.shortcuts import render
from mock import patch, MagicMock, Mock

from django.contrib.auth.models import AnonymousUser, AbstractUser, User
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.test import TestCase
from django.http import HttpRequest
from unittest import skipIf, skip
from django.template.loader import render_to_string
from django.contrib.messages.middleware import MessageMiddleware

from map_app.utils import messages_to_dict
from ...views import home, address_view, reset_address
from ...models import Address, UserTokens
from ...tables import AddressTable
from ...forms import AddressForm


class BaseTestCase(TestCase):
    create_address = False
    maxDiff = None

    def setUp(self):
        self.request = HttpRequest()
        self.request.session = {}
        self.request.user = self.create_test_superuser()
        self.anonymous_user = AnonymousUser()
        self.request.META.update({'SERVER_NAME': 'localhost',
                                  'SERVER_PORT': '8000'})
        self.message_middleware = MessageMiddleware()
        if self.create_address:
            self.address = 'Toronto, Ontario'
            self.address_object = (
                self._create_test_address(self.address)
            )

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


class HomePageTestCase(BaseTestCase):
    create_address = True

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    @skip('Need to implement.')
    def test_home_page_can_save_POST_request(self):
        new_address = 'New york'
        pass

    def test_post_request_return_correct_html(self):
        request = self.request
        request.method = 'POST'
        # Delete the existing address to prevent violating the
        # unique constraint.
        self.address_object.delete()
        request.POST = {'address': self.address}
        self.message_middleware.process_request(self.request)
        form = AddressForm(request.POST)
        flow_client = MagicMock(name='FlowClient')
        flow_client.credential_is_valid.return_value = True
        flow_client.get_service_and_table_id.return_value = (
            111, 'test-table')

        fusion_table_mixin = MagicMock(name='FusionTableMixin')
        fusion_table_mixin.address_exists = None

        with patch('map_app.lib.FlowClient',
                   return_value=flow_client) as fc, \
                patch('map_app.lib.FusionTableMixin',
                      return_value=fusion_table_mixin) as ft:
            response = home(request)

            # Moved below since new instance of
            # the address will be created
            table = AddressTable(Address.objects.only('address')
                                 .order_by('-id').all(),
                                 request=request)
            expected = render(
                    request, 'table.html',
                    {'table': table,
                     'form': form,
                     'storage': messages_to_dict(
                         request, to_str=True)})

            self.assertHTMLEqual(response.content.decode(),
                                 expected.content.decode())

    def test_invalid_credentials_returns_redirect(self):
        request = self.request
        request.method = 'POST'
        request.POST = {'address': self.address}

        response = home(request)
        # Token is updated after call
        user_token = self.get_user_token()
        self.assertIsInstance(response, HttpResponseRedirect)
        if user_token:
            self.assertRedirects(response,
                                 user_token.authorized_url,
                                 fetch_redirect_response=False)

    def test_post_invalid_request_returns_http_bad_request(self):
        request = self.request
        request.method = 'POST'
        # Address already created before request raises
        # HttpBadRequest
        request.POST = {'address': self.address}
        flow_client = MagicMock(name='FlowClient')
        flow_client.credential_is_valid.return_value = True

        with patch('map_app.lib.FlowClient',
                   return_value=flow_client):

            response = home(request)

            self.assertIsInstance(response, HttpResponseBadRequest)
            flow_client.credential_is_valid.assert_called_once()

            response_text = json.loads(response.content.decode())
            self.assertEqual(
                'EasyMaps Address with this Address already exists.',
                ''.join(response_text.get('address')))


class AddressTestCase(BaseTestCase):
    create_address = False

    def test_address_url_resolves_to_address_view(self):
        found = resolve('/address')
        self.assertEqual(found.func, address_view)


class AddressResetTestCase(BaseTestCase):
    create_address = False

    def test_reset_address_url_resolves_to_reset_address_view(self):
        found = resolve('/reset-address')
        self.assertEqual(found.func, reset_address)

    @skip('Need to implement.')
    def test_send_get_request_returns_correct_html(self):
        pass
