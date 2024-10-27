#!/usr/bin/python3
""" Module for compressing content"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Creating .tgz archive from the contents of the web static folder"""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    #generating timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{timestamp}.tgz"

    print(f"Packing web_static to {archive_name}")

    #use the local command to create the .tgz archive

    command = f"tar -cvzf {archive_name} web_static"
    result = local(command)

    # check if the archive was successfully created
    if result.succeded:
        print(f"web_static packed: {archive_name}")
        return archive_name
    else:
        print("Failed to create the archive.")
        return None