from __future__ import absolute_import, unicode_literals

import json
import logging

from django.conf import settings
from django.contrib.auth import decorators
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from oauth2client.contrib import xsrfutil

from . import lib
from .decorators import oauth_decorator
from .forms import AddressForm
from .models import Address
from .tables import AddressTable, SearchedAddressesTable, FusionTable
from .utils import messages_to_dict, verify_table_id_cookie_set

log = logging.getLogger(__name__)


@decorators.login_required
@ensure_csrf_cookie
@oauth_decorator.oauth_required
def home(request):
    """
    Render the home page with a default address if no address.
    """
    table = AddressTable(Address.objects.only('address')
                         .order_by('-id').all(),
                         request=request)
    street_address = 'Toronto, Canada'
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            table = AddressTable(
                form.get_addresses(),
                request=request)
        else:
            log.debug("Error address form invalid.",
                      extra=form.errors)
            return HttpResponseBadRequest(
                json.dumps(form.errors))
        return render(request, 'table.html',
                      {'table': table,
                       'form': form,
                       'storage': messages_to_dict(
                           request, to_str=True)})
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
    table = SearchedAddressesTable(
        Address.objects.order_by('-id').all(),
        request=request)
    return render(request, 'address.html',
                  {'table': table})


@require_GET
@oauth_decorator.oauth_required
def reset_address(request):
    """
    Resets all previously added addresses.
    """
    flow = lib.FlowClient(request)
    log.info("Deleting all saved addresses.")
    Address.objects.all().delete()
    log.info("Deleting all addresses in fusion table.")
    lib.FusionTableMixin.delete_all_addresses(
        *flow.get_service_and_table_id())
    return redirect('/')


@decorators.login_required
def oauth_callback(request):
    token = request.GET.get('state')
    if not token:
        log.error('Invalid request.')
        return HttpResponseBadRequest('Invalid Request.')
    if not xsrfutil.validate_token(
            settings.SECRET,
            bytes(token, encoding='utf-8'),
            request.user.id):
        log.error("User id %d Invalid Token used: %s"
                  % (request.user.id, token))
        return HttpResponseBadRequest('Invalid Token')
    flow = lib.FlowClient(request)
    flow.update_user_credential()
    return redirect('/')


class FusionTableHandler(TemplateView, lib.FusionTableMixin):

    template_name = 'fusion_table.html'

    def __init__(self, **kwargs):
        super(FusionTableHandler, self).__init__(**kwargs)
        self.flow = None

    @oauth_decorator.oauth_required
    def get(self, request, *args, **kwargs):
        # This relies on get called first will neat to
        # have an interface without having to
        # create the flow here
        self.flow = lib.FlowClient(request)
        kwargs['_request'] = request
        return super(FusionTableHandler, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.flow:
            service, table_id = (
                self.flow.get_service_and_table_id())
        else:
            service, table_id = self.get_service_and_table_id()
        results = self.select_all_rows(service, table_id)
        table = FusionTable(self._process_result(results),
                            request=kwargs.get('_request'))
        return {'fusion_table': table}
