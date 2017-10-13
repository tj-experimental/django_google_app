from __future__ import unicode_literals, absolute_import

from django.http import HttpResponseBadRequest
from functools import wraps


def ajax_permitted(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Invalid ajax Request.')
        return func(request, *args, **kwargs)
    return wrapped
