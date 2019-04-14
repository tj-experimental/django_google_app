import json
import os


def get_file_contents(path):
    if os.path.exists(path):
        with open(path, 'r+') as f:
            return f.read()

def get_json_from_file(path):
    return {} if not os.path.exists(path) else json.loads(get_file_contents(path))
