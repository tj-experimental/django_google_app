from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address
from .tables import AddressTable

# TODO: Handle displaying errors.


def home(request):
    """Render the home page with a default address if no addresses exists."""
    table = AddressTable(Address.objects.only('address').order_by('-id').all())
    street_address = 'Toronto, Canada'
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            if form.instance is not None:
                form.instance.refresh_from_db()
        return render(request, 'table.html',
                      {'table': table, 'form': form})
    if Address.objects.exists():
        default_address = Address.objects.last()
        if default_address.computed_address:
            street_address = default_address.address
        else:
            default_address.delete()
    return render(request, 'index.html', {'address': street_address,
                                          'table': table})


def address(request):
    """Render a table of valid searched/clicked addresses."""
    table = AddressTable(Address.objects.order_by('-id').all())
    return render(request, 'address.html', {'table': table})


def reset_address(request):
    """Remove previously searched addresses."""
    Address.objects.all().delete()
    return redirect('home')
