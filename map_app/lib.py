from __future__ import absolute_import

import functools
import json
import os
from abc import ABCMeta

from django.conf import settings
from django.shortcuts import get_object_or_404
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.service_account import ServiceAccountCredentials

from .exceptions import InvalidCredentialException
from .models import UserTokens, CredentialsModel


def _build_service(http, service_name='fusiontables', version='v1'):
    return build(service_name, version, http=http,
                 developerKey=settings.GOOGLE_FUSION_TABLE_API_KEY)


def store_user_tokens(user, access_token, refresh_token):
    return UserTokens.objects.create(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


class FlowClient(object):
    """
    FlowClient to manage credentials.
    """
    def __init__(self,
                 request,
                 client_secret_json=settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
                 scope=settings.FUSION_TABLE_SCOPE,
                 redirect_url=settings.OAUTH2_CLIENT_REDIRECT_PATH,
                 ):
        self.flow = client.flow_from_clientsecrets(
            filename=client_secret_json, scope=scope,
            redirect_uri=redirect_url)
        self.request = request
        self.user = self.request.user
        self.http = Http()

    def get_credential(self):
        # Read credentials
        storage = DjangoORMStorage(CredentialsModel, 'id', self.user, 'credential')
        return storage.get()

    def generate_token(self):
        token = xsrfutil.generate_token(
            settings.SECRET, self.user.id)
        self.flow.params['state'] = token
        return token

    def update_user_token_model(self, token, authorization_url):
        user_token = UserTokens(user=self.user,
                                access_token=token,
                                authorized_url=authorization_url)
        user_token.save()

    def credential_is_valid(self):
        credential = self.get_credential()
        # Credential not valid if None or credential.invalid == True
        if credential:
            return not credential.access_token_expired
        return False

    def get_authorization_url(self):
        if not self.credential_is_valid():
            token = self.generate_token()
            authorization_url = self.flow.step1_get_authorize_url()
            self.update_user_token_model(token, authorization_url)
            return authorization_url

    def get_user_token(self):
        user_token = get_object_or_404(UserTokens, pk=self.user.id)
        return user_token.access_token

    def update_user_credential(self):
        # Create credential
        request = self.request
        credential = self.flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(CredentialsModel, 'id',
                                   request.user, 'credential')
        # Write credential
        storage.put(credential)
        cred, created = CredentialsModel.objects.update_or_create(
            id=request.user, credential=credential)
        return cred, created

    def _authorize_http(self):
        if self.credential_is_valid():
            credential = self.get_credential()
            self.http = credential.authorize(self.http)

    def get_service_and_table_id(self):
        self._authorize_http()
        # http is authorized with the user's Credentials and can be
        # used in API calls
        table_id = settings.FUSION_TABLE_ID
        service = _build_service(self.http)
        return service, table_id


class FusionTableMixin(metaclass=ABCMeta):
    """
    Mixin to manage Interactions with google fusion table.
    """
    @classmethod
    def select_all_rows(cls, service, table_id):
        return (service.query()
                .sql(sql='SELECT ROWID, address,'
                         ' latitude, longitude,'
                         ' computed_address FROM %s'
                         % table_id).execute())

    @classmethod
    def delete_all_addresses(cls, service, table_id):
        return (service.table()
                .delete(tableId=table_id).execute())

    @classmethod
    def get_style(cls, service, table_id, style_id=1):
        style = (service.style().get(tableId=table_id,
                                     styleId=style_id)
                 .execute())
        if style:
            return json.dumps(style)

    @classmethod
    def save(cls, address, service, table_id):
        values_dict = cls.sanitize_address(address)
        values_dict.update({'table_id': table_id})
        if not cls.address_exists(address, service, table_id):
            return (service.query()
                    .sql(sql="INSERT INTO {table_id} "
                             "(address, latitude, longitude,"
                             " computed_address)"
                             "VALUES \"('{address}', {latitude}, "
                             "{longitude}, '{computed_address}')\""
                         .format(**values_dict)).execute())

    @classmethod
    def address_exists(cls, address, service, table_id):
        query_dict = {'table_id': table_id,
                      'address': address.address}
        results = (service.query()
                   .sql(sql="SELECT address FROM {table_id} "
                            "WHERE address LIKE '%{address}%'"
                        .format(**query_dict)).execute())
        try:
            return next(cls._process_result(results))
        except StopIteration:
            pass
        return None

    @classmethod
    def get_service_and_table_id(cls):
        # This should be removed.
        # http = get_http_auth(settings.GOOGLE_SERVICE_ACCOUNT_KEY_FILE)
        # http is authorized with the user's Credentials and can be
        # used in API calls
        # table_id = settings.FUSION_TABLE_ID
        # service = _build_service(http)
        # return service, table_id
        raise NotImplementedError()

    @classmethod
    def _process_result(cls, results):
        rows = results.get('rows', [])
        columns = results.get('columns', [])
        for row in rows:
            yield dict(zip(columns, row))

    @classmethod
    def sanitize_address(cls, address):
        values_dict = {'address': address.address or '',
                       'latitude': address.latitude or '',
                       'longitude': address.longitude or '',
                       'computed_address': address.computed_address or ''}
        return values_dict
