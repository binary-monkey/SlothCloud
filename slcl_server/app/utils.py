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
    """
    deletes all empty directories in dir
    :param path: path to be cleaned
    :return:
    """
    for element in os.listdir(path):
        if os.path.isdir(path + '/' + element) and not os.listdir(path + '/' + element):
            rmtree(path + '/' + element)


def get_config(json_filename):
    """
    returns dict of config json
    :param json_filename: path to config file
    :return: dict of the json file
    """
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/config/" +
                          json_filename + ".json", 'r') as file:
            return json.load(file)
    except FileNotFoundError as fnfe:
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
    :return:
    """
    if path[-1] == '/':
        path = path[0:-1]
    error = ""
    if '/' in path:
        dirlist = path.split("/")
        try:
            os.mkdir(ninia_path + "/app/static/media/" +
                     str(_prevpath) + secure_filename(dirlist[0]))
        except FileExistsError:
            pass
        if not error:
            error = makedirs(path=''.join(
                [x + '/' for x in dirlist[1:]]),
                _prevpath=_prevpath +
                         ''.join(dirlist[0]))
    else:
        try:
            os.mkdir(ninia_path + "/app/static/media/" + prevpath + '/' + secure_filename(path))
        except:
            return json.dumps({"error": "0"})
    return error