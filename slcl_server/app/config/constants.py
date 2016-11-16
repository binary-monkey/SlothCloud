import os


host = "localhost"
port = "5000"

slcl_path = os.path.dirname(os.path.abspath(__file__)).replace(
    "/app/config" if os.name != "nt" else "\\app\\config", '')

# path of slcl_server/app
app_path = slcl_path + "/app" if os.name != "nt" else slcl_path + "\\app"

# path of slcl_server/app/media
media_path = slcl_path + "/app/media" \
                         "" if os.name != "nt" else slcl_path + "\\app\\media"

# default upload path
upload_folder = media_path + "/uploads".replace(
    '/', '\\' if os.name == "nt" else '/'
)
