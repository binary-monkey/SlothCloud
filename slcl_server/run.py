# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port, app_path
from OpenSSL import SSL
from utils import nt

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file(nt(app_path + '/static/slcl.key'))
context.use_certificate_file(nt(app_path + '/static/slcl.crt'))

app.run(host=host, port=port, ssl_context=context, threaded=True)