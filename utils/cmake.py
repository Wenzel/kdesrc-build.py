import sys
import os
import logging
import subprocess
import shutil

def run(source, dest, install_prefix):
    binary = shutil.which('cmake')
    args = [source, '-DCMAKE_INSTALL_PREFIX={}'.format(install_prefix)]
    args.insert(0, binary)
    p = subprocess.Popen(args, executable=binary, cwd=dest)
    (stdout, stderr) = p.communicate()
    return p.returncode
