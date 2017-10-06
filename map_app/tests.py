from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

from .views import home, address, reset_address
from .models import Address
from .tables import AddressTable
from .forms import AddressForm


class HomePageTest(TestCase):

	def setUp(self):
		super(HomePageTest, self).setUp()
		self.request = HttpRequest()
		self.address = 'Toronto, Ontario'
		self.address_object, self.delete_address = self._create_test_address(
		    self.address)

	def _create_test_address(self, address):
		delete_address = True
		if self._address_exists(address):
			address_object = q.first()
			delete_address = False
		else:
			address_object = Address.objects.create(address=address)
		return address_object, delete_address

	def _address_exists(self, address):
		return Address.objects.filter(address__icontains=address).exists()

	def tearDown(self):
		if self.delete_address:
			self.address_object.delete()
			super(HomePageTest, self).tearDown()

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
		form =  AddressForm(request.POST)
		expected_html = render_to_string('table.html', 
						 context={'table': table, 
							  'form': form},
						 request=self.request)

		response = home(request)

		self.assertEqual(response.content.decode(), expected_html)

class AddressTest(TestCase):
	def test_address_url_resolves_to_address_view(self):
		found = resolve('/address')
		self.assertEqual(found.func, address)

		
class AddressResetTest(TestCase):
	def test_reset_address_url_resolves_to_reset_address_view(self):
		found = resolve('/reset-address')
		self.assertEqual(found.func, reset_address)
