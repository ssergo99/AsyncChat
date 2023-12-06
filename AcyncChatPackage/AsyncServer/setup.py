import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {"packages" : ["log", "messageutils"]
           }

setup(
        name = "async_server",
        version = "1.1",
        description = "Message Chat Server",
        options = {"build_exe" : options},
        executables = [Executable("server_side.py", base = base)])