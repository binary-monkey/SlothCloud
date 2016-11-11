"""
Here we define functions required in modules.py but that are not called from
app/__init__.py
"""

from app.config.constants import app_path, slcl_path
import json
import os
from shutil import rmtree
from werkzeug.utils import secure_filename


def clean_dir(path):
    """
    deletes all empty directories in dir
    :param path: path to be cleaned
    :return:
    """
    for element in os.listdir(nt(path)):
        if os.path.isdir(nt(path + '/' + element)) and not os.listdir(
                nt(path + '/' + element)):
            rmtree(nt(path + '/' + element))


def get_config(json_filename):
    """
    returns dict of config json
    :param json_filename: path to config file
    :return: dict of the json file
    """
    try:
        with open(nt(app_path + "/config/" + json_filename + ".json"),
                  'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "0"}


def get_permitted_formats():
    """
    returns all permitted formats specified in config.permissions.json
    :return: dictionary of permitted formats
    """
    return get_config("permissions")["formats"]


def is_allowed(fformat):
    """
    checks if format is allowed
    :param fformat: format to be checked
    :return: True if file is allowed else False
    """
    formats = get_permitted_formats()
    for category in formats:
        for extension in formats[category]:
            if fformat == extension:
                return True

    return False


def makedirs(path, _prevpath=""):
    """
    Creates full path passed as parameter
    :param path: complete path to be created
    :param _prevpath: empty
    :return: error if errors were made
    """
    if path[-1] == '/':
        path = path[0:-1]
    error = ""
    if '/' in path:
        dirlist = path.split("/")
        try:
            os.mkdir(nt(slcl_path + "/app/static/media/" +
                     str(_prevpath) + secure_filename(dirlist[0])))
        except FileExistsError:
            pass
        if not error:
            error = makedirs(path=''.join(
                [x + '/' for x in dirlist[1:]]),
                _prevpath=_prevpath + ''.join(dirlist[0]))
    else:
        try:
            os.mkdir(nt(slcl_path + "/app/static/media/" + _prevpath + '/'
                        + secure_filename(path)))
        except Exception:
            return json.dumps({"error": "0"})
    return error


def nt(path):
    """
    Takes a path with '/' separators and returns the correct one for the OS
    :param path: path to be corrected
    :return: usable path
    """
    return path.replace('/', '\\') if os.name == "nt" else path
