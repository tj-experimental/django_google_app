import urllib

from django.utils.html import mark_safe
from django.conf import settings
import django_tables2 as tables
from django_tables2.columns import LinkColumn

from .models import Address


class BassAddressTable(tables.Table):
	map_link = LinkColumn(text='', orderable=False)

	def render_map_link(self, record):
		extra_classes = 'btn-success'
		if record.address and record.latitude and record.longitude:
			extra_classes = 'btn-info disabled'
		url = settings.VIEW_GOOGLE_MAP_LINK.format(latitude=record.latitude,
			longitude=record.longitude, address=record.address, zoom=6)
		return mark_safe('<a href="{url}" target="__blank" '
			'class="btn {extra_classes}">Open Map</a>'.format(
				url=url, extra_classes=extra_classes))


class AddressTable(BassAddressTable):

	class Meta:
		fields = ('id', 'address')
		model = Address
		attrs = {'class': 'address_table table table-hover' + 
						'table-condensed table-striped'}

class SearchedAddressesTable(BassAddressTable):

	class Meta:
		exclude = ['geocode_error']
		model = Address
		attrs = {'class': 'address_table table table-hover' + 
						'table-condensed table-striped'}



		


