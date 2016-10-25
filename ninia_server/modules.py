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


def scan_scheme(path=""):
    """
    Scans scheme for files dividing them into categories
    :param path: root directory to scan
    :return: dictionary with audio and video files dictionaries
    """
    app_path = os.path.dirname(os.path.abspath(__file__)) + "/app/"

    audio_entries = []
    video_entries = []

    scheme = get_scheme(app_path + "static/media/" + path, restricted=False)

    for i in range(len(scheme["files"])):

        if "audio" in get_type(scheme["files"][i]):
            audio_entries.append(path + "/" + scheme["files"][i])
        if "video" in get_type(scheme["files"][i]):
            video_entries.append(path + "/" + scheme["files"][i])

    for j in range(len(scheme["folders"])):
        for key in scheme["folders"][j]:
            temp = scan_scheme(path + "/" + key)

            for entry in temp.get("audio"):
                audio_entries.append(entry)
            for entry in temp.get("video"):
                video_entries.append(entry)

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

    filename, extension = file.split(".")

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

    app_path = os.path.dirname(os.path.abspath(__file__)) + "/app/"

    menu_entries = scan_scheme()

    menu_audio = menu_entries.get("audio")
    menu_video = menu_entries.get("video")

    menu_file = open(app_path + "templates/menu.html", "w")

    # writes beginning section
    menu_file.write(
        """<!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8">
        <title>Ninia - Menu</title>
        </head><body><h1>Ninia (in-dev) - Menu</h1>""")

    # writes audio sectiom
    menu_file.write("<h2>Audio:</h2>")
    for i in range(len(menu_audio)):
        # removes 1st / and changes / to | in order to avoid errors
        entry = menu_audio[i][1:].replace("/", "|")

        menu_file.write(
            '<a href="http://0.0.0.0:5000/play/' + entry + '">' +
            menu_audio[i] + '</a>')
        menu_file.write("<br>")
    # writes video section
    menu_file.write("<h2>Video:</h2>")
    for i in range(len(menu_video)):
        # removes 1st / and changes / to | in order to avoid errors
        entry = menu_video[i][1:].replace("/", "|")

        menu_file.write(
            '<a href="http://0.0.0.0:5000/play/' + entry + '">' +
            menu_video[i] + '</a>')
        menu_file.write("<br>")
    # writes end section
    menu_file.write("</body></html>")


if __name__ == "__main__":
    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))
    # test_index()
    # gen_menu()
