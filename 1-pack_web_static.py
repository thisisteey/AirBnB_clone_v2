#!/usr/bin/python3
"""
Module for web application deployment using Fabric
"""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Creates an archive of the static files"""
    if not os.path.exists("versions"):
        os.mkdir("versions")
    currdt = datetime.utcnow()
    result = f"versions/web_static_{currdt.strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        print(f"Packing web_static to {result}")
        local(f"tar -cvzf {result} web_static")
        file_size = os.path.getsize(result)
        print(f"web_static packed: {result} -> {file_size} Bytes")
    except Exception as e:
        print(f"Error: {e}")
        result = None
    return result
