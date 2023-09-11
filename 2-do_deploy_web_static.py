#!/usr/bin/python3
# fabric script for compress and deployment

from datetime import datetime
from fabric.api import local, env, put, run
import os

env.hosts = ["34.232.69.68", "35.174.176.142"]
env.user = "ubuntu"


def do_pack():
    """creats a tgz archive from web_static content"""
    d = datetime.now().strftime("%Y%m%d%H%M%S")
    f_name = f"versions/web_static_{d}.tgz"

    if not os.path.isdir("versions"):
        local("mkdir -p versions")
    try:
        local(f"tar -cvzf {f_name} web_static")
        return f_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute archive to web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        fi = archive_path.split("/")[-1]
        no_extention = fi.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_extention))
        run('tar -xzf /tmp/{} -C {}{}/'.format(fi, path, no_extention))
        run('rm /tmp/{}'.format(fi))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_extention))
        run('rm -rf {}{}/web_static'.format(path, no_extention))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_extention))
        return True
    except Exception:
        return False
