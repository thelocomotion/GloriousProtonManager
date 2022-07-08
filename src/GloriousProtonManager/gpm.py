#!/usr/bin/env python3

import os
import PySimpleGUI as sg
import requests
import shutil
import tarfile
from settings import *

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
            window.refresh()
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
    In the Old Releases section the user will pass an input in step 2, which will be stored in values[0]
    This variable will be formatted into another one called old_version, defining the old version to install 
    Refreshing the window before the request is needed to prevent the application from looking stuck during the process
    '''
    old_version = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(values[0])
    print(f"Downloading and extracting Proton-GE {values[0]}. It might take a while.\n")
    window.refresh()
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
    '''
    First it checks that the default directory exists. It it does, the input passed by the user in the Removals section
    will be stored in the variable values[1]. This variable will be used for two things: knowing if an input was passed
    at all and also knowing which version to delete. If the version is present in the default directory then it will be
    deleted and a popup message will show. If the user left the field empty a popup will show telling the user to select
    a version to delete. If a wrong value was typed a popup will say that version is not installed.
    If the directory doesn't exists the user will be prompted to check the prerequisites
    '''
    if os.path.exists(DEFAULT_DIR):
        user_input_two = values[1]
        ge_del_version = "GE-Proton{0}".format(values[1])
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

# Theme selection
sg.theme('DarkBlue2')

# Columns definition. Text in the buttons MUST match events when called
col1 =  [ 
            [sg.Button('See if default Proton-GE directory exists', size=(47, 2), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Button('Update Proton-GE to latest version', size=(47, 6), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col2 =  [ 
            [sg.Button('1. List last 15 versions', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Text('2. Pick one (e.g. 7-15):', font=('DejaVu 9')), sg.InputText(size=[20, 20], font=('DejaVu 12'))],
            [sg.Button('3. Install past Proton-GE version', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col3 =  [
            [sg.Button('1. List currently installed versions', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Text('2. Pick one (e.g. 7-15):', font=('DejaVu 9')), sg.InputText(size=[20, 20], font=('DejaVu 12'))],
            [sg.Button('3. Delete Proton-GE version', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col4 =  [
            [sg.Multiline(size=(115, 18),
                font='DejaVu 11',
                text_color='#171a21',
                background_color = BUTTON_COLOR,
                do_not_clear=False,
                reroute_stdout=True, 
                reroute_stderr=True)]
        ]

col5 =  [
            [sg.Button('Exit', font=('DejaVu 11'), button_color=BUTTON_COLOR)]
        ]

layout = [     
            [sg.Frame('Prerequisites & updates', col1, size=(325, 190)), sg.Frame('Old versions', col2, size=(325, 190)), sg.Frame('Removals', col3, size=(325, 190))],
            [sg.Column(col4)],
            [sg.Column(col5)],
         ]

# Create the window
window = sg.Window("Glorious Proton Manager", layout, element_justification="c", finalize=True)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "See if default Proton-GE directory exists":
        see_directory_exists()
    if event == "Update Proton-GE to latest version":
        install_latest_update()
    if event == "1. List currently installed versions":
        if os.path.exists(DEFAULT_DIR) == False:
            sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")
        elif len(os.listdir(DEFAULT_DIR)) == 0:
            print("No Proton-GE versions found on your system\n")
        else:
            list_installed_versions()
    if event == "1. List last 15 versions":
        last_fifteen_versions()
    if event == "3. Install past Proton-GE version":
        user_input_one = values[0]
        new_dict = []
        for x in LAST_FIFTEEN:
            new_dict.append(x['tag_name'])
        if user_input_one == '':
            sg.popup("Field is empty. Give a version to install in step 2", font=('DejaVu 9'), title="Glorious Proton Manager")
        elif user_input_one not in str(new_dict):
            sg.popup(f"Invalid value. You can only install one of the versions listed", title="Glorious Proton Manager")
        elif user_input_one in str(os.listdir(DEFAULT_DIR)):
            sg.popup(f"This Proton-GE version is already installed", title="Glorious Proton Manager")
        else:
            install_old_version()
            sg.popup(f"Proton-GE{values[0]} successfully installed", font=('DejaVu 9'), title="Glorious Proton Manager")
    if event == "3. Delete Proton-GE version":
        delete_old_version()

window.close()
