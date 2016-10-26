#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os

# <definition of global variables>
abspath = os.path.dirname(os.path.abspath(__file__))
host = "localhost"
port = "port"
# </definition of global variables>


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


# todo: scans the same directory multiple times. Find reason and fix.
def scan_scheme(path="", video_entries=[], audio_entries=[]):
    """
    Scans scheme for files dividing them into categories
    :param path: root directory to scan
    :param video_entries: video entries in previous folders
    :param audio_entries: audio entries in previous folders
    :return: dictionary with audio and video files dictionaries
    """
    app_path = abspath + "/app/"
    scheme = get_scheme(app_path + "static/media" + path, restricted=False)

    for folder in scheme["folders"]:
        audio_entries = scan_scheme(path + "/" + folder,
                                    audio_entries=audio_entries)["audio"]
        video_entries = scan_scheme(path + "/" + folder,
                                    video_entries=video_entries)["video"]

    for file in scheme["files"]:
        if "audio" in get_type(file):
            if not path + "/" + file in audio_entries:
                audio_entries.append(path + "/" + file)
        elif "video" in get_type(file):
            if not path + "/" + file in video_entries:
                video_entries.append(path + "/" + file)

    return {"audio": audio_entries, "video": video_entries}


# todo: optimize restriction check
def get_index(path=""):
    """
    Returns json file containing the files and directories subsequent to the path
    passed as a parameter. Each folder has a list containing everything in of it.
    :param path: optional, default=root
    """

    if not path:
        path = abspath + "/app/static/media"

    with open('app/config/permissions.json') as permission_file:
        permitted_dirs = json.load(permission_file)["directories"]["index"]

    return json.dumps({path: get_scheme(path, permitted_dirs=permitted_dirs)},
                      ensure_ascii=False, indent=4, sort_keys=True)


def get_type(file):
    """
    Returns mimetype of the file given as a parameter
    :param file
    """

    dict_path = abspath + "/app/dictionaries/"

    # Generate dictionaries
    with open(dict_path + 'audio_dict.json', 'r') as fp:
        audio_dict = json.load(fp)
    with open(dict_path + 'video_dict.json', 'r') as fp:
        video_dict = json.load(fp)

    # changed so it also works with files named f.e: script.bak.py
    filename, extension = ''.join(file.split('.')[0:-1]), file.split('.')[-1]

    if extension in audio_dict:
        return "audio/" + audio_dict[extension]
    elif extension in video_dict:
        return "video/" + video_dict[extension]
    else:  # file not supported
        return ""


# stays for review, use gen_menu instead
def gen_menu_file():
    """
    Autogenerates a menu with the media files stored in app/static/media/
    """
    global host, port
    app_path = abspath + "/app/"

    menu_entries = scan_scheme()
    menu_file = open(app_path + "templates/menu.html", "w")

    # writes beginning section
    menu_file.write(
        """<!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Menu</title>
        </head><body><h1>Ninia (in-dev) - Menu</h1>""")

    for category in menu_entries:
        # Category name, first letter is upper
        menu_file.write("\n<h2>" + category[0].upper() + category[1:] + "</h2>")
        # List of all entries in category
        for entry in menu_entries[category]:
            entry = entry[1:].replace("/", "|")
            menu_file.write(
                '\n<a href="http://' + host + ':' + port + '/play/' + entry +
                '">' + entry.replace("|", "/") + '</a>')
            menu_file.write("<br>")

    # writes end section
    menu_file.write("</body></html>")


def gen_menu():
    """
    Autogenerates a menu with the media files stored in app/static/media/
    """
    global host, port

    menu_entries = scan_scheme()

    # menu_file variable will be the html file.
    # writes beginning section
    menu_file = """
        <!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Menu</title>
        </head><body><h1>Ninia (in-dev) - Menu</h1>"""

    for category in menu_entries:
        # Category name, first letter is upper
        menu_file += "\n<h2>" + category[0].upper() + category[1:] + "</h2>"
        # List of all entries in category
        for entry in menu_entries[category]:
            entry = entry[1:].replace("/", "|")
            menu_file += '\n<a href="http://' + host + ':' + port + '/play/' + \
                         entry + '">' + entry.replace("|", "/") + '</a>'
            menu_file += "<br>"

    # writes end section
    menu_file += "</body></html>"

if __name__ == "__main__":
    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))
    # test_index()
    # gen_menu()
