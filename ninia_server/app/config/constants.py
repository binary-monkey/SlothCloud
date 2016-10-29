import os

ninia_path = os.path.dirname(os.path.abspath(__file__)).replace("/app/config", '')
host = "localhost"
port = "5000"
upload_folder = ninia_path + "/app/static/media/uploads"
