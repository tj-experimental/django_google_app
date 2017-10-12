from __future__ import absolute_import

import json

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.http import HttpResponseBadRequest
from django.test import TestCase
from django.http import HttpRequest
from unittest import skipIf, skip
from django.template.loader import render_to_string
from django.contrib.messages.middleware import MessageMiddleware

from ..views import home, address_view, reset_address
from ..models import Address
from ..tables import AddressTable
from ..forms import AddressForm


class BaseTestCase(TestCase):
    create_address = False

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = AnonymousUser()
        self.request.session = {}
        self.message_middleware = MessageMiddleware()
        if self.create_address:
            self.address = 'Toronto, Ontario'
            self.address_object = (
                self._create_test_address(self.address)
            )

    def _create_test_address(self, address_str):
        address_object = Address.objects.create(address=address_str)
        return address_object
    

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
        self.message_middleware.process_request(request)
        # Delete the existing address to prevent violating the
        # unique constraint.
        self.address_object.delete()
        request.POST['address'] = self.address
        form = AddressForm(request.POST)

        response = home(request)

        # Moved below since new instance of the address will be created
        addresses = (Address.objects.only('address')
                     .order_by('-id').all())
        expected_html = render_to_string(
            'table.html',
            context={'table': AddressTable(addresses),
                     'form': form},
            request=self.request)

        self.assertEqual(response.content.decode(), expected_html)

    def test_post_invalid_request_returns_http_bad_request(self):
        request = self.request
        request.method = 'POST'
        # Address already created before request raises
        # HttpBadRequest
        request.POST['address'] = self.address
        self.message_middleware.process_request(request)

        response = home(request)

        self.assertIsInstance(response, HttpResponseBadRequest)

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
