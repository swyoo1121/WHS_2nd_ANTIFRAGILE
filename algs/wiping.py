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

target_subpath = r'..\..\C-CPP\104.cpp' 

def detect_wiped(file_path):
    with open(file_path, "rb") as file:
        # 파일의 헤더 부분 바이트 읽어오기
        header = file.read(16)

        # 파일의 푸터 부분 바이트 읽어오기
        file.seek(-16, 2)  # 파일 끝에서 16바이트 앞부분으로 이동, whence 2 = 끝에서 부터 커서 이동
        footer = file.read(16)


        return 

def get_file_dir():
    for current_dir in listdir(CURRENT_DIR):
        current_path = join(CURRENT_DIR, current_dir)
        root_path = get_root_path(current_path)
        target_path = get_target_path(current_path, target_subpath)     

        print(current_path)
        print(root_path)
        print(target_path)
        
        if check_file_exists(target_path):
            print("The file or directory exists.")
        else:
            print("The file or directory does not exist.")
        
def get_root_path(path):
    drive, _ = os.path.splitdrive(path)
    return drive if drive else '/'

def get_target_path(current_file_path, target_subpath):
    # Get the directory of the current file
    current_dir = os.path.dirname(current_file_path)
    
    # Construct the full path to the target
    target_path = os.path.join(current_dir, target_subpath)
    
    # Resolve the absolute path
    absolute_target_path = os.path.abspath(target_path)
    
    return absolute_target_path
    
def check_file_exists(absolute_path):
    return os.path.exists(absolute_path)

def main():
    get_file_dir()  
    
main()

