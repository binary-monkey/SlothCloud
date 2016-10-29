# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host

app.run(host=host, threaded=True)
