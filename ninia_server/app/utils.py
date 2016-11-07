import json
import os


def get_permissions():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config/permissions.json",
              'r') as format_file:
        return json.load(format_file)

def get_permitted_formats():
        return get_permissions()["formats"]


def is_allowed(fformat):
    formats = get_permitted_formats()
    for category in formats:
        for extension in formats[category]:
            if fformat == extension:
                return True

    return False

