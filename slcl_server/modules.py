#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The goal of this file is to have here the functions app/__init__.py uses
so that file can be read with no difficulties.
"""

from app.config.constants import ninia_path, host, port, upload_folder
from app.utils import get_permitted_formats
import json
import os
from shutil import rmtree
from utils import clean_dir, get_config, is_allowed, makedirs
from werkzeug.utils import secure_filename

media = ""


def gen_menu_abslist():
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


def gen_menu_table():
    """
    Autogenerates a table with the media files stored in app/static/media/
    :return: html file of menu
    """
    menu_entries = read_scheme()

    # menu_file variable will be the html file.
    # writes beginning section
    menu_file = """
        <!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Main Index</title>
        </head><body>
        <TABLE BORDER="5"    WIDTH="50%"   CELLPADDING="4" CELLSPACING="3">
            <TR>
                <TH COLSPAN="2"><BR><H3>Ninia (in-dev) - Menu</H3>
                </TH>
            </TR>
            <TR ALIGN="CENTER">"""

    for category in sorted(menu_entries.keys()):
        # Category name, first letter is upper
        menu_file += "\n<TD>" + category[0].upper() + category[1:] + "</TD>"
        # List of all entries in category
        for entry in sorted(menu_entries[category]):
            entry = entry[1:].replace("/", "|")
            menu_file += '\n<TD><a href="http://' + host + ':' + port + '/play/' + \
                         entry + '">' + entry.replace("|", "/") + '</TD>'
            ##menu_file += "<br>"
        menu_file += """</TR><TR ALIGN="CENTER">"""

    # writes end section
    menu_file += "</TR></TABLE></body></html>"
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


def rename(old, new):
    """
    renames path or folder
    :param old: file to be renamed
    :param new: new name o path
    :return: error if errors happened
    """
    if old != "None" and new != "None":

        if os.path.isfile(ninia_path + "/app/static/media/" + old):

            if old.split(".")[-1].lower() == new.split(".")[
                -1].lower() and len(
                    new.split(".")) > 1:

                try:
                    # create necessary directories
                    if len(new.split('/')) > 1:
                        makedirs(''.join(
                            [x + '/' for x in new.split('/')[0:-1]]))

                    os.rename(
                        ninia_path + "/app/static/media/" + old,
                        ninia_path + "/app/static/media/" + new
                    )
                    clean_dir(ninia_path + "/app/static/media")
                    return "File (1) moved to (2)<br>(1):%s<br>(2):%s" % (
                    old, new)

                except Exception as ex:
                    clean_dir(ninia_path + "/app/static/media")
                    # System error
                    return json.dumps({"error": "0"})
            else:
                print(old.split(".")[-1].lower() + "__" + new.split(".")[
                    -1].lower())
                # Invalid filename
                return json.dumps({"error": "3"})
        else:
            # File not found
            return json.dumps({"error": "2"})
    else:
        # Missing required parameters
        return json.dumps({"error": "1", "parameters": ["old", "new"]})


def remove(path):
    """
    removes path and everything contained in it
    :param path: path to be removed
    :return: error if error happens
    """

    # todo: authentication


    if path[0] == '/':
        path = path[1:]
    path = ninia_path + "/app/static/media/" + path
    try:
        if os.path.isfile(path):
            os.rmdir(path)
        elif os.path.isdir(path):
            rmtree(path)
        else:
            return json.dumps({"error": "4"})
        return ""
    except Exception:
        return json.dumps({"error": "0"})


def upload(file, folder):
    if not file:
        # File not found
        return json.dumps({"error": "2"})

    if len(file.filename.split(".")) < 2:
        # Incorrect filename
        return json.dumps({"error": "3"})

    if not is_allowed(file.filename.split(".")[-1]):
        # Unsupported extension
        return json.dumps({"error": "5"})

    filename = secure_filename(file.filename)
    filename = folder + "/" + filename
    temp_path = upload_folder


    if not folder.split('/')[0].lower().strip() in get_config("permissions")[
        "reserved words"]:
        # create necessary folders
        if len(folder.split('/')) > 1:
            makedirs(''.join([x + '/' for x in folder.split('/')[0:-1]]))

        # save file in abspath
        try:
            file.save(''.join([upload_folder] + [
                "/" + x for x in filename.split('/')]))
        except:
            # System Error
            return json.dumps({"error": "0"})
        # function that removes all empty directories
        clean_dir(upload_folder)

        return ""
    else:
        return json.dumps({"error": "6"})


if __name__ == "__main__":
    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))
    # test_index()
    # gen_menu()
