#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json

"""
Returns json file containing the files and directories subsequent to the path
passed as a parameter. Each folder has a list containing everything in of it.

:param path: optional, default=root
"""


# todo: ignore not permitted folders
def get_index(path=""):

    if not path:
        path = os.path.dirname(os.path.abspath(__file__))

    def get_scheme(path):
        scheme = {
            "folders": [],
            "files": []
        }
        for x in os.listdir(path):
            if os.path.isdir(path + "/" + x):
                scheme["folders"].append({x: get_scheme(path + "/" + x)})
            else:
                scheme["files"].append(x)

        return scheme

    return json.dumps(get_scheme(path), ensure_ascii=False,
                      indent=4, sort_keys=True)

"""
Returns mimetype of the file given as a parameter

:param file
"""


def get_type(file):
    # Generate dictionaries
    with open('ninia_server/app/dictionaries/audio_dict.json', 'r') as fp:
        audio_dict = json.load(fp)
    with open('ninia_server/app/dictionaries/video_dict.json', 'r') as fp:
        video_dict = json.load(fp)

    filename, extension = file.split(".")

    if extension in audio_dict:
        return "audio/" + audio_dict[extension]
    elif extension in video_dict:
        return "video/" + video_dict[extension]
    else:  # file not supported
        return ""


"""
Autogenerates a menu with the media files stored in app/static/media/
"""


def gen_menu():
    menu_entries = os.listdir("ninia_server/app/static/media")
    menu_audio = []
    menu_video = []

    for i in range(len(menu_entries)):
        if "audio" in get_type(menu_entries[i]):
            menu_audio.append(menu_entries[i])
        if "video" in get_type(menu_entries[i]):
            menu_video.append(menu_entries[i])

    menu_file = open("ninia_server/app/templates/menu.html", "w")

    # writes beginning section
    menu_file.write("""<!DOCTYPE html><html lang="en">
    <head><meta charset="UTF-8">
    <title>PyMediaServer - Menu</title>
    </head>
    <body><h1>PyMediaServer (in-dev) - Menu</h1>""")

    # writes audio sectiom
    menu_file.write("<h2>Audio:</h2>")
    for i in range(len(menu_audio)):
        menu_file.write('<a href="http://0.0.0.0:5000/play/' + menu_audio[i] +
                        '">' + menu_audio[i] + '</a>')
        menu_file.write("<br>")
    # writes video section
    menu_file.write("<h2>Video:</h2>")
    for i in range(len(menu_video)):
        menu_file.write('<a href="http://0.0.0.0:5000/play/' + menu_video[i] +
                        '">' + menu_video[i] + '</a>')
        menu_file.write("<br>")
    # writes end section
    menu_file.write("</body></html>")


if __name__ == "__main__":

    # Test get_index() by printing the returned json of the root folder
    def test_index(path=""):
        print(json.dumps(json.loads(get_index(path), encoding="utf-8"),
                         ensure_ascii=False, indent=4, sort_keys=True))

