from setuptools import setup

APP = ['server_side.py']
DATA_FILES = ["srvmeta.py", "deco_func.py",
              "descservsock.py", "db.py",
              "serv_admin.py", "srv_config.ini"]
OPTIONS = {"packages" : ["log", "messageutils",
                         "sqlalchemy"]
           }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)