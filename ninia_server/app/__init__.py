# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app.config.constants import abspath
from flask import Flask, render_template, request, send_from_directory
from modules import *
from werkzeug.utils import secure_filename

app = Flask(__name__)


# root directory
@app.route("/")
def menu():
    return gen_menu()


@app.route("/antigravity")
def antigravity():
    return ("""
    <html>
    <body><script>
    window.location = "https://xkcd.com/353/"
    </script>
    </noscript>
    <h3> You'll have to enable scripts if you want to fly :/ </h3>
    </noscript></body>
    </html>
    """)


# webpage icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# root directory
@app.route("/index.json")
def index():
    return get_index()


# create the media stream
@app.route("/media_feed")
def media_feed():
    global media
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=get_type(media))


# plays media, allows to input file in url
@app.route("/play/<string:file>")
def open_media(file):

    global media

    media = file.replace("|", "/")

    with open(abspath + "/app/config/permissions.json", "r") as format_file:
        file_formats = json.load(format_file)["formats"]

    for file_type in file_formats:
        if file_type in get_type(media):
            return render_template("dynamic.html", ftype=file_type)

    return render_template("default.html")


# return media feed without interface from, allows to input file in url
@app.route("/media_feed/<string:file>")
def return_feed(file):
    media = file.replace("|", "/")
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=get_type(media))


if __name__ == "__main__":
    get_type(None)
    app.run(host="0.0.0.0", threaded=True)
