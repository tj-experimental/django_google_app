from django import forms
from easy_maps.models import Address
from easy_maps.widgets import AddressWithMapWidget


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']
