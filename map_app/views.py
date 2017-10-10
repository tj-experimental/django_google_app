from __future__ import absolute_import, unicode_literals

import json
import logging

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from .utils import messages_to_dict, verify_table_id_cookie_set
from .forms import AddressForm
from .models import Address
from .tables import AddressTable, SearchedAddressesTable

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
    # TODO: Delete all from google fusion table.
    Address.objects.all().delete()
    log.info("Deleted all saved addresses.")
    return redirect('home')


@require_GET
def oauth_view(request):
    """
    Callback view to handle google OAuth request.
    :param request:
    """
    pass

