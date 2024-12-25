# -*- coding: utf-8 -*- noqa
"""
Created on Thu Nov  7 18:37:35 2024

@author: JoelT
"""
import sys

from .database import Database  # noqa
from .window_add_archive import WindowAddArchive  # noqa


if sys.version_info[0] < 3:
    raise RuntimeError("Python version lower than 3.")

if sys.version_info[1] < 12:
    raise RuntimeError("Python version lower than 3.12.")

if sys.version_info[2] < 5:
    raise RuntimeError("Python version lower than 3.12.5.")
