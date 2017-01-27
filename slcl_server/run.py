#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port, app_path
from app import paths
from sys import argv

# Temporary argument-deactivation of https so it works on windows systems.
if len(argv) > 1 and argv[1] == "-ns":
    app.run(host=host, port=port, threaded=True)
else:
    context = (paths.app('static/slcl.crt'), paths.app('static/slcl.key'))
    app.run(host=host, port=port, ssl_context=context, threaded=True)
