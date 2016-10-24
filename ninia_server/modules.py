#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json

"""
Returns json file containing the files and directories subsequent to the path
passed as a parameter. Each folder has a list containing everything in of it.

:param path: optional, default=/ninia_server/app/root/static/media/
"""

def get_index(path=""):
    if not path:
        scheme = {
            "root": {
                "static": [

                ]
            }
        }

        # returns the path to the current file
        # multiple variables are just for better understanding
        root_path = os.path.dirname(os.path.abspath(__file__))
        media_path = root_path + "/app/static/media/"
        path = media_path
    else:
        scheme = {}

    # returns a list containing a json-structured representation of subsequent
    # dirs and files
    def get_scheme(x):
        return [{y: get_scheme(x + "/" + y)} if os.path.isdir(x + "/" + y)
                else y for y in os.listdir(x)]

    scheme["root"]["static"] = get_scheme(path)
    # print(json.dumps(, indent=4, sort_keys=True))
    return json.dumps(scheme, ensure_ascii=False)


"""
Returns mimetype of the file given as a parameter

:param file
"""

def get_type(file):

    root_path = os.path.dirname(os.path.abspath(__file__))
    dict_path = root_path + "/app/dictionaries/"

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


"""
Autogenerates a menu with the media files stored in app/static/media/
"""

def gen_menu():
    root_path = os.path.dirname(os.path.abspath(__file__))
    static_path = root_path + "/app/"
    menu_entries = os.listdir(static_path + "static/media/")
    menu_audio = []
    menu_video = []

    for i in range(len(menu_entries)):
        if "audio" in get_type(menu_entries[i]):
            menu_audio.append(menu_entries[i])
        if "video" in get_type(menu_entries[i]):
            menu_video.append(menu_entries[i])

    menu_file = open(static_path + "templates/menu.html", "w")

    # writes beginning section
    menu_file.write("""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>PyMediaServer - Menu</title>
    </head><body><h1>PyMediaServer (in-dev) - Menu</h1>""")

    # writes audio sectiom
    menu_file.write("<h2>Audio:</h2>")
    for i in range(len(menu_audio)):
        menu_file.write('<a href="http://0.0.0.0:5000/play/' + menu_audio[i] + '">' + menu_audio[i] + '</a>')
        menu_file.write("<br>")
    # writes video section
    menu_file.write("<h2>Video:</h2>")
    for i in range(len(menu_video)):
        menu_file.write('<a href="http://0.0.0.0:5000/play/' + menu_video[i] + '">' + menu_video[i] + '</a>')
        menu_file.write("<br>")
    # writes end section
    menu_file.write("</body></html>")

