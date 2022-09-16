from os import listdir, makedirs
from os.path import exists
from shutil import rmtree
from tarfile import open
import PySimpleGUI as sg
from requests import get
from .constants import DEFAULT_DIR, LAST_FIFTEEN


def see_directory_exists() -> None:
    """
    Sees if Proton-GE default directory exists

    """
    if exists(DEFAULT_DIR):
        sg.popup(
            "Proton-GE directory already created",
            font=("DejaVu 9"),
            title="Glorious Proton Manager",
        )
    else:
        print("Creating default Proton-GE directory...\n")
        makedirs(DEFAULT_DIR, exist_ok=True)
        print(f"{DEFAULT_DIR} successfully created\n")


def install_release(download_url) -> None:
    """
    Installs a Proton-GE release
    """
    response = get(download_url, stream=True)
    file = open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=DEFAULT_DIR)


def last_fifteen_versions() -> list:
    """
    Prints last 15 versions
    """
    list_available = []
    for version in LAST_FIFTEEN:
        list_available.append(version["tag_name"])
    return list_available


def list_installed_versions() -> list:
    """
    Sees installed versions in default directory and sorts them in reverse
    """
    list_installed = []
    for version_found in sorted(listdir(DEFAULT_DIR), reverse=True):
        list_installed.append(version_found)
    return list_installed


def delete_old_version() -> None:
    """
    Deletes old version
    """
    ge_del_version = "GE-Proton{0}".format(sg.values[1])
    rmtree(DEFAULT_DIR + ge_del_version)
