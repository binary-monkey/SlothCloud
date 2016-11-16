# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port, app_path
from utils import nt

context = (nt(app_path + '/static/slcl.crt'), nt(app_path + '/static/slcl.key'))
app.run(host=host, port=port, ssl_context=context, threaded=True)