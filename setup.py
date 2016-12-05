#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Carlos, Mikel, Rafa: Create desktop icon for linux. (and maybe Windows)

from app.config.constants import app_path
from gen_ssl import create_self_signed_cert
from os import name
from setuptools import setup
from subprocess import Popen, PIPE

setup(name="SlothCloud", version="0.1",
      description="RESTful access media server made using Python 3 and Flask",
      author="Ninia",
      author_email="ninia@protonmail.com",
      url="https://github.com/Ninia/SlothCloud",
      install_requires=["flask", "Flask-AutoIndex", "pyopenssl"])

if name == "posix":
    print("[*] Generating alias for slcl...")

    try:
        with open("~/.bashrc", 'a') as bashrc:
            bashrc.write("alias slcl='%s/run.py'" % app_path)
        print("[*] Done.")
    except FileNotFoundError:
        print("[*] Error. Couldn't create alias")

    print("[*] updating terminal...")
    out, err = Popen("source ~/.bashrc", shell=True,
                     stdout=PIPE, stderr=PIPE).communicate()
    if err:
        print(err)
    else:
        print("[*] Done.")

create_self_signed_cert()
