#!/usr/bin/env python3

from pprint import pprint
import json
from urllib.parse import urlparse
from pathlib import Path
import sys
import os
import shlex
import subprocess

def main():
    newtag = os.environ["NEW_TAG"]

    cmd = f"gh release  view {newtag} --jq '.assets[].url' --json assets"
    try:
        output = subprocess.run(shlex.split(cmd), capture_output=True, check=True, text=True).stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        sys.exit(1)

    index = ""
    index += "<html>\n"
    for o in output:
        index += f"<a href='{o}'>{o}</a>\n"
    index += "</html>\n"


    Path("./public").mkdir(exist_ok=True)
    Path("./public/index.html").write_text(index)

if __name__ == '__main__':
    main()
