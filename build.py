#!/usr/bin/env python3

import datetime
import os
import venv
import subprocess
import shutil
import tarfile

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

    os.chdir(f"/src/pyzstd-{VERSION}")


    d = datetime.now()

    subprocess.run([python, "./setup.py", "bdist_wheel", "-dynamic-link-zstd", "--build-number", d.isoformat(timespec='minutes')], check=True, env={'SOURCE_DATE_EPOCH': "315532800", "CFLAGS": "-g0 -march=x86-64-v3 -O3"})


if __name__ == '__main__':
    main()
