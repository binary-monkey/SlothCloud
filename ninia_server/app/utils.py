import json
import os


def get_permitted_formats():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config/permissions.json",
              'r') as format_file:
        return json.load(format_file)["formats"]