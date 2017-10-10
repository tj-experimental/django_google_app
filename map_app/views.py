from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import AddressForm
from .models import Address
from .tables import AddressTable, SearchedAddressesTable
from .utils.message_tag import messages_dict_list

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
            log.debug("Error address form invalid.")
        return render(request, 'table.html',
                      {'table': table,
                       'form': form,
                       'storage': messages_dict_list(request)})
    if Address.objects.exists():
        log.info("Found existing address.")
        last_address = Address.objects.filter(
            geocode_error=0).exclude(
            computed_address__isnull=True).last()
        street_address = last_address.address
    response = render(request, 'index.html',
                      {'address': street_address,
                       'table': table})
    if 'fusion_table_id' not in request.COOKIES:
        return _set_fusion_table_cookie(response)
    return response


def address(request):
    """
    Render a table of valid searched/clicked addresses.
    """
    table = SearchedAddressesTable(Address.objects.order_by('-id').all())
    return render(request, 'address.html',
                  {'table': table,
                   'fusion_api_key': settings.GOOGLE_FUSION_TABLE_API_KEY})


def reset_address(request):
    """
    Resets all previously added addresses.
    """
    # TODO: Delete all from google fusion table.
    Address.objects.all().delete()
    log.info("Deleted all saved addresses.")
    return redirect('home')


def oauth_view(request):
    """
    Callback view to handle google OAuth request.
    """
    pass


def _set_fusion_table_cookie(response):
    """
    Set the ``fusion_table_id`` cookie using the ``settings.FUSION_TABLE_ID``.
    :param response: An instance of response object.
    :type response: :class:`django.http.HttpResponse`
    :rtype: :class:`django.http.HttpResponse`
    """
    response.set_cookie('fusion_table_id', settings.FUSION_TABLE_ID)
    return response
