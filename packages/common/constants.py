# ../common/constants.py

"""Provides commonly used constants."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import os
from collections import OrderedDict
from platform import system
from warnings import warn

# Site-Package
from configobj import ConfigObj
from path import Path


# =============================================================================
# >> HELPER CLASSES
# =============================================================================
class Environ:
    def __getitem__(self, item):
        return os.environ[item].strip('"')


environ = Environ()


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
PLATFORM = system().lower()

# Store the binary names
_binary = "dll" if PLATFORM == "windows" else "so"
SOURCE_BINARY = f"source-python.{_binary}"
CORE_BINARY = f"core.{_binary}"

# Store the configuration values
START_DIR = Path(environ['STARTDIR'])
PLUGIN_BASE_PATH = Path(environ['PLUGIN_BASE_PATH'])
CONFIG_BASE_PATH = Path(environ['CONFIG_BASE_PATH'])
DATA_BASE_PATH = Path(environ['DATA_BASE_PATH'])
DOCS_BASE_PATH = Path(environ['DOCS_BASE_PATH'])
EVENTS_BASE_PATH = Path(environ['EVENTS_BASE_PATH'])
LOGS_BASE_PATH = Path(environ['LOGS_BASE_PATH'])
SOUND_BASE_PATH = Path(environ['SOUND_BASE_PATH'])
TRANSLATIONS_BASE_PATH = Path(environ['TRANSLATIONS_BASE_PATH'])
PLUGIN_PRIMARY_FILES_DIR = Path(environ['PLUGIN_PRIMARY_FILES_DIR'])
PLUGIN_ROOT_FILES_DIR = Path(environ['PLUGIN_ROOT_FILES_DIR'])
LINK_BASE_DIRECTORY = Path(environ['LINK_BASE_DIRECTORY'])
AUTHOR = environ["AUTHOR"]
RELEASE_DIR = Path(environ["RELEASE_DIRECTORY"])

_readable_data = [
    "ini",
    "json",
    "vdf",
    "xml",
]

# Store plugin specific directories with their respective allowed file types
ALLOWED_FILETYPES = {
    PLUGIN_BASE_PATH: [*_readable_data, "md", "py"],
    DATA_BASE_PATH: [*_readable_data, "md", "txt"],
    CONFIG_BASE_PATH: [*_readable_data, "cfg", "md", "txt"],
    LOGS_BASE_PATH: ["md", "txt"],
    SOUND_BASE_PATH: ["md", "mp3", "wav"],
    EVENTS_BASE_PATH: ["md", "txt"],
    TRANSLATIONS_BASE_PATH: ["md", "ini"],
    "materials/": ["vmt", "vtf"],
    "models/": ["mdl", "phy", "vtx", "vvd"],
}

# Store directories with files that fit allowed_filetypes
#   with names that should not be included
EXCEPTION_FILETYPES = {
    TRANSLATIONS_BASE_PATH: ["_server.ini"],
}

SEMANTIC_VERSIONING_COUNT = 3

# Get a list of all plugins
PLUGIN_LIST = [
    x.stem for x in START_DIR.dirs()
    if not x.stem.startswith((".", "_"))
]
