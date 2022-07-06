#!/usr/bin/env python3

import json
import os
import PySimpleGUI as sg
import requests
import shutil
import tarfile
from constants import DEFAULT_DIR, PROTON_GE_LATEST, PROTON_GE_RELEASES
from constants import BUTTON_COLOR

r1 = requests.get(PROTON_GE_LATEST)
r2 = requests.get(PROTON_GE_RELEASES)
filter_latest = json.loads(r1.text)
filter_releases = json.loads(r2.text)
last_version_url = filter_latest['assets'][1]['browser_download_url']
last_version_tag = filter_latest['tag_name']
last_fifteen = filter_releases[0:15]

def check_directory_exists():
    if os.path.exists(DEFAULT_DIR):
        sg.popup("GE-Proton directory already created", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
    else:
        print("Creating default GE-Proton directory...\n")
        os.makedirs(DEFAULT_DIR, exist_ok=True)
        print(f"{DEFAULT_DIR} successfully created\n")

def install_latest_update():
    if os.path.exists(DEFAULT_DIR):
        if last_version_tag not in os.listdir(DEFAULT_DIR):
            print("Installing latest version of GE-Proton. This might take a minute or two...")
            response = requests.get(last_version_url, stream=True)
            file = tarfile.open(fileobj=response.raw, mode="r|gz")
            file.extractall(path=DEFAULT_DIR)
            os.scandir()
            sg.popup(f"{last_version_tag} successfully installed", font=('Any 9'), title="Glorious Proton Manager (GPM)")
        else:
            sg.popup("Latest version is already installed", font=('Any 9'), title="Glorious Proton Manager (GPM)")
    else:
        sg.popup("Default directory doesn't exist. Check the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")

def last_fifteen_releases():
    print("Versions available for installation:\n")
    for x in last_fifteen:
        print(f"- {x['tag_name']}")

def install_old_release():
    old_release = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(values[0])
    print(f"Downloading and extracting GE-Proton {values[0]}. This might take a minute or two...\n")
    response = requests.get(old_release, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)
    print("Installation complete\n")

def list_installed_versions():
    print("Currently these GE-Proton versions are installed on your system:\n")
    for x in sorted(os.listdir(DEFAULT_DIR), reverse=True):
        print(f"- {x}")

def delete_old_release(): 
    if os.path.exists(DEFAULT_DIR):
        user_input_two = values[1]
        ge_del_version = "GE-Proton{0}".format(values[1])
        if ge_del_version in os.listdir(DEFAULT_DIR):
            print(f"Deleting {ge_del_version}...\n")
            shutil.rmtree(DEFAULT_DIR + ge_del_version)
            sg.popup(f"GE-Proton{user_input_two} successfully deleted", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
            os.scandir()
        elif user_input_two == '':
            sg.popup("Field is empty. Provide a version to delete in step 2", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
        else:
            sg.popup("This version is not installed on your system", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
    else:
        sg.popup("Default directory doesn't exist. Check the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")

sg.theme('DarkBlue2')

col1 =  [ 
            [sg.Button('Check if Default GE-Proton Directory Exists', size=(47, 2), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Button('Update GE-Proton to Latest Version', size=(47, 6), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col2 =  [ 
            [sg.Button('1. List Previous Releases (Last 15)', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Text('2. Select One (e.g 7-15):', font=('DejaVu 9')), sg.InputText(size=[20, 20], font=('DejaVu 12'))],
            [sg.Button('3. Install Previous Release of GE-Proton', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col3 =  [
            [sg.Button('1. List Currently Installed Versions', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)],
            [sg.Text('2. Select One (e.g 7-15):', font=('DejaVu 9')), sg.InputText(size=[20, 20], font=('DejaVu 12'))],
            [sg.Button('3. Delete GE-Proton Version', size=(47, 3), font=('DejaVu 9'), button_color=BUTTON_COLOR)]
        ]

col4 =  [
            [sg.Multiline(size=(120,18),
                font='DejaVu 11',
                text_color='#171a21',
                background_color = BUTTON_COLOR,
                do_not_clear=False,
                reroute_stdout=True, 
                reroute_stderr=True,
                autoscroll = True)]
        ]

col5 =  [
            [sg.Button('Exit', font=('DejaVu 11'), button_color=BUTTON_COLOR)]
        ]

layout = [     
            [sg.Frame('Prerequisites & Updates', col1, size=(325, 200)), sg.Frame('Old Releases', col2, size=(325, 200)), sg.Frame('Removals', col3, size=(325, 200))],
            [sg.Column(col4)],
            [sg.Column(col5)],
         ]

# Create the Window
window = sg.Window("Glorious Proton Manager (GPM)", layout, element_justification="c", finalize=True)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Check if Default GE-Proton Directory Exists":
        check_directory_exists()
    if event == "Update GE-Proton to Latest Version":
        install_latest_update()
    if event == "1. List Currently Installed Versions":
        if os.path.exists(DEFAULT_DIR) == False:
            sg.popup("Default directory doesn't exist. Check the prerequisites", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
        elif len(os.listdir(DEFAULT_DIR)) == 0:
            print("No GE-Proton versions found on your system\n")
        else:
            list_installed_versions()
    if event == "1. List Previous Releases (Last 15)":
        last_fifteen_releases()
    if event == "3. Install Previous Release of GE-Proton":
        user_input_one = values[0]
        new_dict = []
        for x in last_fifteen:
            new_dict.append(x['tag_name'])
        if user_input_one == '':
            sg.popup("Field is empty. Provide a version to install in step 2", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
        elif user_input_one not in str(new_dict):
            sg.popup(f"Invalid value. You can only install one of the versions listed", title="Glorious Proton Manager (GPM)")
        elif user_input_one in str(os.listdir(DEFAULT_DIR)):
            sg.popup(f"This version of GE-Proton is already installed", title="Glorious Proton Manager (GPM)")
        else:
            install_old_release()
            sg.popup(f"GE-Proton{values[0]} successfully installed", font=('DejaVu 9'), title="Glorious Proton Manager (GPM)")
    if event == "3. Delete GE-Proton Version":
        delete_old_release()

window.close()
