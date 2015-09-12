import sys
import os
import logging
import subprocess
import shutil

def install(build_dir):
    binary = shutil.which('make')
    args = ['install']
    args.insert(0, binary)
    p = subprocess.Popen(args, executable=binary, cwd=build_dir)
    (stdout, stderr) = p.communicate()
    return p.returncode

