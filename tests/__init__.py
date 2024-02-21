#!/usr/bin/python3
"""Package module for the test_console.py file"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clearfilecontents(file_stream: TextIO):
    """Clears file stream contents"""
    if file_stream.seekable():
        file_stream.seek(0)
        file_stream.truncate(0)


def removefile(path: str):
    """Deletes a file if it exists"""
    if os.path.isfile(path):
        os.unlink(path)


def resetstorage(data_store: FileStorage, path='file.json'):
    """Resets the items in a data store"""
    with open(path, mode='w') as fl:
        fl.write('{}')
        data_store.reload() if data_store else None


def readfilecontents(filename):
    """Reads the file contents"""
    file_content = []
    if os.path.isfile(filename):
        with open(filename, mode='r') as fl:
            for file_content in fl.readlines():
                file_content.append(file_content)
    return ''.join(file_content)


def writetofile(filename, content):
    """Writes content into a file"""
    with open(filename, mode='w') as fl:
        fl.write(content)
