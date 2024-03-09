import toml


def read_version():
    with open("pyproject.toml") as f:
        mt = toml.load(f)
        return mt["tool"]["poetry"]["version"]


version = read_version()