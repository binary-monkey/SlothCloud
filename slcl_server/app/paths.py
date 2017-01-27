#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .config import constants
from .utils import *

"""
Path shortcut functions
"""

def static(path=""):
    return nt(constants.static_path + "/" + path)

def media(path=""):
    return nt(constants.media_path + "/" + path)

def app(path=""):
    return nt(constants.app_path + "/" + path)
