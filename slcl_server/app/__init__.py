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
    return modules.get_index()


# returns json of dir
@app.route("/listdir")
def list_root():
    index = modules.get_index()
    return index if index else json.dumps({"error": "4"})


# returns json of dir
@app.route("/listdir/<path:dir>")
def list_dir(dir):
    index = modules.get_index(dir)
    return index if index else json.dumps({"error": "4"})  # Not a directory


# create the media stream
@app.route("/media_feed")
def media_feed():
    global media
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=modules.get_type(media))


# root directory
@app.route("/menu")
def menu():
    return modules.gen_menu_abslist()


# plays media, allows to input file in url
@app.route("/play/<string:file>")
def open_media(file):

    global media

    media = file.replace("|", "/")

    with open(ninia_path + "/app/config/permissions.json", "r") as format_file:
        file_formats = json.load(format_file)["formats"]

    for file_type in file_formats:
        if file_type in modules.get_type(media):
            return render_template("dynamic.html", ftype=file_type)

    return render_template("default.html")


# return media feed without interface from, allows to input file in url
@app.route("/media_feed/<string:file>")
def return_feed(file):
    media = file.replace("|", "/")
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=modules.get_type(media))


@app.route("/remove/<string:path>")
def remove(path):
    modules.remove(path)


# move/rename file
@app.route("/rename")
def rename():
    old, new = str(request.args.get("old")), str(request.args.get("new"))
    return modules.rename(old, new)


@app.route("/upload", methods=["POST"])
def upload():
    # folder passed as a parameter in the url
    subfolder = request.args.get("folder").replace('"', '').replace("'", '')
    # file of the http post request
    file = request.files["file"]

    return modules.upload(file, subfolder)


if __name__ == "__main__":
    modules.get_type(None)
    app.run(host="0.0.0.0", threaded=True)
