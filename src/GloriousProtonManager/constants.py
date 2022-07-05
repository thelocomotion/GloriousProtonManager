# Defining constant variables across the project

import os
import json
import requests

DEFAULT_DIR = os.path.expanduser('~/.steam/root/compatibilitytools.d/')
PROTON_GE_LATEST = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
PROTON_GE_RELEASES = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
R1 = requests.get(PROTON_GE_LATEST)
R2 = requests.get(PROTON_GE_RELEASES)
FILTER_LATEST = json.loads(r1.text)
FILTER_RELEASES = json.loads(r2.text)
LAST_VERSION_URL = FILTER_LATEST['assets'][1]['browser_download_url']
LAST_VERSION_TAG = FILTER_LATEST['tag_name']
LAST_FIFTEEN = FILTER_RELEASES[0:15]