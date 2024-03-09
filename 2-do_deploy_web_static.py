#!/usr/bin/python3
"""
Module for web application deployment using Fabric
"""
from os.path import *
from fabric.api import *

env.hosts = ["100.25.199.90", "52.3.242.186"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """Distributes archives to the web servers
    Args:
    archive_path: the path to the static files"""
    if not exists(archive_path):
        return False

    fldpath = splitext(archive_path)[0]
    fldpath = fldpath.split('/')[-1]
    flname = fldpath + '.tgz'

    try:
        put(archive_path, "/tmp/")

        run(f'mkdir -p /data/web_static/releases/{fldpath}')
        run(f'tar -xzf /tmp/{flname} -C /data/web_static/releases/{fldpath}')
        run(f'rm /tmp/{flname}')
        run(f'mv /data/web_static/releases/{fldpath}/web_static/*'
            f' /data/web_static/releases/{fldpath}')
        run(f'rm -rf /data/web_static/releases/{fldpath}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -sf /data/web_static/releases/{fldpath}'
            f' /data/web_static/current')
        run("sudo service nginx restart")
        print("New version deployed!")
        return True

    except Exception:
        return False
