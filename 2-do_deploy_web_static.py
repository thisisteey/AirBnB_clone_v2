#!/usr/bin/python3
"""
Module for web application deployment using Fabric
"""
from os.path import exists
from fabric.api import *

env.hosts = ["100.25.199.90", "52.3.242.186"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """Distributes archives to the web servers
    Args:
    archive_path: the path to the static files"""
    try:
        if not exists(archive_path):
            print("File does not exist")
            return False
        archflname = archive_path.split("/")[-1].split('.')[0]
        put(archive_path, "/tmp/")
        fldpath = f"/data/web_static/releases/{archflname}"
        tmppath = f"/tmp/{archflname}"

        run(f"mkdir -p {fldpath}")
        run(f"tar -xvzf {tmppath}.tgz -C {fldpath}")
        run(f"rm {tmppath}.tgz")
        run(f"mv {fldpath}/web_static/* {fldpath}")
        run(f"rm -rf {fldpath}")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -sf {fldpath} /data/web_static/current")
        run("sudo service nginx restart")
        print("New version deployed!")
        return True
    except Exception as err:
        print(f"Error: {err}")
        return False
