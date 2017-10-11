import json
from django.utils.six import wraps
import functools

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings
from django.http.response import HttpResponseNotAllowed

from map_app.models import UserTokens


@functools.lru_cache(maxsize=None)
def get_http_auth():
    if not settings.GOOGLE_SERVICE_ACCOUNT_KEY_FILE:
        raise HttpResponseNotAllowed('No service account key file found.')
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.GOOGLE_SERVICE_ACCOUNT_KEY_FILE,
            settings.FUSION_TABLE_SCOPE
        )
        # TODO: Add file based cache for http auth
        http = credentials.authorize(Http())
        return http


@functools.lru_cache(maxsize=None, typed=True)
def get_service(http, service_name='fusiontables', version='v2'):
    return build(service_name, version, http=http)


def store_user_tokens(user, access_token, refresh_token):
    return UserTokens.objects.create(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


class FlowClient(object):
    def __init__(self,
                 client_secret_json=settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
                 scope=settings.FUSION_TABLE_SCOPE,
                 redirect_url=settings.OAUTH2_CLIENT_REDIRECT_PATH,
                 ):
        self.flow = client.flow_from_clientsecrets(
            filename=client_secret_json, scope=scope,
            redirect_uri=redirect_url)


class FusionTableMixin(object):

    @classmethod
    def select_all_rows(cls, service, table_id):
        return (service.query()
                .sql(sql='SELECT * FROM %s' % table_id).execute())

    @classmethod
    def delete_all_addresses(cls, service, table_id):
        return (service.query()
                .sql(sql='DELETE FROM %s' % table_id).execute())

    @classmethod
    def insert_address(cls, address, service, table_id):
        values_dict = {'address': address.address,
                       'latitude': address.latitude,
                       'longitude': address.longitude,
                       'computed_address': address.computed_address,
                       'table_id': table_id}
        if not cls.address_exists(address, service, table_id):
            return (service.query()
                    .sql(sql='INSERT INTO {table_id} '
                             '(address, latitude, longitude,'
                             ' computed_address)'
                             'VALUES ("{address}", {latitude}, '
                             '{longitude}, "{computed_address}")'
                         .format(**values_dict)).execute())

    @classmethod
    def address_exists(cls, address, service, table_id):
        query_dict = {'table_id': table_id,
                      'address': address.address}
        results = (service.query()
                   .sql(sql='SELECT address FROM {table_id} '
                            'WHERE EXISTS '
                            '(SELECT address FROM {table_id} '
                            'WHERE address LIKE "%{address}%")'
                   .format(**query_dict)).execute())
        return cls._process_result(results)

    @classmethod
    def get_service_and_table_id(cls):
        http = get_http_auth()
        # http is authorized with the user's Credentials and can be
        # used in API calls
        table_id = settings.FUSION_TABLE_ID
        service = get_service(http)
        return service, table_id

    @classmethod
    def _process_result(cls, results):
        rows = results.get('rows')
        columns = results.get('columns')
        for row in rows:
            yield dict(zip(columns, row))

    @classmethod
    def save(cls, address, service, table_id):
        return cls.insert_address(address, service, table_id)
