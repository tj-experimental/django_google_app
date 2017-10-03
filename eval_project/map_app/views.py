import logging

from django.shortcuts import render
from .forms import AddressForm
from .models import Address
from .tables import AddressTable

log = logging.getLogger(__name__)


def home(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            address = cd['address']
            log.info("Added address {address}".format(**cd))
            form.save()
            return render(request, 'index.html', {'address': address})
    return render(request, 'index.html', {'address': 'Toronto, Ontario'})


def address(request):
	table = AddressTable(Address.objects.all())
	return render(request, 'address.html', {'table': table})