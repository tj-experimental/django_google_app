from django import forms
from easy_maps.models import Address


class AddressForm(forms.ModelForm):
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Address
        fields = ['address']

    def save(self, *args):
        if self.cleaned_data['address']:
            q = Address.objects.filter(
                address__icontains=self.cleaned_data['address']
            ).exists()
            if q:
                raise ValueError(
                    "The %s could not be %s because similar address already exists." % (
                        self.instance.__class__.__name__, 'created'
                    )
                )
        return super(AddressForm, self).save(*args)
