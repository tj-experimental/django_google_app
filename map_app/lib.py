import json

from oauth2client import client
from oauth2client.contrib import appengine
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings


class FlowClient(object):
    def __init__(self,
                 client_secret_json=settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
                 scope=settings.FUSION_TABLE_SCOPE,
                 redirect_url=settings.OAUTH2_CLIENT_REDIRECT_URL,
                 ):
        self.flow = client.flow_from_clientsecrets(
            filename=client_secret_json, scope=scope,
            redirect_uri=redirect_url)

decorator = appengine.OAuth2DecoratorFromClientSecrets(

)
