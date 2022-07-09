import os
import log
import shop
import time

def clone(src, dest):
    try:
        log.Log(1, "Cloning...")
        if os.system(f"git clone -q {src} {dest}") != 0:
            _in = input("You I remove the directory? ")
            if _in == "yes":
                log.Log(2, "Removing directory!")
                time.sleep(3)
                shop.shutil.rmtree(dest)
                log.Log(1, "Cloning...")
                os.system(f"git clone -q {src} {dest}")
            elif _in == "no":
                log.Log(3, "Cannot Proceed: Directory Exists")
                exit(1)
            else:
                log.Log(3, "Please answer 'yes' or 'no'.")
                exit(1)
    except FileExistsError:
        log.Log(3, "Folder Exists") 
    finally:
        print("\n")
        log.Log(1, "Successfully Cloned")
