from __future__ import absolute_import

import json
from unittest import skip

from django.core.urlresolvers import resolve
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from mock import patch, MagicMock

from .base import BaseViewTestCase
from ...utils import messages_to_dict
from ...forms import AddressForm
from ...models import Address
from ...tables import AddressTable
from ...views import home, address_view, reset_address


class HomePageTestCase(BaseViewTestCase):
    create_address = True

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    @skip('Need to implement')
    def test_home_page_can_save_POST_request(self):
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
                   return_value=flow_client), \
                patch('map_app.lib.FusionTableMixin',
                      return_value=fusion_table_mixin):
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
            flow_client.credential_is_valid.assert_called_once()

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


class AddressTestCase(BaseViewTestCase):
    create_address = False

    def test_address_url_resolves_to_address_view(self):
        found = resolve('/address')
        self.assertEqual(found.func, address_view)


class AddressResetTestCase(BaseViewTestCase):
    create_address = False

    def test_reset_address_url_resolves_to_reset_address_view(self):
        found = resolve('/reset-address')
        self.assertEqual(found.func, reset_address)

    @skip('Need to implement')
    def test_send_get_request_returns_correct_html(self):
        pass
