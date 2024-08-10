import os

def is_root():
    return os.geteuid() == 0
def check_root():
    if is_root():
        print("The script is running as root.")
    else:
        print("The script is not running as root.")
