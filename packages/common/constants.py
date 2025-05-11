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
PLUGIN_BASE_PATH = environ['PLUGIN_BASE_PATH']

# Store the premade files location
PREMADE_FILES_DIR = START_DIR / ".plugin_helpers" / "files"

# Store the author value
AUTHOR = environ["AUTHOR"]

# Store the Source.Python repository directory
SOURCE_PYTHON_DIR = Path(environ["SOURCE_PYTHON_DIRECTORY"].strip('"'))

# Get Source.Python's addons directory
SOURCE_PYTHON_ADDONS_DIR = SOURCE_PYTHON_DIR / "addons" / "source-python"

# Get Source.Python's build directory
SOURCE_PYTHON_BUILDS_DIR = SOURCE_PYTHON_DIR.joinpath(
    "src",
    "Builds",
    "Windows" if PLATFORM == "windows" else "Linux",
)

# Get the directories to link
source_python_directories = {
    x.stem for x in SOURCE_PYTHON_DIR.dirs()
    if x.stem not in ("addons", "src", ".git")
}

# Get the addons directories to link
source_python_addons_directories = {
    x.stem for x in SOURCE_PYTHON_DIR.joinpath(
        "addons",
        "source-python",
    ).dirs() if x.stem != "bin"
}

_support = ConfigObj(START_DIR / ".plugin_helpers" / "tools" / "support.ini")

supported_games = OrderedDict()

_check_files = ["srcds.exe", "srcds_run", "srcds_linux"]

for _directory in environ["SERVER_DIRECTORIES"].split(";"):
    _path = Path(_directory)
    for _check_directory in _path.dirs():
        if not any(
            _check_directory.joinpath(_check_file).is_file()
            for _check_file in _check_files
        ):
            continue
        for _game in _support["servers"]:
            _game_dir = _check_directory / _support["servers"][_game]["folder"]
            if not _game_dir.is_dir():
                continue
            if _game in supported_games:
                warn(
                    f"{_game} already assigned to {supported_games[_game]}.  "
                    f"New path found: {_game_dir}",
                )
                continue
            supported_games[_game] = {
                "directory": _game_dir,
                "branch": _support["servers"][_game]["branch"],
            }

for _directory in environ["STEAM_DIRECTORIES"].split(";"):
    _path = Path(_directory) / "SteamApps"
    for _game_type in ("common", "sourcemods"):
        for _game in _support[_game_type]:
            if "game" in _support[_game_type][_game]:
                _game_dir = _path.joinpath(
                    _game_type, _support[_game_type][_game]["game"],
                    _support[_game_type][_game]["folder"],
                )
            else:
                _game_dir = _path.joinpath(
                    _game_type, _game, _support[_game_type][_game]["folder"])
            if not _game_dir.is_dir():
                continue
            if _game in supported_games:
                warn(
                    f"{_game} already assigned to {supported_games[_game]}.  "
                    f"New path found: {_game_dir}",
                )
                continue
            supported_games[_game] = {
                "directory": _game_dir,
                "branch": _support[_game_type][_game]["branch"],
            }

# Store the Release directory
RELEASE_DIR = Path(environ["RELEASE_DIRECTORY"])

# Get a list of all plugins
plugin_list = [
    x.stem for x in START_DIR.dirs()
    if not x.stem.startswith((".", "_"))
]
