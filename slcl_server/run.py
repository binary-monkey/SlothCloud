# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port, app_path
from sys import argv
from utils import nt

# Temporary argument-deactivation of https so it works on windows systems.
if len(argv) > 1 and argv[1] == "-ns":
    app.run(host=host, port=port, threaded=True)
else:
    context = (nt(app_path + '/static/slcl.crt'), nt(app_path + '/static/slcl.key'))
    app.run(host=host, port=port, ssl_context=context, threaded=True)