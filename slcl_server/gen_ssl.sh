#!/bin/bash
sudo openssl genrsa -des3 -out app/static/slcl.key 2048
sudo openssl req -new -key app/static/slcl.key -out app/static/slcl.csr
sudo cp app/static/slcl.key app/static/slcl.key.org
sudo openssl rsa -in app/static/slcl.key.org -out app/static/slcl.key
sudo openssl x509 -req -days 365 -in app/static/slcl.csr -signkey app/static/slcl.key -out app/static/slcl.crt
rm app/static/slcl.key.org
rm app/static/slcl.csrgit