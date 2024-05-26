# 와이핑 툴 Eraser 하나로 제한 (Wiping tool : Eraser)

import os
import psutil

from os import listdir, getcwd, remove
from os.path import isfile, join, realpath
from pickle import load, dump
from typing import Final

# CONFIG (CONSTANT VALUES)
CURRENT_DIR: Final = getcwd()
SELF_DESTRUCT: Final = False
CURRENT_SCRIPT: Final = realpath(__file__)
DISPLAY_MESSAGE: Final = True

for current_dir in listdir(CURRENT_DIR):
    current_path = join(CURRENT_DIR, current_dir)
    
    print(current_path)
    

