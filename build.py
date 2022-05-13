#!/usr/bin/env python3

from datetime import datetime
import os
import venv
import subprocess
import shutil
import tarfile
from pathlib import Path

VERSION = "0.15.2"

def main():
    builder = venv.EnvBuilder(
            clear=True,
            with_pip=True,
            )

    builder.create("./venv")
    subprocess.run(["./venv/bin/pip", "install", "-U", "wheel==0.37.1", "pip==22.0.4", "setuptools==62.2.0"], check=True)

    shutil.rmtree("./src", ignore_errors=True)
    tf = tarfile.open(name=f"./{VERSION}.tar.gz")
    tf.extractall("./src")
    tf.close()

    python = os.path.abspath("./venv/bin/python3")

    old = os.getcwd()

    srcdir = f"./src/pyzstd-{VERSION}"

    os.chdir(srcdir)


    d = datetime.now()
    d = d.isoformat(timespec='minutes')
    d = d.replace('-', '_')
    d = d.replace(':', '_')

    e = os.environ.copy()
    e['SOURCE_DATE_EPOCH'] = "315532800"
    e["CFLAGS"] = "-g0 -march=x86-64-v3 -O3"

    subprocess.run([python, "./setup.py", "bdist_wheel", "--dynamic-link-zstd", "--build-number", d], check=True, env=e)

    os.chdir(old)


    out = Path("./out")
    out.mkdir(exist_ok=True)

    shutil.copytree(srcdir + "/dist", "./out" ,dirs_exist_ok=True)


if __name__ == '__main__':
    main()
