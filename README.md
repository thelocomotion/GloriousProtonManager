Introduction
------------
**Glorious Proton Manager (GPM)** is a tool which allows Linux users to install old and new releases of [GE-Proton][ge-proton-url] as they come out, as well as deleting them. Providing a UI for something like this felt needed as the number of new users gaming on Linux is growing thanks to Valve, WINE and other Open Source projects.

[ge-proton-url]: https://github.com/GloriousEggroll/proton-ge-custom

Installation
------------

## From Source
You can clone the repository with this command:
```bash
git clone https://github.com/thelocomotion/GloriousProtonManager.git
```

Once the repository is cloned, you can enter the directory and run:
```bash
pip3 install -r requirements.txt
```
This should install the Python modules that are needed to run the application.

## Using pip
```
pip3 install GloriousProtonManager
```

Dependencies
------------
GPM requires **Python 3.10** to run as PySimpleGUI has some bugs in v3.9.

Usage
-----
To run the application simply type:
```bash
./gpm.py
```

What can you do with this tool
------------------------------
GPM is divided into 3 different columns: **Prerequisites and Updates**, **Old Releases** and **Removals**.

## Prerequisites
This button checks whether the default directory **(~/.steam/root/compatibilitytools.d)** where GE-Proton releases should be installed to exist. If it doesn't, the directory will be created.

## Updates
This button checks whether the last version of GE-Proton is installed on your system or not. If it is, a message will be displayed saying so. Otherwise it'll be installed.

## Old Releases
This column is divided into 3 different steps, which the user should ideally follow in order. First list the releases, then select one from the list by typing its version and lastly press the Install button. I decided to only show the last 15 releases as anything older than that felt irrelevant. If the field is left empty or an invalid value is provided the application will say so with a popup warning message.

## Removals
Another 3 step column. Works the same way as the other menu. The application checks to see which releases are installed and allows you to delete them once the version value is provided as input. If the field is left empty or an invalid value is provided the application will also show a popup warning message.
