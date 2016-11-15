# !/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
from app.config.constants import host, port, app_path
from OpenSSL import SSL

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file(app_path + '/static/slcl.key')
context.use_certificate_file(app_path + '/static/slcl.crt')

app.run(host=host, port=port, debug=False, ssl_context=context, threaded=True)