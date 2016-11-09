# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app.config.constants import upload_folder
from flask import Flask, render_template, request, send_from_directory
from flask_autoindex import AutoIndex
from modules import *
from utils import is_allowed, get_config, makedirs
from werkzeug.utils import secure_filename

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
    return index if index else json.dumps({"error": "4"})  # Not a directory


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


@app.route("/rename")
def rename():

    old, new = str(request.args.get("old")), str(request.args.get("new"))

    if old != "None" and new != "None":

        if os.path.isfile(ninia_path + "/app/static/media/" + old):

            if old.split(".")[-1].lower() == new.split(".")[-1].lower() and len(
                new.split(".")) > 1:

                try:
                    # create necessary directories
                    if len(new.split('/')) > 1:
                        makedirs(''.join([x + '/' for x in new.split('/')[0:-1]]))

                    os.rename(
                        ninia_path + "/app/static/media/" + old,
                        ninia_path + "/app/static/media/" + new
                    )
                    clean_dir(ninia_path + "/app/static/media")
                    return "File (1) moved to (2)<br>(1):%s<br>(2):%s" % (old, new)

                except Exception as ex:
                    clean_dir(ninia_path + "/app/static/media")
                    # System error
                    return json.dumps({"error": "0"})
            else:
                print(old.split(".")[-1].lower() + "__" + new.split(".")[-1].lower())
                # Invalid filename
                return json.dumps({"error": "3"})
        else:
            # File not found
            return json.dumps({"error": "2"})
    else:
        # Missing required parameters
        return json.dumps({"error": "1", "parameters": ["old", "new"] })


@app.route("/upload", methods=["POST"])
def upload():
    # folder passed as a parameter in the url
    subfolder = request.args.get("folder").replace('"', '').replace("'", '')
    # file of the http post request
    file = request.files["file"]

    if not file:
        # File not found
        return json.dumps({"error": "2"})

    if len(file.filename.split(".")) < 2:
        # Incorrect filename
        return json.dumps({"error": "3"})

    if not is_allowed(file.filename.split(".")[-1]):
        # Unsupported extension
        return json.dumps({"error": "5"})

    filename = secure_filename(file.filename)
    filename = subfolder + "/" + filename
    temp_path = upload_folder


    if not subfolder.split('/')[0].lower().strip() in get_config("permissions")[
        "reserved words"]:
        # create necessary folders
        if len(subfolder.split('/')) > 1:
            makedirs(''.join([x + '/' for x in subfolder.split('/')[0:-1]]))

        # save file in abspath
        try:
            file.save(''.join([upload_folder] + ["/" + x for x in filename.split('/')]))
        except:
            # System Error
            return json.dumps({"error": "0"})
        # function that removes all empty directories
        clean_dir(upload_folder)

        return "[*] File:" + filename + "was successfully uploaded."
    else:
        return json.dumps({"error": "6"})


if __name__ == "__main__":
    get_type(None)
    app.run(host="0.0.0.0", threaded=True)
