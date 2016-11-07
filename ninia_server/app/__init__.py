# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app.config.constants import upload_folder
from flask import Flask, render_template, request, send_from_directory
from modules import *
from utils import is_allowed, get_permissions
from werkzeug.utils import secure_filename
from flask_autoindex import AutoIndex

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


# returns json of dir
@app.route("/listdir")
def list_root():
    index = get_index()
    return index if index else "Invalid directory."


# returns json of dir
@app.route("/listdir/<path:dir>")
def list_dir(dir):
    index = get_index(dir)
    return index if index else "Invalid directory."


# create the media stream
@app.route("/media_feed")
def media_feed():
    global media
    return send_from_directory(os.path.join(app.root_path, 'static/media'),
                               media, mimetype=get_type(media))


# root directory
@app.route("/menu")
def menu():
    return gen_menu()


# plays media, allows to input file in url
@app.route("/play/<string:file>")
def open_media(file):

    global media

    media = file.replace("|", "/")

    with open(ninia_path + "/app/config/permissions.json", "r") as format_file:
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


@app.route("/upload", methods=["POST"])
def upload():
    # folder passed as a parameter in the url
    subfolder = request.args.get("folder").replace('"', '').replace("'", '')
    # file of the http post request
    file = request.files["file"]

    # if file exists, has an extension and the extension is supported
    if file and len(file.filename.split(".")) > 1 \
            and is_allowed(file.filename.split(".")[-1]):

        filename = secure_filename(file.filename)
        filename = subfolder + "/" + filename
        temp_path = upload_folder

        try:  # May be unnecessary
            if not subfolder.split('/')[0].lower().strip() in get_permissions()[
                "reserved words"]:
                # create necessary folders
                for path in subfolder.split('/'):
                    try:
                        os.mkdir(temp_path + "/" + path)
                    except FileExistsError as fee:
                        pass
                    temp_path += "/" + path

                # save file in abspath
                file.save(''.join([upload_folder] + ["/" + x for x in filename.split('/')]))
                # function that removes all empty directories
                clean_dir(upload_folder)

                return "[*] File:" + filename + "was successfully uploaded."
        except:
            pass

    return "Error."


if __name__ == "__main__":
    get_type(None)
    app.run(host="0.0.0.0", threaded=True)
