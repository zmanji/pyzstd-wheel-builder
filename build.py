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

    e = os.environ.copy()
    e['SOURCE_DATE_EPOCH'] = "315532800"
    e["CFLAGS"] = "-g0 -march=x86-64-v3 -O3"

    subprocess.run([python, "./setup.py", "build_ext", "--dynamic-link-zstd"], check=True, env=e)

    dlibs = list(Path(".").glob("build/**/*.so"))
    for l in dlibs:
        subprocess.run(["patchelf", "--remove-rpath", str(l)], check=True, env=e)

    # Always set a build number to be higher version than pypi
    subprocess.run([python, "./setup.py", "bdist_wheel", "--dynamic-link-zstd", "--build-number", "1"], check=True, env=e)

    os.chdir(old)


    out = Path("./out")
    out.mkdir(exist_ok=True)

    shutil.copytree(srcdir + "/dist", "./out" ,dirs_exist_ok=True)

    shutil.rmtree("./src", ignore_errors=True)
    shutil.rmtree("./venv", ignore_errors=True)


if __name__ == '__main__':
    main()
