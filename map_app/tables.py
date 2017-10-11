from __future__ import absolute_import, unicode_literals

from future.moves.urllib.parse import quote_plus

from django.utils.html import mark_safe
from django.conf import settings
import django_tables2 as tables
from django_tables2.columns import LinkColumn

from .models import Address


class BassAddressTable(tables.Table):
    map_link = LinkColumn(text='', orderable=False)

    def render_map_link(self, record):
        extra_classes = 'btn-info disabled'
        if record.address and record.latitude and record.longitude:
            extra_classes = 'btn-success'
        query_ = ('&query={address}&query={latitude},'
                  '{longitude}&zoom=7'
                  .format(latitude=record.latitude,
                          longitude=record.longitude,
                          address=record.address))
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
                          'table-condensed table-striped'}


class SearchedAddressesTable(BassAddressTable):
    class Meta:
        exclude = ['geocode_error']
        model = Address
        attrs = {'class': 'address_table table table-hover' +
                          'table-condensed table-striped'}
        fields = ('id', 'address', 'computed_address', 'longitude',
                  'latitude', 'map_link',)


class FusionTable(tables.Table):
    class Meta:
        attrs = {'class': 'address_table table table-hover' +
                          'table-condensed table-striped'}


