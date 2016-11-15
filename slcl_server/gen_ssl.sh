#!/bin/bash
openssl req \
       -newkey rsa:2048 -nodes -keyout app/static/slcl.key \
       -x509 -days 365 -out app/static/slcl.crt