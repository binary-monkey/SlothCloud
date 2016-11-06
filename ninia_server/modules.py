#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.config.constants import ninia_path, host, port
from app.utils import get_permitted_formats
import json
import os
from shutil import rmtree


media = ""


def clean_dir(path):
    for element in os.listdir(path):
        if os.path.isdir(path + '/' + element) and not os.listdir(path + '/' + element):
            rmtree(path + '/' + element)


def gen_menu():
    """
    Autogenerates a menu with the media files stored in app/static/media/
    """
    menu_entries = read_scheme()

    # menu_file variable will be the html file.
    # writes beginning section
    menu_file = """
        <!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Main Index</title>
        </head><body><h1>Ninia (in-dev) - Menu</h1>"""

    for category in sorted(menu_entries.keys()):
        # Category name, first letter is upper
        menu_file += "\n<h2>" + category[0].upper() + category[1:] + "</h2>"
        # List of all entries in category
        for entry in sorted(menu_entries[category]):
            entry = entry[1:].replace("/", "|")
            menu_file += '\n<a href="http://' + host + ':' + port + '/play/' + \
                         entry + '">' + entry.replace("|", "/") + '</a>'
            menu_file += "<br>"

    # writes end section
    menu_file += "</body></html>"
    return menu_file


# todo: optimize restriction check
def get_index(path=""):
    """
    Returns json file containing the files and directories subsequent to the path
    passed as a parameter. Each folder has a list containing everything in of it.
    :param path: optional, default=root
    """
    rel_path = path
    if not path:
        path = ninia_path + "/app/static/media"
    else:
        path = ninia_path + "/app/static/media/" + path

    if os.path.exists(path) and os.path.isdir(path):
        with open('app/config/permissions.json') as permission_file:
            permitted_dirs = json.load(permission_file)["directories"]["index"]

        return json.dumps({rel_path: get_scheme(path, permitted_dirs=permitted_dirs)},
                          ensure_ascii=False, indent=4, sort_keys=True)
    else:
        return {}

def get_scheme(path, restricted=True, permitted_dirs=[]):
    """
    Recursively scans directories and returns a dictionary containing a list
    of files and directories in path
    :param path: root directory to scan
    :param restricted: If it only checks permitted dirs
    :param permitted_dirs: list of permitted directories
    :return: dictionary in json format
    """
    if restricted:
        for directory in permitted_dirs:
            if directory in path:
                restricted = False
    return {
        "folders": {x: get_scheme(path + "/" + x, restricted, permitted_dirs)
                    for x in os.listdir(path) if os.path.isdir(path + "/" + x)},
        "files": [x for x in os.listdir(path) if
                  not os.path.isdir(path + "/" + x)]
    } if not restricted else {}


def get_type(file):
    """
    Returns mimetype of the file given as a parameter
    :param file
    """
    if file:
        file_types = get_permitted_formats()

        # changed so it also works with files named f.e: script.bak.py
        filename, extension = ''.join(file.split('.')[0:-1]),\
                              file.split('.')[-1].lower()

        for file_type in file_types:
            for ext in file_types[file_type]:
                if extension == ext:
                    return file_type + "/" + ext
    return "notype"


# todo: scans the same directory multiple times. Find reason and fix.
def read_scheme(path="", entries={}, file_types={}):
    """
    Scans scheme for files dividing them into categories
    :param path: root directory to scan
    :param entries: a dict: keys are file types (audio, video) and val are lists
    :param file_types: supported file types
    :return: dictionary with files with files sorted in categories (audio, video..)
    """
    app_path = ninia_path + "/app/"
    scheme = get_scheme(app_path + "static/media" + path, restricted=False)
    if not file_types:
        file_types = get_permitted_formats()

    for folder in scheme["folders"]:
        for file_type in file_types:
            try:
                entries = read_scheme(path + "/" + folder,
                                      entries=entries, file_types=file_types)
            except KeyError as ke:
                pass

    for file in scheme["files"]:
        for file_type in file_types:
            if file_type in get_type(file):
                    try:
                        if not path + "/" + file in entries[file_type]:
                            # raise
                            entries[file_type].append(path + "/" + file)
                    except:
                        entries[file_type] = [path + "/" + file]
    return entries


if __name__ == "__main__":
    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))
    # test_index()
    # gen_menu()
