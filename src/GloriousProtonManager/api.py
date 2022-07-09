from os import listdir, makedirs
from os.path import exists
from shutil import rmtree
from tarfile import open
import PySimpleGUI as sg
from requests import get
from .constants import DEFAULT_DIR, LAST_FIFTEEN, LATEST_VERSION_URL

def see_directory_exists():
    '''
    Check if GE-Proton default directory exists or not

    '''
    if exists(DEFAULT_DIR):
        sg.popup("Proton-GE directory already created", font=('DejaVu 9'), title="Glorious Proton Manager")
    else:
        print("Creating default Proton-GE directory...\n")
        makedirs(DEFAULT_DIR, exist_ok=True)
        print(f"{DEFAULT_DIR} successfully created\n")

def install_latest_update():
    '''
    Install the latest version of GE-Proton that is available
    
    '''
    response = get(LATEST_VERSION_URL, stream=True)
    file = open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)

def last_fifteen_versions():
    '''
    Print last 15 versions
    '''
    print("Versions available to install:\n")
    for x in LAST_FIFTEEN:
        print(f"- {x['tag_name']}")

def install_old_version():
    '''
    Installs an old release of GE-Proton
    '''
    old_version = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(sg.values[0])
    response = get(old_version, stream=True)
    file = open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)

def list_installed_versions():
    '''
    Check installed versions in default directory and sort them out in reverse
    '''
    print("These Proton-GE versions are currently installed on your system:\n")
    for x in sorted(listdir(DEFAULT_DIR), reverse=True):
        print(f"- {x}")

def delete_old_version():
    '''
    Delete old version
    '''
    ge_del_version = "GE-Proton{0}".format(sg.values[1])
    rmtree(DEFAULT_DIR + ge_del_version)
