#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import modules
from . import paths
from .config.credentials import secret_key
from .utils import makedirs as mkd
from .utils import nt

import json
import os

from flask import escape, Flask, redirect, render_template, request, send_from_directory
from flask import session, url_for
# from flask_autoindex import AutoIndex

app = Flask(__name__)
app.secret_key = secret_key
# AutoIndex(app, browse_root=paths.media, add_url_rules=True)


#
#
#
# Logging Resources
#
#
#

@app.route('/')
def logged():
    if "username" in session:
        return "Logged in as %s" % escape(session["username"])
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    TODO: ENCRYPTED CONNECTION
    Gets login data
    :return: form to get data or redirect
    """
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("logged"))
    return """
    <form action="" method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
    """
#
#
#
# Basic Resources
#
#
#


# Returns error codes and descriptions
@app.route("/errors")
def errors():
    with open(paths.app("/config/errors.json"), 'r') as error_list:
        return error_list.read()


# root directory
@app.route("/index.json")
def index():
    """
    :return: json of index
    """
    return modules.get_index()


# returns json of dir
@app.route("/listdir")
@app.route("/listdir/")
def list_root():
    """
    :return: json of root media folder
    """
    rindex = modules.get_index()
    return rindex if rindex else json.dumps({"error": "4"})


# returns json of dir
@app.route("/listdir/<path:directory>")
def list_dir(directory):
    """
    json of specified directory
    :param directory: directory to be shown
    :return: json of the structure of the directory
    """
    dindex = modules.get_index(directory)
    print(dindex)
    return dindex if dindex else json.dumps({"error": "4"})  # Not a directory


@app.route("/map")
def map_site():
    """
    Map of the site
    :return: a list of all the routes and associated functions of the API
    """
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and modules.has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return json.dumps(links)


#
#
#
# File Obtention
#
#
#


@app.route("/view/<path:path>")
def view(path):
    """
    Sends file specified in url
    :return: requested file
    """

    if path and os.path.isfile(paths.media(path)):
        return send_from_directory(
            # path to file folder
            paths.media(
                ''.join(path.split('/')[0:-1]) if '/' in path else ''
            ) + '/',
            #file
            path.split('/')[-1])
    else:
        return json.dumps({"error": "2"})


#
#
#
# Web Resources
#
#
#


@app.route("/css")
def css():
    template = render_template(nt("css/" + request.args.get("filename")))
    with open(paths.app("templates/rendered/" + request.args.get("filename")),
              'w') as f:
        f.write(template)
    return send_from_directory(paths.app("templates/rendered"),
                               filename=request.args.get("filename"))


# view allowed file in html template
# todo: decent html interface, working media controls
@app.route("/display/<path:file>")
def display(file):
    """
    like "/view" but with html interface
    :param file: file to be visualized
    :return: html template with file
    """
    file = nt(file)
    with open(paths.app("config/permissions.json"), "r") as format_file:
        file_formats = json.load(format_file)["formats"]

    for file_type in file_formats:
        if file_type in modules.get_type(file):
            return render_template("dynamic.html", ftype=file_type, path=file)

    return render_template("default.html")


# webpage icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/fonts")
def fonts():
    return send_from_directory(paths.app("/templates/fonts"),
                               request.args.get("filename"))


@app.route("/js/<path:path>")
def js(path):
    return render_template("js/" + path)


# root directory
@app.route("/menu")
def menu():
    """
    menu with abspath of all files
    :return: main html menu
    """
    path = str(request.args.get("path"))

    scheme = json.loads(str(modules.get_index(path if path != "None" else '')))
    if len(path) > 0 and path[0] == '/':
        path = path[1:]
    if len(path.split('/')) <= 1:
        prevdir = ''
    else:
        prevdir = ''.join(['/' + x for x in path.split('/')[:-1]])

    return render_template("menu.html",
                           directory=path if path != "None" else '',
                           files=sorted(
                               scheme[''.join(key for key in scheme)]["files"],
                               key=lambda s: s.lower()) if scheme else [],
                           folders=sorted(
                               scheme[''.join(key for key in scheme)][
                                   "folders"],
                               key=lambda s: s.lower()) if scheme else [],
                           prevdir=prevdir,
                           root=True if path == "None" else False,
                           title="Index")


@app.route("/static")
def get_static():
    return send_from_directory(
        paths.app('static/' + request.args.get("filename")))


@app.route("/templates/<path:path>")
def templates(path):
    return render_template(nt(path))


#
#
#
# File/Directory Operations
#
#
#


# Create directory
@app.route("/makedir")
def makedir():
    if not str(request.args.get('dirname')) in ("None", ""):
        err = mkd(request.args.get('dirname'))
        return err if err else ''

    return '{"error":"3"}'


# upload file
@app.route("/upload", methods=["POST"])
def upload():
    """
    Used to upload files to server
    :return: error if errors were made
    """

    # todo: should we check if file existed or is it better to overwrite?

    # folder passed as a parameter in the url
    subfolder = nt(request.args.get("folder").replace('"', '').replace("'", ''))
    # file of the http post request
    file = request.files["file"]

    return modules.upload(file, subfolder)


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


#
#
#
# Other
#
#
#


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
