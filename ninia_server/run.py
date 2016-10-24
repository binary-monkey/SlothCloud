# !/usr/bin/python3
# -*- coding: utf-8 -*-

from ninia_server.app import app

app.run(host='0.0.0.0', threaded=True)
