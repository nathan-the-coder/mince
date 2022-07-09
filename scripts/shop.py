import os 
import shutil
import time
from colorama import Fore

def cd(path):
    """Change directory to path"""
    os.chdir(path)
    print(path)

def mkdir(path):
    """Make a directory"""
    os.mkdir(path)
    print(os.getcwd())

def cp(src, dest):
    """Copy source to destination"""
    shutil.copy(src, dest)
    print(Fore.GREEN + "[COPY]" + Fore.WHITE + ": " + dest)

def install(mode, src, dest):
    os.system("clear")
    time.sleep(1)
    if os.path.isdir(src):
        os.system(f"install -d {src} {dest}")
    else:
        os.system(f"install -Dm{mode} {src} {dest}")

    print(Fore.GREEN + "[INSTALL]: \n"
                     + Fore.CYAN 
                     + "  [MODE]: "
                     + Fore.WHITE
                     + str(mode) + "\n"
                     + Fore.LIGHTMAGENTA_EX
                     + "   [SRC]: "
                     + Fore.WHITE
                     + src + "\n"
                     + Fore.BLUE
                     + "  [DEST]: "
                     + Fore.WHITE
                     + dest + "\n")
    time.sleep(1)
    print(Fore.GREEN + "[SUCCESS]: " + Fore.WHITE + "Sucessfully Installed")

def rem(path):
    if os.path.isdir(path):
        os.removedirs(path)
    else:
        os.remove(path)
