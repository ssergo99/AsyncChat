from setuptools import setup, find_packages

setup(
    name="asyncchatclient",
    version="1.0.1",
    description="chat_client",
    packages=find_packages(),
    author="Ssergo99",
    author_email="ssergo99.git@google.com",
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
)
