#!/usr/bin/env python3

from os import listdir
from os.path import exists
import PySimpleGUI as sg
from .api import (delete_old_version, install_latest_update,
                  install_old_version, last_fifteen_versions,
                  list_installed_versions, see_directory_exists)
from .constants import (BUTTON_COLOR, DEFAULT_DIR, LAST_FIFTEEN,
                        LATEST_VERSION_TAG)

def main():
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
                    expand_x=True,
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
                [sg.Frame('Prerequisites & updates', col1, size=(325, 190), expand_x=True, expand_y=True), 
                    sg.Frame('Old versions', col2, size=(325, 190), expand_x=True, expand_y=True), 
                    sg.Frame('Removals', col3, size=(325, 190), expand_x=True, expand_y=True)],
                [sg.Column(col4, expand_x=True)],
                [sg.Column(col5)],
            ]

    # Create the window
    window = sg.Window("Glorious Proton Manager", layout, element_justification="c", finalize=True)
    while True:
        event, sg.values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "See if default Proton-GE directory exists":
            see_directory_exists()

        if event == "Update Proton-GE to latest version":
            if exists(DEFAULT_DIR):
                if LATEST_VERSION_TAG not in listdir(DEFAULT_DIR):
                    print("Installing latest Proton-GE version. It might take a while.")
                    window.refresh()
                    install_latest_update()
                    sg.popup(f"{LATEST_VERSION_TAG} successfully installed", font=('Any 9'), title="Glorious Proton Manager")
                else:
                    sg.popup("Latest version is already installed", font=('Any 9'), title="Glorious Proton Manager")
            else:
                sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")

        if event == "1. List currently installed versions":
            if exists(DEFAULT_DIR) == False:
                sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")
            elif len(listdir(DEFAULT_DIR)) == 0:
                print("No Proton-GE versions found on your system\n")
            else:
                list_installed_versions()
        if event == "1. List last 15 versions":
            last_fifteen_versions()
 
        if event == "3. Install past Proton-GE version":
            user_input_one = sg.values[0]
            new_dict = []
            for x in LAST_FIFTEEN:
                new_dict.append(x['tag_name'])
            if user_input_one == '':
                sg.popup("Field is empty. Give a version to install in step 2", font=('DejaVu 9'), title="Glorious Proton Manager")
            elif user_input_one not in str(new_dict):
                sg.popup(f"Invalid value. You can only install one of the versions listed", title="Glorious Proton Manager")
            elif user_input_one in str(listdir(DEFAULT_DIR)):
                sg.popup(f"This Proton-GE version is already installed", title="Glorious Proton Manager")
            else:
                print(f"Downloading and extracting Proton-GE {sg.values[0]}. It might take a while.\n")
                window.refresh()
                install_old_version()
                sg.popup(f"Proton-GE {sg.values[0]} successfully installed", font=('DejaVu 9'), title="Glorious Proton Manager")
 
        if event == "3. Delete Proton-GE version":
            user_input_two = sg.values[1]
            ge_del_version = "GE-Proton{0}".format(sg.values[1])
            if exists(DEFAULT_DIR):
                if ge_del_version in listdir(DEFAULT_DIR):
                    print(f"Deleting {ge_del_version}...\n")
                    delete_old_version()
                    sg.popup(f"Proton-GE {user_input_two} successfully deleted", font=('DejaVu 9'), title="Glorious Proton Manager")
                elif user_input_two == '':
                    sg.popup("Field is empty. Give a version to delete in step 2", font=('DejaVu 9'), title="Glorious Proton Manager")
                else:
                    sg.popup("This version is not installed on your system", font=('DejaVu 9'), title="Glorious Proton Manager")
            else:
                sg.popup("Default directory is not created. See the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager")

    window.close()
