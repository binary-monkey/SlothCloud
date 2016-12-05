#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.constants import static_path
from os.path import join
from OpenSSL import crypto

cert_file = "slcl.crt"
key_file = "slcl.key"


def create_self_signed_cert():
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = input("Country Name (2 letter code) [AU]: ")
    cert.get_subject().ST = \
        input("State or Province Name (full name) [Some-State]: ")
    cert.get_subject().L = input("Locality Name (eg, city) []: ")
    cert.get_subject().O = \
        input("Organization Name (eg, company) [Internet Widgits Pty Ltd]: ")
    cert.get_subject().OU = input("Organizational Unit Name (eg, section) []: ")
    cert.get_subject().CN = \
        input("Common Name (e.g. server FQDN or YOUR name) []: ")
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(join(static_path, cert_file), "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
    open(join(static_path, key_file), "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode())


if __name__ == '__main__':
    create_self_signed_cert()
