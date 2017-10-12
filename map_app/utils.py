from __future__ import absolute_import

import json

from django.conf import settings
from django.contrib.messages import get_messages


def verify_table_id_cookie_set(request, response):
    """
    Verify the google fusion ``table_id`` is set on the request.

    :param request: HttpRequest object
    :type request: :class:`django.http.request.HttpRequest`
    :param response: HttpResponse object
    :type response: :class:`django.http.response.HttpResponse`.
    """
    if 'fusion_table_id' not in request.COOKIES:
        return set_fusion_table_cookie(response)


def set_fusion_table_cookie(response):
    """
    Set the ``fusion_table_id`` cookie using the ``settings.FUSION_TABLE_ID``.

    :param response: An instance of response object.
    :type response: :class:`django.http.HttpResponse`
    :return: An instance of the HttpResponse object.
    :rtype: :class:`django.http.HttpResponse`
    """
    response.set_cookie('fusion_table_id', settings.FUSION_TABLE_ID)
    return response


def messages_to_dict(request, to_str=False):
    """
    :py:function ***message_to_dict***

    Returns an iterator that yields a JSON formatted string or dictionary.

    Retrieve the ``_messages`` from an instance of
    :py:class:`django.http.request.HttpRequest`.
    :param request: An instance of :py:class:`django.http.request.HttpRequest`,
    :type request: :py:class:`django.http.request.HttpRequest`
    :param to_str: Boolean indication to serialize message object to string.
    :type to_str: bool
    :rtype: str|dict
    """
    storage = get_messages(request)
    storage.used = True
    for message in storage:
        ret_dict = {'message': message.message,
                    'level_tag': message.level_tag,
                    'level': message.level}
        if to_str:
            ret_dict = json.dumps(ret_dict)
        yield ret_dict
