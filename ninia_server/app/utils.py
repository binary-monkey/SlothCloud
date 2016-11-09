"""
Here we define functions required in modules.py but that are not called from
app/__init.py
"""

from app.config.constants import ninia_path
import json
import os
from shutil import rmtree
from werkzeug.utils import secure_filename


def clean_dir(path):
    for element in os.listdir(path):
        if os.path.isdir(path + '/' + element) and not os.listdir(path + '/' + element):
            rmtree(path + '/' + element)


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


def makedirs(path, prevpath=""):
    if path[-1] == '/':
        path = path[0:-1]
    error = ""
    if '/' in path:
        dirlist = path.split("/")
        try:
            os.mkdir(ninia_path + "/app/static/media/" +
                     str(prevpath) + secure_filename(dirlist[0]))
        except FileExistsError:
            pass
        if not error:
            error = makedirs(path=''.join(
                [x + '/' for x in dirlist[1:]]),
                prevpath=prevpath +
                         ''.join(dirlist[0]))
    else:
        try:
            os.mkdir(ninia_path + "/app/static/media/" + prevpath + '/' + secure_filename(path))
        except:
            return json.dumps({"error": "0"})
    return error