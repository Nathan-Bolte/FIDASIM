#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prefida_py import colored


def info(string):
    """
    ;+#info
    ;+Print a informational message
    ;+***
    ;+##Arguments
    ;+     **str**: message
    ;+
    ;+##Example Usage
    ;+```idl
    ;+IDL> info, "This is an informative message"
    ;+```
    """
    print colored('INFO: ' + string, c='b')
