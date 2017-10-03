from django import forms
from easy_maps.models import Address
from easy_maps.widgets import AddressWithMapWidget


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']
        exclude = ['address_reset']
        widgets = {
            'address': AddressWithMapWidget({'class': 'vTextField'})
        }

    def save(self, *args):
        q = Address.objects.filter(address__icontains=self.cleaned_data['address'])
        if q:
            raise ValueError(
                "The %s could not be %s because similar address already exists." % (
                    self.instance.object_name, 'created'
                )
            )
        return super(AddressForm, self).save(*args)

    @staticmethod
    def reset():
        return Address.objects.all().delete()
