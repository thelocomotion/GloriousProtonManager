# Glorious Proton Manager
**Glorious Proton Manager (GPM)** is a tool that allows Linux users to delete and install old and new [Proton-GE][proton-ge-url] versions as they come out. Giving a GUI for this felt needed, as the number of Linux gamers is growing thanks to Valve, Wine and other open source projects.

[proton-ge-url]: https://github.com/GloriousEggroll/proton-ge-custom
![GPM screenshot](.github/images/GPM.png)
## Dependencies
GPM needs python3-tkinter (Fedora)/python3-tk (Ubuntu or openSUSE Leap). You can install it with the command:
### Fedora
```
sudo dnf install python3-tkinter
```
### Ubuntu
```
sudo apt install python3-tk
```
### openSUSE Leap
```
sudo zypper in python3-tk
```
## Installation
### From source
You can clone the repository with the command:
```
git clone https://github.com/thelocomotion/GloriousProtonManager.git
```
You can enter the directory once the repository is cloned and run:
```
pip3 install -r requirements.txt
```
It will install the needed Python modules to run GPM.
### Using pip
```
pip3 install GloriousProtonManager
```
Locate gpm.py and run:
```
chmod +x gpm.py
./gpm.py
```
## Usage
To run GPM, type:
```bash
./gpm.py
```
## Features
GPM is split into 3 different columns: **Prerequisites and updates**, **Old versions** and **Removals**.
### Prerequisites
This button sees if the default directory **(~/.steam/root/compatibilitytools.d)** where Proton-GE versions should be installed exists. It will be created if it does not.
### Updates
This button sees if the latest Proton-GE version is installed on your system. A message saying so will be shown if it is. Otherwise it will be installed.
### Old versions
This column is divided into 3 different steps, which the user should follow in order. First list the versions, then pick one from the list by typing its version and lastly click the Install button. I decided to show only the last 15 versions, as older versions felt pointless. It will say so with a popup warning message if the field is left empty or an invalid value is given.
### Removals
Another 3 step column. Works the same way as the other menu. It sees which versions are installed and allows you to delete them once the version value is given as input. It will also show a popup warning message if the field is left empty or an invalid value is given.
## Known bugs
- Making the GUI look identical on distinct platforms and distros is hard with PySimpleGUI. It will look fine on Fedora, but may look a bit off on distros like Ubuntu or OpenSUSE.
