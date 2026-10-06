#!/usr/bin/env python3
"""01_hello.py — your first Python script.

Run it with:  python 01_hello.py
"""
import platform
import sys

name = "Scripting 101"
print(f"Hello, {name}!")
print(f"Python version : {platform.python_version()}")
print(f"Interpreter    : {sys.executable}")   # tells you WHICH python ran (conda env or system?)
