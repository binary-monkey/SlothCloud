#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json


"""
Returns json file containing the files and directories subsequent to the path
passed as a parameter. Each folder has a list containing everything in of it.

:param path: optional, default=root/static
"""


def get_index(path=""):

    if not path:
        scheme = {
            "root": {
                "static": [

                ]
            }
        }

        # returns the path to the current file
        # multiple variables are just for better understanding
        root_path = os.path.dirname(os.path.abspath(__file__))
        static_path = root_path + "/static"
        path = static_path
    else:
        scheme = {}

    # returns a list containing a json-structured representation of subsequent
    # dirs and files
    def get_scheme(x):
        return [{y: get_scheme(x + "/" + y)} if os.path.isdir(x + "/" + y)
                else y for y in os.listdir(x)]

    scheme["root"]["static"] = get_scheme(path)
    # print(json.dumps(, indent=4, sort_keys=True))
    return json.dumps(scheme, ensure_ascii=False)


if __name__ == "__main__":
    print(print(json.dumps(json.loads(get_index(), encoding="utf-8"),
                           indent=4, sort_keys=True)))
