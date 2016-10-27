# !/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory

from modules import *

app = Flask(__name__)
abspath = os.path.dirname(os.path.abspath(__file__))

media = ""


# root directory
@app.route("/")
def menu():
    return gen_menu()


# root directory
@app.route("/index.json")
def index():
    return get_index()


# webpage icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# plays media, allows to input file in url
@app.route("/play/<string:file>")
def open_media(file):

    global abspath, media

    media = file.replace("|", "/")

    with open(abspath + "/dictionaries/formats.json", "r") as format_file:
        file_formats = json.load(format_file)

    for file_type in file_formats:
        if file_type in get_type(media):
            return render_template(file_type + ".html")

    return render_template("default.html")


# create the media stream
@app.route("/media_feed")
def media_feed():
    global media
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=get_type(media))


# return media feed without interface from, allows to input file in url
@app.route("/media_feed/<string:file>")
def return_feed(file):
    media = file.replace("|", "/")
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=get_type(media))


if __name__ == "__main__":
    get_type(None)
    app.run(host="0.0.0.0", threaded=True)
