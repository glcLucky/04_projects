# -*- coding: utf-8 -*-

try:
    from termcolor import colored
except Exception:
    colored = lambda msg, clr: msg

try:
    from WindPy import w as WDServer
except Exception:
    raise ImportError("Please check WindPy path!")

from . utils import options2str, test_error
from . api import *


def login(is_quiet=False):
    if not WDServer.isconnected():
        login = WDServer.start()
        if not is_quiet:
            print(colored("WDServer is connected successfully!", "green"))
    else:
        if not is_quiet:
            print(colored("WDServer is already connected!", "green"))


def logout():
    if WDServer.isconnected():
        logout = WDServer.stop()
        print(colored("WDServer is disconnected successfully!", "green"))
    else:
        print(colored("WDServer is already disconnected!", "green"))


def test():
    response = WDServer.wss("000001.SZ", "industry_sw", "industryType=1")
    if response.ErrorCode == 0:
        print(colored("WDServer is running.", "green"))
    else:
        login()
