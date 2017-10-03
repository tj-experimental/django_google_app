import django_tables2 as tables
from .models import Address

class AddressTable(tables.Table):
	class Meta:
		model = Address
		attrs = {'class': 'address_table'}