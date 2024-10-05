#!/usr/bin/python3
"""Fabric script which generates a tgz archive"""

from datetime import datetime
from fabric import task
from os.path import isdir
import os


@task
def do_pack(c):
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            os.mkdir("versions")  # Using os.mkdir() to create directories
        file_name = "versions/web_static_{}.tgz".format(date)
        c.local(f"tar -cvzf {file_name} web_static")  # Use the connection object `c`
        return file_name
    except Exception as e:
        print(f"Error: {e}")
        return None
