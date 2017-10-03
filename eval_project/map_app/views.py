from django.shortcuts import render, render_to_response
from .forms import AddressForm
from .models import Address
from .tables import AddressTable


def home(request):
    """Render the home page with a default address if no addresses exists."""
    table = AddressTable(Address.objects.only('address').order_by('id').all())
    street_address = 'King Street West'
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if request.POST['address_reset'] == "yes":
            form.reset()
            cd = {'address': street_address}
        elif form.is_valid():
            cd = form.cleaned_data
            form.save()
            form.instance.refresh_from_db()
        table = AddressTable(Address.objects.only('address').order_by('id').all())
        return render(request, 'index.html', {'address': cd['address'],
        									 'table': table})
    if Address.objects.exists():
        street_address = Address.objects.only('address').last()
    return render(request, 'index.html',
                  {'address': street_address,
                   'table': table})


def address(request):
    """Render a table of valid searched/clicked addresses."""
    table = AddressTable(Address.objects.all())
    return render(request, 'address.html', {'table': table})
