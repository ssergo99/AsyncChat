import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
options = {"packages" : ["log", "messageutils", "sqlalchemy"]
           }
setup(
        name = "async_client",
        version = "1.1",
        description = "Message Chat Client",
        options = {"build_exe" : options},
        executables = [Executable("client_side.py",
                                  base = base)])