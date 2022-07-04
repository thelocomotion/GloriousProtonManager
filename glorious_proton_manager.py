#!/usr/bin/env python

import os
import sys
import PySimpleGUI as sg
import json
import requests
import shutil
import tarfile

user_home = os.environ['HOME']
proton_ge_latest = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
proton_ge_releases = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
proton_dir = f"{user_home}/.steam/root/compatibilitytools.d/"
r1 = requests.get(proton_ge_latest)
r2 = requests.get(proton_ge_releases)
filter_latest = json.loads(r1.text)
filter_releases = json.loads(r2.text)
last_version_url = filter_latest['assets'][1]['browser_download_url']
last_version_tag = filter_latest['tag_name']
last_fifteen = filter_releases[0:15]

def check_directory_exists():
    if os.path.exists(proton_dir) == True:
        sg.popup("GE-Proton directory already created", font=('Any 9'), title="Glorious Proton Manager (GPM)")
    else:
        print("Creating default GE-Proton directory...\n")
        os.mkdir(proton_dir)
        print(f"\n{proton_dir} successfully created\n")

def install_latest_update():
    print("Installing latest version of GE-Proton. This might take a minute or two...")
    response = requests.get(last_version_url, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=proton_dir)
    os.scandir()

def last_fifteen_releases():
    print("Versions available for installation:\n")
    for x in last_fifteen:
        print(f"- {x['tag_name']}")

def install_old_release():
    old_release = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(values[0])
    print(f"Downloading and extracting GE-Proton {values[0]}. This might take a minute or two...\n")
    response = requests.get(old_release, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=proton_dir)
    print("Installation complete\n")

def list_installed_versions():
    print("Currently these GE-Proton versions are installed in your system:\n")
    installed_versions = os.listdir(proton_dir)
    for x in sorted(installed_versions, reverse=True):
        print(f"- {x}")

def delete_old_release():
    ge_del_version = "GE-Proton{0}".format(values[1])
    print(f"Deleting {ge_del_version}...\n")
    shutil.rmtree(proton_dir + ge_del_version)
    os.scandir()

sg.theme('DarkBlue2')

col1 =  [ 
        [sg.Button("Check if Default GE-Proton Directory Exists", size=(100, 200), font=('Any 9'))]
        ]

col2 =  [ 
        [sg.Button("Update GE-Proton to Latest Version", size=(100, 200), font=('Any 9'))]
        ]

col3 =  [ 
        [sg.Button("1. List Previous Releases (Last 15)", size=(47, 4), font=('Any 9'))],
        [sg.Text("2. Select One (e.g 7-15):", font=('Any 9')), sg.InputText(size=[20, 20], font=('Any 12'))],
        [sg.Button("3. Install Previous Release of GE-Proton", size=(47, 4), font=('Any 9'))]
        ]

col4 =  [
        [sg.Button("1. List Currently Installed Versions", size=(47, 4), font=('Any 9'))],
        [sg.Text("2. Select One (e.g 7-15):", font=('Any 9')), sg.InputText(size=[20, 20], font=('Any 12'))],
        [sg.Button("3. Delete GE-Proton Version", size=(47, 4), font=('Any 9'))]
        ]

col5 =  [
        [sg.Multiline(size=(165,18),
              font='Any 11',
              do_not_clear=False,
              reroute_stdout=True, 
              reroute_stderr=True,
              autoscroll = True)]
        ]

col6 =  [
        [sg.Button("Exit", font=('Any 11'))]
        ]

layout = [  
            [   
                sg.Frame("Prerequisites", col1, size=(325, 230)), 
                sg.Frame("Updates", col2, size=(325, 230)), 
                sg.Frame("Old Releases", col3, size=(325, 230)), 
                sg.Frame("Removals", col4, size=(325, 230))
            ],
                [sg.Column(col5)],
                [sg.Column(col6)],
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
        installed_versions = os.listdir(proton_dir)
        if last_version_tag in installed_versions:
            sg.popup("Latest version is already installed", font=('Any 9'), title="Glorious Proton Manager (GPM)")
        else:
            install_latest_update()
            sg.popup(f"{last_version_tag} successfully installed", font=('Any 9'), title="Glorious Proton Manager (GPM)")
    if event == "1. List Currently Installed Versions":
        installed_versions = os.listdir(proton_dir)
        if len(installed_versions) == 0:
            print("No GE-Proton versions are installed on your system\n")
        else:
            list_installed_versions()
    if event == "1. List Previous Releases (Last 15)":
        last_fifteen_releases()
    if event == "3. Install Previous Release of GE-Proton":
        installed_versions = os.listdir(proton_dir)
        user_input_one = values[0]
        new_dict = []
        for x in last_fifteen:
            new_dict.append(x['tag_name'])
        if user_input_one == '':
            sg.popup("Field is empty", font=('Any 9'), title="Glorious Proton Manager (GPM)")
        elif user_input_one not in str(new_dict):
            sg.popup(f"Invalid value", title="Glorious Proton Manager (GPM)")
        elif user_input_one in str(installed_versions):
            sg.popup(f"This version of GE-Proton is already installed", title="Glorious Proton Manager (GPM)")
        else:
            install_old_release()
            sg.popup(f"GE-Proton{values[0]} successfully installed", font=('Any 9'), title="Glorious Proton Manager (GPM)")
    if event == "3. Delete GE-Proton Version":
        user_input_two = values[1]
        if user_input_two == '':
            sg.popup("Field is empty", font=('Any 9'), title="Glorious Proton Manager (GPM)")
        elif user_input_two not in str(installed_versions):
            sg.popup("This version is not installed on your system", font=('Any 9'), title="Glorious Proton Manager (GPM)")
        else:
            delete_old_release()
            sg.popup(f"GE-Proton{user_input_two} successfully deleted", font=('Any 9'), title="Glorious Proton Manager (GPM)")

window.close()
