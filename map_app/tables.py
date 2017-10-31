from __future__ import absolute_import, unicode_literals

from django.utils.html import mark_safe
from django.conf import settings
import django_tables2 as tables
from django_tables2.columns import LinkColumn, Column

from .models import Address


class BassAddressTable(tables.Table):
    map_link = LinkColumn(text='', orderable=False)

    def safe_get_value(self, record, attr):
        return (getattr(record, attr)
                if hasattr(record, attr)
                else record.get(attr, ''))

    def render_map_link(self, record):
        extra_classes = 'btn-info disabled'
        address = self.safe_get_value(record, 'address')
        latitude = self.safe_get_value(record, 'latitude')
        longitude = self.safe_get_value(record, 'longitude')
        if address and latitude and longitude:
            extra_classes = 'btn-success'
        query_ = ('&query={address}&query={latitude},'
                  '{longitude}&zoom=7'
                  .format(latitude=latitude,
                          longitude=longitude,
                          address=address))
        url = settings.VIEW_GOOGLE_MAP_LINK + query_
        return (mark_safe('<a href="{url}" target="__blank" '
                          'class="btn {extra_classes}">'
                          'Open Map</a>'
                .format(url=url,
                        extra_classes=extra_classes)))


class AddressTable(BassAddressTable):
    class Meta:
        fields = ('id', 'address')
        model = Address
        attrs = {'class': 'address_table table table-hover' +
                          'table-condensed table-striped ' +
                           'table-responsive'}


class SearchedAddressesTable(BassAddressTable):
    class Meta:
        exclude = ['geocode_error']
        model = Address
        attrs = {'class': 'address_table table table-hover' +
                          'table-condensed table-striped ' + 
                          'table-responsive'}
        fields = ('id', 'address', 'computed_address', 'longitude',
                  'latitude', 'map_link',)


class FusionTable(BassAddressTable):
    address = Column('Address', orderable=True)
    longitude = Column('Longitude', orderable=True)
    latitude = Column('Latitude', orderable=True)
    computed_address = Column('Computed Address', orderable=True)
    rowid = Column('ID', orderable=True)

    class Meta:
        order_by = 'rowid'
        attrs = {'class': 'address_table table table-hover' +
                          'table-condensed table-striped ' +
                          'table-responsive'}

        fields = ('rowid', 'address', 'longitude', 'latitude',
                  'computed_address',)


