import json

from django.contrib import messages
from django.contrib.messages import get_messages


def update_error_tag():
    return {messages.ERROR: 'danger'}


def message_to_dict(messages_, to_json):
    for message in messages_:
        ret_dict = {'message': message.message,
                    'level_tag': message.level_tag,
                    'level': message.level}
        if to_json:
            ret_dict = json.dumps(ret_dict)
        yield ret_dict


def messages_dict_list(request, to_json=True):
    return [message for message in
            message_to_dict(get_messages(request), to_json)]
