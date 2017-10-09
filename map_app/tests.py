from __future__ import absolute_import

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

from .views import home, address, reset_address
from .models import Address
from .tables import AddressTable
from .forms import AddressForm


class BaseTestCase(TestCase):
    create_address = False

    def setUp(self):
        self.request = HttpRequest()
        if self.create_address:
            self.address = 'Toronto, Ontario'
            self.address_object, self.delete_address = (
                self._create_test_address(self.address))

    def _create_test_address(self, address_str):
        delete_address = True
        if self._address_exists(address_str):
            address_object = self._get_first_address(address_str)
            delete_address = False
        else:
            address_object = Address.objects.create(address=address_str)
        return address_object, delete_address

    @staticmethod
    def _address_exists(address_str):
        return Address.objects.filter(address__icontains=address_str).exists()

    @staticmethod
    def _get_first_address(address_str):
        return Address.objects.filter(address__icontains=address_str).first()

    def tearDown(self):
        if self.delete_address and self.create_address:
            self.address_object.delete()


class HomePageTestCase(BaseTestCase):
    create_address = True

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_can_save_POST_request(self):
        # TODO: Use address generator.
        pass

    def test_POST_request_return_correct_html(self):
        request = self.request
        request.method = 'POST'
        request.POST['address'] = self.address
        table = AddressTable(Address.objects.only('address')
                             .order_by('-id').all())
        form = AddressForm(request.POST)
        expected_html = render_to_string('table.html',
                                         context={'table': table,
                                                  'form': form},
                                         request=self.request)

        response = home(request)

        self.assertEqual(response.content.decode(), expected_html)


class AddressTestCase(BaseTestCase):
    create_address = False

    def test_address_url_resolves_to_address_view(self):
        found = resolve('/address')
        self.assertEqual(found.func, address)


class AddressResetTestCase(BaseTestCase):
    create_address = False

    def test_reset_address_url_resolves_to_reset_address_view(self):
        found = resolve('/reset-address')
        self.assertEqual(found.func, reset_address)
