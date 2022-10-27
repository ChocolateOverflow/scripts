#!/usr/bin/python3
"""Handles some commands on text executables
Given some arguments, this script filters out non-executables as well as file
whose MIME types are not text. It then runs one of the defined commands on
the remaining text executables.

Usage: symlink `handle_txt_exec` (shell aliases won't work) and add the name
of that symlink to `cmd2app`, telling `handle_txt_exec` what command to run
for that symlink. Each member value of `cmd2app` can be either a single string
or a list of arguments.
"""

import os
import sys
import subprocess
from shutil import which
from typing import Union
from colorama import Fore, Style


# config command -> application
cmd2app = {
    "cx": ["bat", "--style", "header,grid,numbers"],
    "ex": os.environ["EDITOR"],
}


def print_error(msg: str) -> None:
    """Prints an error message"""
    print(Fore.RED + f"[!] {msg}" + Style.RESET_ALL, file=sys.stderr)


def get_abs_path(file: str) -> Union[str, None]:
    """Gets the real abosulte path (resolving symlinks) of the given file"""
    path = which(file)
    if path is None:
        return None
    return os.path.realpath(path)


def get_mime_type(file: str) -> str:
    """Get the MIME type of the given file"""
    # TODO: get a library to do this instead of using the system command
    return subprocess.check_output([b"file", b"-ib", file.encode()]).decode().split("/")[0]


def main(cmd, args):
    # filter for executables & get abs path
    tmp = []
    for arg in args:
        abs_path = get_abs_path(arg)
        if abs_path is None:
            print_error(f"{arg} does not exist as an executable")
        else:
            tmp.append(abs_path)
    args = list(set(tmp))

    # filter for "text" MIME type
    for arg in list(args):
        if get_mime_type(arg) != "text":
            print_error(f"{arg} is not a text file")
            args.remove(arg)

    if cmd == "handle_txt_exec.py":
        # simply print the filtered files line by line
        for arg in args:
            print(arg)
    elif cmd in cmd2app:
        if len(args) == 0:
            print_error("No file passed")
            sys.exit()
        cmd_arr = cmd2app[cmd] if isinstance(cmd2app[cmd], list) else [cmd2app[cmd]]
        cmd_arr.extend(args)
        subprocess.call(cmd_arr)
    else:
        print_error(f"Unrecognized command: {cmd}")


if __name__ == "__main__":
    main(os.path.basename(__file__), sys.argv[1:])
