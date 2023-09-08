#!/usr/bin/python3
# fabric script that is generating tgz archive

from datetime import datetime
from fabric.api import local
import os.path


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
