# Defining constant variables across the project

from json import loads
from os.path import expanduser
from requests import get

DEFAULT_DIR = expanduser('~/.steam/root/compatibilitytools.d/')
PROTON_GE_LATEST = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
PROTON_GE_RELEASES = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
BUTTON_COLOR = "#c7d5e0"
R1 = get(PROTON_GE_LATEST)
R2 = get(PROTON_GE_RELEASES)
FILTER_LATEST = loads(R1.text)
FILTER_VERSIONS = loads(R2.text)
LATEST_VERSION_URL = FILTER_LATEST['assets'][1]['browser_download_url']
LATEST_VERSION_TAG = FILTER_LATEST['tag_name']
LAST_FIFTEEN = FILTER_VERSIONS[0:15]
