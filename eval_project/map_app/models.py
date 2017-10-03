from django.db import models
from django.utils.translation import ugettext_lazy
from easy_maps.models import Address


class Place(models.Model):

    place_id = models.CharField(ugettext_lazy('place_id'), max_length=255, unique=True)

    def __str__(self):
        return self.place_id
