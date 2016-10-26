#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os


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


def scan_scheme(path="", video_entries=[], audio_entries=[]):
    """
    Scans scheme for files dividing them into categories
    :param path: root directory to scan
    :param video_entries: video entries in previous folders
    :param audio_entries: audio entries in previous folders
    :return: dictionary with audio and video files dictionaries
    """
    app_path = os.path.dirname(os.path.abspath(__file__)) + "/app/"

    scheme = get_scheme(app_path + "static/media" + path, restricted=False)

    for file in scheme["files"]:
        if "audio" in get_type(file):
            audio_entries.append(path + "/" + file)
        elif "video" in get_type(file):
            video_entries.append(path + "/" + file)

    for folder in scheme["folders"]:
        audio_entries = scan_scheme(path + "/" + folder,
                                    audio_entries=audio_entries)["audio"]
        video_entries = scan_scheme(path + "/" + folder,
                                    video_entries=video_entries)["video"]

    return {"audio": audio_entries, "video": video_entries}


# todo: optimize restriction check
def get_index(path=""):
    """
    Returns json file containing the files and directories subsequent to the path
    passed as a parameter. Each folder has a list containing everything in of it.
    :param path: optional, default=root
    """

    if not path:
        # path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(os.path.abspath(__file__)) + "/app/static/media"

    with open('app/config/permissions.json') as permission_file:
        permitted_dirs = json.load(permission_file)["directories"]["index"]

    return json.dumps({path: get_scheme(path, permitted_dirs=permitted_dirs)},
                      ensure_ascii=False, indent=4, sort_keys=True)


def get_type(file):
    """
    Returns mimetype of the file given as a parameter
    :param file
    """

    dict_path = os.path.dirname(os.path.abspath(__file__)) \
                + "/app/dictionaries/"

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


def gen_menu():
    """
    Autogenerates a menu with the media files stored in app/static/media/
    """
    host = "localhost"
    port = "5000"
    app_path = os.path.dirname(os.path.abspath(__file__)) + "/app/"

    menu_entries = scan_scheme()
    menu_file = open(app_path + "templates/menu.html", "w")

    # writes beginning section
    menu_file.write(
        """<!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Menu</title>
        </head><body><h1>Ninia (in-dev) - Menu</h1>""")

    # writes audio sectiom
    menu_file.write("<h2>Audio:</h2>")

    for audio_path in menu_entries["audio"]:
        # removes 1st / and changes / to | in order to avoid errors
        entry = audio_path[1:].replace("/", "|")

        menu_file.write(
            '<a href="http://' + host + ':' + port + '/play/' + entry + '">' +
            audio_path + '</a>')
        menu_file.write("<br>")
    # writes video section
    menu_file.write("<h2>Video:</h2>")

    for video_path in menu_entries["video"]:

        # removes 1st / and changes / to | in order to avoid errors
        entry = video_path[1:].replace("/", "|")

        menu_file.write(
            '<a href="http://' + host + ':' + port + '/play/' + entry + '">' +
            video_path + '</a>')
        menu_file.write("<br>")
    # writes end section
    menu_file.write("</body></html>")


if __name__ == "__main__":
    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))
    test_index()
    # gen_menu()
