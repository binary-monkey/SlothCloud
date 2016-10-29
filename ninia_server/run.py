# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port

app.run(host=host, port=port, threaded=True)
