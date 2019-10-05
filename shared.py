from urllib.request import urlopen, urlretrieve
from traceback import print_exc
import json
import sys
import platform
import tarfile
import zipfile
import os
import os.path
import time
import datetime
import argparse
import shutil
import ntpath
import subprocess

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def download_with_progress(url, target, block_size=2 ** 19):
    if os.path.exists(target):
        print("File already exists. Skipping.")
        return
    try:
        u = urlopen(url)
        with open(target, 'wb') as f:
            file_size_downloaded = 0
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break
                file_size_downloaded += len(buffer)
                f.write(buffer)

                mb = file_size_downloaded / 1000000
                print(f"Downloaded {mb:.2f}MB")
    except Exception:
        print_exc()
        print("Failed to download files")
        input()
        sys.exit(1)

def unzip(path: str, name: str):
    # assume file format here
    if os.path.exists(name):
        print("Unzip Already Exists. Skipping.")
        return
    print(f"Unzipping {path}")
    with zipfile.ZipFile(path, "r") as zf:
        zf.extractall(name)
    print("Done unzipping.")

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:xz") as tar:
        tar.add(source_dir)