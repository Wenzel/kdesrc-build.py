# kdesrc-build.py

An attempt to rewrite the `kdesrc-build` script into Python.

# Requirements

- `Python` `>=` `3.4`
- `virtualenv`

# Setup

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

# Usage

    """
    Usage:
        kdesrc-build.py [options] <project>...

    options:
        -h --help           Show this screen.
        --version           Show version.
    """

Exemple:

    ./kdesrc-build.py extra-cmake-modules

# Done

- [x] get, build and install a simple project
- [x] handle project group (components, modules, ...)

# TODO

- [ ] add `-p`, `--pretend` option
- [ ] handle a configuration file
- [ ] handle a project build dependencies
- [ ] add nice user output
- [ ] add good logging capabilities
