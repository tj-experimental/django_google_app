from __future__ import absolute_import, unicode_literals

import json
import logging
from itertools import chain

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from .lib import FusionTableMixin
from .utils import messages_to_dict, verify_table_id_cookie_set
from .forms import AddressForm
from .models import Address
from .tables import AddressTable, SearchedAddressesTable, FusionTable

log = logging.getLogger(__name__)


@ensure_csrf_cookie
def home(request):
    """
    Render the home page with a default address if no addresses exists.
    """
    table = AddressTable(Address.objects.only('address').order_by('-id').all())
    street_address = 'Toronto, Canada'
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # TODO Add record to Fusion table.
            form.save(request=request)
        else:
            log.debug("Error address form invalid.", extra=form.errors)
            return HttpResponseBadRequest(json.dumps(form.errors))
        return render(request, 'table.html',
                      {'table': table,
                       'form': form,
                       'storage': messages_to_dict(request, to_str=True)})
    address = (Address.objects
               .filter(geocode_error=0)
               .exclude(computed_address__isnull=True))
    if address.count() > 0:
        log.info("Found existing address.")
        last_address = address.last()
        street_address = last_address.address
    response = render(request, 'index.html',
                      {'address': street_address,
                       'table': table})
    verify_table_id_cookie_set(request, response)
    return response


@require_GET
def address_view(request):
    """
    Render a table of valid searched/clicked addresses.
    """
    table = SearchedAddressesTable(Address.objects.order_by('-id').all())
    return render(request, 'address.html',
                  {'table': table,
                   'fusion_api_key': settings.GOOGLE_FUSION_TABLE_API_KEY})


@require_GET
def reset_address(request):
    """
    Resets all previously added addresses.
    """
    log.info("Deleting all saved addresses.")
    Address.objects.all().delete()
    log.info("Deleting all addresses in fusion table.")
    service, table_id = FusionTableMixin.get_service_and_table_id()
    FusionTableMixin.delete_all_addresses(service, table_id)
    return redirect('home')


class FusionTableHandler(TemplateView, FusionTableMixin):

    template_name = 'fusion_table.html'

    def get_context_data(self):
        service, table_id = self.get_service_and_table_id()
        results = self.select_all_rows(service, table_id)
        import pdb
        pdb.set_trace()
        table = FusionTable(self._process_result(results))
        return {'fusion_table': table}
