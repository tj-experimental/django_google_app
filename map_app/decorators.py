from __future__ import unicode_literals, absolute_import

import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from functools import wraps
from oauth2client.client import HttpAccessTokenRefreshError
from oauth2client.contrib import xsrfutil

from . import lib

log = logging.getLogger(__name__)


def update_site_info(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        current_site = Site.objects.get_or_create(
            name=settings.SITE_NAME,
            domain=settings.SITE_DOMAIN)
        site, exists = current_site
        settings.SITE_ID = site.id
        return func(*args, **kwargs)
    return wrapped


def ajax_permitted(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Invalid ajax Request.')
        return func(request, *args, **kwargs)
    return wrapped


class OAuth2Decorator(object):

    def __init__(self, client_id, secret, scope):
        self._client_id = client_id
        self._secret = secret
        self._scope = scope

    def oauth_required(self, method):
        """Decorator that starts the OAuth 2.0 dance.

        Starts the OAuth dance for the logged in user if they haven't already
        granted access for this application.

        Args:
            method: callable, to be decorated method of a webapp.RequestHandler
                    instance.
        """

        def check_oauth(request_handler, *args, **kwargs):
            class_handler = None
            if hasattr(request_handler, 'request'):
                class_handler = request_handler
                request_handler = request_handler.request
            user = request_handler.user
            if not user:
                # This should be an extra argument
                return HttpResponseRedirect(reverse('auth_login'))

            flow_client = lib.FlowClient(request_handler)
            if not flow_client.credential_is_valid():
                log.debug("Invalid user credential: %d",
                          request_handler.user.id)
                authorization_url = flow_client.get_authorization_url()
                return HttpResponseRedirect(authorization_url)

            if 'state' in request_handler.GET:
                token = bytes(request_handler.GET['state'], encoding='utf-8')
                if not xsrfutil.validate_token(
                        settings.SECRET,
                        token,
                        request_handler.user.id):
                    log.error('Invalid token used by %s: %d' % (
                        request_handler.user.username, request_handler.user.id))
                    return HttpResponseBadRequest('Invalid Token')

            try:
                if class_handler:
                    return method(class_handler, request_handler,
                                  *args, **kwargs)
                else:
                    return method(request_handler, *args, **kwargs)
            except HttpAccessTokenRefreshError as e:
                log.debug(e)
                authorization_url = flow_client.get_authorization_url()
                return HttpResponseRedirect(authorization_url)
        return check_oauth


oauth_decorator = OAuth2Decorator(
    settings.CLIENT_ID,
    settings.SECRET,
    settings.FUSION_TABLE_SCOPE
)
