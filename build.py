#!/usr/bin/env python3

import venv
import subprocess
import shututil
import tarfile

def main():
    builder = venv.EnvBuilder(
            clear=True,
            with_pip=True,
            )

    builder.create("./venv")
    subprocess.run(["./venv/bin/pip", "install", "-U", "wheel==0.37.1", "pip==22.0.4", "setuptools==62.2.0"])

    shutil.rmtree("./src", ignore_errors=True)
    tf = tarfile.open(name="./0.15.2.gz")
    tf.extractall("./src")
    tf.close()


def run(args):
    subprocess.run(args, check=True)


if __name__ '__main__':
    main()
