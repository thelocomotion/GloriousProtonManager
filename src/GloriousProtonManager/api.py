import os
import shutil
import tarfile
import PySimpleGUI as sg
import requests
from .constants import DEFAULT_DIR, LAST_FIFTEEN, LATEST_VERSION_TAG, LATEST_VERSION_URL

def see_directory_exists():
    '''
    Checks path to see if the directory exists. In the case it does, a popup shows.
    If it doesn't, it will be created and a message printed to screen

    '''
    if os.path.exists(DEFAULT_DIR):
        sg.popup("Proton-GE directory already created", font=('DejaVu 9'), title="Glorious Proton Manager")
    else:
        print("Creating default Proton-GE directory...\n")
        os.makedirs(DEFAULT_DIR, exist_ok=True)
        print(f"{DEFAULT_DIR} successfully created\n")

def install_latest_update():
    '''
    First it checks that the default directory exists. If it does, the latest version available will be downloaded, extracted in place
    and a popup window will show. If the latest version is already present in the directory, a popup window will show saying so.
    In the case the default directory doesn't exist, a popup will ask the user to check the prerequisites
    
    '''
    if os.path.exists(DEFAULT_DIR):
        if LATEST_VERSION_TAG not in os.listdir(DEFAULT_DIR):
            print("Installing latest Proton-GE version. It might take a while.")
            # Refreshing breaks the app - to investigate
            # sg.window.refresh()
            response = requests.get(LATEST_VERSION_URL, stream=True)
            file = tarfile.open(fileobj=response.raw, mode="r|gz")
            file.extractall(path=DEFAULT_DIR)
            sg.popup(f"{LATEST_VERSION_TAG} successfully installed", font=('Any 9'), title="Glorious Proton Manager")
        else:
            sg.popup("Latest version is already installed", font=('Any 9'), title="Glorious Proton Manager")
    else:
        sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")

def last_fifteen_versions():
    '''
    Prints last 15 versions available
    '''
    print("Versions available to install:\n")
    for x in LAST_FIFTEEN:
        print(f"- {x['tag_name']}")

def install_old_version():
    '''
    In the Old Releases section the user will pass an input in step 2, which will be stored in sg.values[0]
    This variable will be formatted into another one called old_version, defining the old version to install 
    Refreshing the window before the request is needed to prevent the application from looking stuck during the process
    '''
    old_version = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(sg.values[0])
    print(f"Downloading and extracting Proton-GE {sg.values[0]}. It might take a while.\n")
    # Refreshing breaks the app - to investigate   
    # sg.window.refresh()
    response = requests.get(old_version, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)
    print("Installation done\n")

def list_installed_versions():
    '''
    Checks installed versions in default directory and sorts them out in reverse
    '''
    print("These Proton-GE versions are currently installed on your system:\n")
    for x in sorted(os.listdir(DEFAULT_DIR), reverse=True):
        print(f"- {x}")

def delete_old_version():
    if os.path.exists(DEFAULT_DIR):
        user_input_two = sg.values[1]
        ge_del_version = "GE-Proton{0}".format(sg.values[1])
        if ge_del_version in os.listdir(DEFAULT_DIR):
            print(f"Deleting {ge_del_version}...\n")
            shutil.rmtree(DEFAULT_DIR + ge_del_version)
            sg.popup(f"Proton-GE{user_input_two} successfully deleted", font=('DejaVu 9'), title="Glorious Proton Manager")
        elif user_input_two == '':
            sg.popup("Field is empty. Give a version to delete in step 2", font=('DejaVu 9'), title="Glorious Proton Manager")
        else:
            sg.popup("This version is not installed on your system", font=('DejaVu 9'), title="Glorious Proton Manager")
    else:
        sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")
