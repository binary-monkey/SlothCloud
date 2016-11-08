import json
import os



def get_config(json_filename):
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/config/" +
                          json_filename + ".json", 'r') as file:
            return json.load(file)
    except FileNotFoundError as fnfe:
        return {"error": "0"}


def get_permitted_formats():
        return get_config("permissions")["formats"]


def is_allowed(fformat):
    formats = get_permitted_formats()
    for category in formats:
        for extension in formats[category]:
            if fformat == extension:
                return True

    return False

