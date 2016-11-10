# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app.config.constants import ninia_path
from flask import Flask, render_template, request, send_from_directory
from flask_autoindex import AutoIndex
import json
import modules
import os


app = Flask(__name__)
AutoIndex(app,browse_root=ninia_path + "/app/static/media", add_url_rules=True)


# ignore this one
@app.route("/antigravity")
def antigravity():
    return ("""
    <html>
    <body><script>
    window.location = "https://xkcd.com/353/"
    </script>
    </noscript>
    <h3> <a href="https://www.xkcd.com/353/">https://www.xkcd.com/353/</a> </h3>
    </noscript></body>
    </html>
    """)


# Returns error codes and descriptions
@app.route("/errors")
def errors():
    with open(ninia_path + "/app/config/errors.json", 'r') as error_list:
        return error_list.read()


# webpage icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# root directory
@app.route("/index.json")
def index():
    """
    :return: json of index
    """
    return modules.get_index()


# returns json of dir
@app.route("/listdir")
def list_root():
    """
    :return: json of root media folder
    """
    index = modules.get_index()
    return index if index else json.dumps({"error": "4"})


# returns json of dir
@app.route("/listdir/<path:dir>")
def list_dir(dir):
    """
    json of specified directory
    :param dir: directory to be shown
    :return: json of the structure of the directory
    """
    index = modules.get_index(dir)
    return index if index else json.dumps({"error": "4"})  # Not a directory


# root directory
@app.route("/menu")
def menu():
    """
    menu with abspath of all files
    :return: main html menu
    """
    return modules.gen_menu_abslist()


# plays media, allows to input file in url
# todo: decent html interface
@app.route("/play/<path:file>")
def open_media(file):
    """
    like "/view" but with html interface
    :param file: file to be visualized
    :return: html template with file
    """

    with open(ninia_path + "/app/config/permissions.json", "r") as format_file:
        file_formats = json.load(format_file)["formats"]

    for file_type in file_formats:
        if file_type in modules.get_type(file):
            return render_template("dynamic.html", ftype=file_type, path=file)

    return render_template("default.html")


# remove file
@app.route("/remove/<path:path>")
def remove(path):
    """
    removes file or directory (rmtree) specified in path
    :param path: path to be removed
    :return: error if errors were made
    """
    return modules.remove(path)


# move/rename file
@app.route("/rename")
def rename():
    """
    rename file
    :return: error if errors were made
    """
    old, new = str(request.args.get("old")), str(request.args.get("new"))
    return modules.rename(old, new)


@app.route("/view/<path:path>")
def view(path):
    """
    Sends file specified in uri
    :return: requested file
    """

    if os.path.isfile(ninia_path + "/app/static/media/" + path):
        return send_from_directory(
            ninia_path + "/app/static/media/" + ''.join(
                path.split('/')[0:-1]) if '/' in path else '',
            path.split('/')[-1])
    else:
        return json.dumps({"error": "2"})


@app.route("/upload", methods=["POST"])
def upload():
    """
    Used to upload files to server
    :return: error if errors were made
    """
    # folder passed as a parameter in the url
    subfolder = request.args.get("folder").replace('"', '').replace("'", '')
    # file of the http post request
    file = request.files["file"]

    return modules.upload(file, subfolder)


if __name__ == "__main__":
    modules.get_type(None)
    app.run(host="0.0.0.0", threaded=True)
