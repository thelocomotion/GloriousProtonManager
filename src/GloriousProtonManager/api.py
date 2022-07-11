from os import listdir, makedirs
from os.path import exists
from shutil import rmtree
from tarfile import open
import PySimpleGUI as sg
from requests import get
from .constants import DEFAULT_DIR, LAST_FIFTEEN, LATEST_VERSION_URL

def see_directory_exists():
    '''
    Sees if Proton-GE default directory exists

    '''
    if exists(DEFAULT_DIR):
        sg.popup("Proton-GE directory already created", font=('DejaVu 9'), title="Glorious Proton Manager")
    else:
        print("Creating default Proton-GE directory...\n")
        makedirs(DEFAULT_DIR, exist_ok=True)
        print(f"{DEFAULT_DIR} successfully created\n")

def install_latest_update():
    '''
    Installs Proton-GE's latest available version
    
    '''
    response = get(LATEST_VERSION_URL, stream=True)
    file = open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)

def last_fifteen_versions():
    '''
    Prints last 15 versions
    '''
    print("Versions available to install:\n")
    for release in LAST_FIFTEEN:
        print(f"- {release['tag_name']}")

def install_old_version():
    '''
    Installs an old Proton-GE version
    '''
    old_version = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(sg.values[0])
    response = get(old_version, stream=True)
    file = open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)

def list_installed_versions():
    '''
    Sees installed versions in default directory & sorts them out in reverse
    '''
    print("These Proton-GE versions are currently installed on your system:\n")
    for version_found in sorted(listdir(DEFAULT_DIR), reverse=True):
        print(f"- {version_found}")

def delete_old_version():
    '''
    Deletes old version
    '''
    ge_del_version = "GE-Proton{0}".format(sg.values[1])
    rmtree(DEFAULT_DIR + ge_del_version)
