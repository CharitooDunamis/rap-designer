from __future__ import absolute_import
from os import getcwd
from os.path import dirname


if getcwd().endswith("gui_"):
    GUI_DIR = getcwd()
else:
    GUI_DIR = dirname(__file__)
