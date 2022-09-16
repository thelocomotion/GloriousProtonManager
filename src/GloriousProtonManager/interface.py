#!/usr/bin/env python3

from os import listdir
from os.path import exists
import PySimpleGUI as sg
from .functions import (
    delete_old_version,
    install_release,
    last_fifteen_versions,
    list_installed_versions,
    see_directory_exists,
)
from .constants import BUTTON_COLOR, DEFAULT_DIR, LATEST_VERSION_TAG, LATEST_VERSION_URL


def main():
    # Theme selection
    sg.theme("DarkBlue2")
    # Columns definition. Text in the buttons MUST match events when called
    col1 = [
        [
            sg.Button(
                "See if default Proton-GE directory exists",
                size=(47, 2),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
        [
            sg.Button(
                "Update Proton-GE to the latest version",
                size=(47, 6),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
    ]

    col2 = [
        [
            sg.Button(
                "1. List last 15 versions",
                size=(47, 3),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
        [
            sg.Text("2. Pick one (e.g., 7-15):", font=("DejaVu 9")),
            sg.InputText(size=[20, 20], font=("DejaVu 12")),
        ],
        [
            sg.Button(
                "3. Install past Proton-GE version",
                size=(47, 3),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
    ]

    col3 = [
        [
            sg.Button(
                "1. List currently installed versions",
                size=(47, 3),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
        [
            sg.Text("2. Pick one (e.g., 7-15):", font=("DejaVu 9")),
            sg.InputText(size=[20, 20], font=("DejaVu 12")),
        ],
        [
            sg.Button(
                "3. Delete Proton-GE version",
                size=(47, 3),
                font=("DejaVu 9"),
                button_color=BUTTON_COLOR,
            )
        ],
    ]

    col4 = [
        [
            sg.Multiline(
                size=(115, 18),
                expand_x=True,
                font="DejaVu 11",
                text_color="#171a21",
                background_color=BUTTON_COLOR,
                do_not_clear=False,
                reroute_stdout=True,
                reroute_stderr=True,
            )
        ]
    ]

    col5 = [[sg.Button("Exit", font=("DejaVu 11"), button_color=BUTTON_COLOR)]]

    layout = [
        [
            sg.Frame(
                "Prerequisites and updates",
                col1,
                size=(325, 190),
                expand_x=True,
                expand_y=True,
            ),
            sg.Frame(
                "Old versions", col2, size=(325, 190), expand_x=True, expand_y=True
            ),
            sg.Frame("Removals", col3, size=(325, 190), expand_x=True, expand_y=True),
        ],
        [sg.Column(col4, expand_x=True)],
        [sg.Column(col5)],
    ]

    # Create the window
    window = sg.Window(
        "Glorious Proton Manager", layout, element_justification="c", finalize=True
    )
    while True:
        event, sg.values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "See if default Proton-GE directory exists":
            see_directory_exists()

        if event == "Update Proton-GE to the latest version":
            if exists(DEFAULT_DIR):
                installed = list_installed_versions()
                if LATEST_VERSION_TAG not in installed:
                    print(
                        "Installing latest Proton-GE version. It might take a while..."
                    )
                    window.refresh()
                    install_release(LATEST_VERSION_URL)
                    sg.popup(
                        f"{LATEST_VERSION_TAG} successfully installed",
                        font=("Any 9"),
                        title="Glorious Proton Manager",
                    )
                else:
                    sg.popup(
                        "Latest version is already installed",
                        font=("Any 9"),
                        title="Glorious Proton Manager",
                    )
            else:
                sg.popup(
                    "Default directory is not created. See the prerequisites",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )

        if event == "1. List currently installed versions":
            if exists(DEFAULT_DIR) == False:
                sg.popup(
                    "Default directory is not created. See the prerequisites",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )
            elif len(listdir(DEFAULT_DIR)) == 0:
                print("No Proton-GE versions found on the system\n")
            else:
                version_found = list_installed_versions()
                print(
                    "These Proton-GE versions are currently installed on the system:\n"
                )
                for installed in version_found:
                    print(f"- {installed}")

        if event == "1. List last 15 versions":
            print("Versions available to install:\n")
            release = last_fifteen_versions()
            for version in release:
                print(f"- {version}")

        if event == "3. Install past Proton-GE version":
            install_old_input = sg.values[0]
            old_version = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{0}/GE-Proton{0}.tar.gz".format(
                sg.values[0]
            )
            release = last_fifteen_versions()
            if install_old_input == "":
                sg.popup(
                    "Field is empty. Give a version to install in step 2",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )
            elif install_old_input not in str(release):
                sg.popup(
                    f"Invalid value. You can only install one of the versions listed",
                    title="Glorious Proton Manager",
                )
            elif install_old_input in str(listdir(DEFAULT_DIR)):
                sg.popup(
                    f"This Proton-GE version is already installed",
                    title="Glorious Proton Manager",
                )
            elif install_old_input not in str(listdir(DEFAULT_DIR)) and (len(install_old_input) <= 5 ):
                print(
                    f"Downloading and extracting Proton-GE{sg.values[0]}. It might take a while.\n"
                )
                window.refresh()
                install_release(old_version)
                sg.popup(
                    f"Proton-GE{sg.values[0]} successfully installed",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )
            elif install_old_input not in str(listdir(DEFAULT_DIR)) and (len(install_old_input) > 5 ):
                sg.popup(
                    f"Invalid value. Only specify the version number, e.g., '7-20'",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )

        if event == "3. Delete Proton-GE version":
            delete_input = sg.values[1]
            ge_del_version = "GE-Proton{0}".format(sg.values[1])
            if exists(DEFAULT_DIR):
                installed = list_installed_versions()
                if ge_del_version in installed:
                    print(f"Deleting {ge_del_version}...\n")
                    delete_old_version()
                    sg.popup(
                        f"Proton-GE {delete_input} successfully deleted",
                        font=("DejaVu 9"),
                        title="Glorious Proton Manager",
                    )
                elif delete_input == "":
                    sg.popup(
                        "Field is empty. Give a version to delete in step 2",
                        font=("DejaVu 9"),
                        title="Glorious Proton Manager",
                    )
                else:
                    sg.popup(
                        "This version is not installed on the system",
                        font=("DejaVu 9"),
                        title="Glorious Proton Manager",
                    )
            else:
                sg.popup(
                    "Default directory is not created. See the prerequisites",
                    font=("DejaVu 9"),
                    title="Glorious Proton Manager",
                )

    window.close()
