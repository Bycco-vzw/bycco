import toml
from pathlib import Path


def read_version():
    with open("pyproject.toml") as f:
        mt = toml.load(f)
        return mt["tool"]["poetry"]["version"]


version = read_version()

ROOT_DIR = (Path(".") / "..").resolve()
