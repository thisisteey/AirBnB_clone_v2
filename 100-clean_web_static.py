#!/usr/bin/python3
"""
Module for web application deployment using Fabric
"""
import os
from datetime import datetime
from fabric.api import local, runs_once, env, put, run

env.hosts = ["54.237.100.185", "18.206.208.19"]


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


def do_deploy(archive_path):
    """Distributes archives to the web servers
    Args:
    archive_path: the path to the static files"""
    if not os.path.exists(archive_path):
        return False
    flname = os.path.basename(archive_path)
    fldname = flname.replace(".tgz", "")
    fldpath = f"/data/web_static/releases/{fldname}/"
    output = False
    try:
        put(archive_path, f"/tmp/{flname}")
        run(f"mkdir -p {fldpath}")
        run(f"tar -xzf /tmp/{flname} -C {fldpath}")
        run(f"rm -rf /tmp/{flname}")
        run(f"mv {fldpath}web_static/* {fldpath}")
        run(f"rm -rf {fldpath}web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {fldpath} /data/web_static/current")
        print('New version deployed!')
        output = True
    except Exception as e:
        output = False
    return output


def deploy():
    """Creates and distributes archives to the web servers"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """Deletes out-of-date archives
    Args:
    number (int): the number of archives to keep"""
    archfld = 'versions/'
    archlst = os.listdir(archives_folder)
    arclst.sort(reverse=True)
    startidx = int(number)
    if not startidx:
        startidx += 1
    if startidx < len(archlst):
        archdel = archlst[startidx:]
    else:
        archdel = []
    for arch in archdel:
        archpth = os.path.join(archfld, arch)
        os.unlink(archpth)
    cmdpts = [
            "rm -rf $(",
            "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
            " '/data/web_static/releases/web_static_.*'",
            f" | sort -r | tr '\\n' ' ' | cut -d ' ' -f{start_index + 1}-)"
    ]
    run(''.join(cmpts))
