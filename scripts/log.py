import sys 
from colorama import Fore

herr = "Cannot run in level higher than '3'"

class Log:
    def __init__(self, lvl, msg):
        if lvl > 3:
            print(Fore.RED + "[ERROR]: " + Fore.WHITE + herr)
            exit(1)
        elif lvl == 3:
            print(Fore.RED + "[ERROR]: " + Fore.WHITE + msg)
            exit(1)
        elif lvl == 2:
            print(Fore.YELLOW + "[WARNING]: " + Fore.WHITE + msg)
        elif lvl == 1:
            print(Fore.GREEN + "[PRINT]: " + Fore.WHITE + msg)
        elif msg == "Hello":
            lvl = 1

