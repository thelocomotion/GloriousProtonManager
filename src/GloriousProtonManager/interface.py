#!/usr/bin/env python3

import os
import PySimpleGUI as sg
from .constants import DEFAULT_DIR, BUTTON_COLOR, LAST_FIFTEEN
from .api import see_directory_exists, install_latest_update, last_fifteen_versions, install_old_version, delete_old_version, list_installed_versions

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
                [sg.Frame('Prerequisites & updates', col1, size=(325, 190), expand_x=True, expand_y=True), sg.Frame('Old versions', col2, size=(325, 190), expand_x=True, expand_y=True), sg.Frame('Removals', col3, size=(325, 190), expand_x=True, expand_y=True)],
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
            user_input_one = sg.values[0]
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
                sg.popup(f"Proton-GE{sg.values[0]} successfully installed", font=('DejaVu 9'), title="Glorious Proton Manager")
        if event == "3. Delete Proton-GE version":
            delete_old_version()
    window.close()
