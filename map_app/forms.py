from __future__ import absolute_import, unicode_literals

import logging

from django import forms
from django.contrib import messages
from django.utils.encoding import smart_str
from easy_maps.models import Address

log = logging.getLogger(__name__)


class AddressForm(forms.ModelForm):
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Address
        fields = ['address']

    def _post_clean(self):
        super(AddressForm, self)._post_clean()
        if self.cleaned_data.get('address'):
            q = Address.objects.filter(
                address__icontains=self.cleaned_data['address']
            ).exists()
            if q:
                message_ = "The %s could not be %s because similar address already exists." % (
                        self.instance.__class__.__name__, 'created'
                    )
                log.debug("%s : %s" % (message_, self.cleaned_data['address']))
                self._update_errors(message_)

    def save(self, commit=True, request=None):
        log.info("Saving new address")
        try:
            instance = super(AddressForm, self).save(commit=commit)
        except ValueError as e:
            log.debug(smart_str(e))
            messages.error(request, smart_str(e))
        else:
            if instance and not self._valid_address(instance):
                messages.error(request,
                               'Error occurred saving %s: %s' %
                               (instance.__class__.__name__,
                                self.errors.get('address')))
                instance.delete()
                return
            if request and instance:
                message_ = "Successfully added a new %s: %s" % (
                        instance.__class__.__name__,
                        instance.address
                    )
                messages.success(request, message_)
                log.info(message_)
            return instance

    def _valid_address(self, instance):
        if instance.geocode_error or not instance.computed_address:
            message_ = 'Geocode Error'
            log.debug("%s : %s" % (smart_str(str(message_)),
                                   self.cleaned_data['address']))
            self._update_errors(message_)
            return False
        return True

