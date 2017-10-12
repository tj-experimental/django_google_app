from __future__ import absolute_import, unicode_literals

import json
import logging
from base64 import urlsafe_b64encode

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from oauth2client.contrib import xsrfutil

from .lib import FusionTableMixin, FlowClient
from .utils import messages_to_dict, verify_table_id_cookie_set
from .forms import AddressForm
from .models import Address, UserTokens
from .tables import AddressTable, SearchedAddressesTable, FusionTable

log = logging.getLogger(__name__)


@login_required
@ensure_csrf_cookie
def home(request):
    """
    Render the home page with a default address if no address.

    Redirect to google authorization page credential is invalid.
    """
    flow = FlowClient(request)

    if not flow.credential_is_valid():
        authorization_url = flow.get_authorization_url()
        return HttpResponseRedirect(authorization_url)
    else:
        table = AddressTable(Address.objects.only('address')
                             .order_by('-id').all())
        street_address = 'Toronto, Canada'
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                form.save(request=request)
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
        Address.objects.order_by('-id').all())
    return render(request, 'address.html',
                  {'table': table})


@require_GET
def reset_address(request):
    """
    Resets all previously added addresses.
    """
    log.info("Deleting all saved addresses.")
    Address.objects.all().delete()
    log.info("Deleting all addresses in fusion table.")
    FusionTableMixin.delete_all_addresses(
        *FusionTableMixin.get_service_and_table_id())
    return redirect('/')


@login_required
def oauth_callback(request):
    if not xsrfutil.validate_token(
            settings.SECRET,
            request.GET['state'].encode('ascii'),
            request.user.id):
        return HttpResponseBadRequest()
    flow = FlowClient(request)
    flow.update_user_credential()
    return redirect('/')


class FusionTableHandler(TemplateView, FusionTableMixin):

    template_name = 'fusion_table.html'

    def __init__(self, **kwargs):
        super(FusionTableHandler, self).__init__(**kwargs)
        self.flow = None

    def get(self, request, *args, **kwargs):
        self.flow = FlowClient(request)
        if not self.flow.credential_is_valid():
            return HttpResponseRedirect('/')
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
