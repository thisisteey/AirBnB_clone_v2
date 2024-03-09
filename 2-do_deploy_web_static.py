#!/usr/bin/python3
"""
Module for web application deployment using Fabric
"""
from os.path import exists, basename
from datetime import datetime
from fabric.api import *

env.hosts = ["100.25.199.90", "52.3.242.186"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


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


@task(default=True)
def do_deploy(archive_path):
    """Distributes archives to the web servers
    Args:
    archive_path: the path to the static files"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        flname = basename(archive_path)
        flnamext = flname.split(".")[0]
        fldpath = f"/data/web_static/releases/{flnamext}/"
        sudo(f"mkdir -p {fldpath}")
        sudo(f"tar -xzf /tmp/{flname} -C {fldpath}")
        sudo(f"rsync -a {fldpath}web_static/* {fldpath}")
        sudo(f"rm -rf {fldpath}web_static")
        sudo(f"rm -rf /tmp/{flname}")
        sudo(f"rm -rf /data/web_static/current")
        sudo(f"ln -sf {fldpath} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
