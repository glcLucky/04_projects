# -*- coding: utf-8 -*-

from . config import _DEPENDENCIES

for pkg in _DEPENDENCIES:
    try:
        __import__(pkg)
    except Exception:
        print("WARNING: Fail to import {}!".format(pkg))
        raise ImportError


from . import (
    api,
    config,
    factor,
    load,
    miscellaneous,
    read,
    write,
    schema,
    utils,
)
