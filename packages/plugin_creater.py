# ../plugin_creater.py

"""Creates a plugin with its base directories and files."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Package
from common.constants import (
    AUTHOR,
    CONFIG_BASE_PATH,
    DATA_BASE_PATH,
    DOCS_BASE_PATH,
    EVENTS_BASE_PATH,
    LOGS_BASE_PATH,
    PLUGIN_BASE_PATH,
    PLUGIN_PRIMARY_FILES_DIR,
    PLUGIN_ROOT_FILES_DIR,
    SOUND_BASE_PATH,
    START_DIR,
    TRANSLATIONS_BASE_PATH,
    PLUGIN_LIST,
)
from common.functions import clear_screen

# Site-package
from jinja2 import Template

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_boolean_values = {
    "1": True,
    "y": True,
    "yes": True,
    "2": False,
    "n": False,
    "no": False,
}

_directory_or_file = {
    "1": "file",
    "2": "directory",
    "3": None,
}


# =============================================================================
# >> MAIN FUNCTION
# =============================================================================
def create_plugin(plugin_name, **options):
    """Verify the plugin name and create its base directories/files."""
    # Was no plugin name provided?
    if plugin_name is None:
        print("No plugin name provided.")
        return

    # Is the given plugin name valid?
    if not plugin_name.replace("_", "").isalnum():
        print("Invalid plugin name.")
        print(
            "Plugin name must only contain alpha-numeric values and "
            "underscores.",
        )
        return

    # Get the path to create the plugin at
    plugin_base_path = START_DIR / plugin_name

    # Has the plugin already been created?
    if plugin_base_path.is_dir():
        print("Plugin already exists.")
        return

    # Get the plugin's directory
    plugin_path = plugin_base_path.joinpath(
        PLUGIN_BASE_PATH,
        plugin_name,
    )

    # Create the plugin's directory
    plugin_path.makedirs()

    # Copy repo primary files
    for file in PLUGIN_PRIMARY_FILES_DIR.files():
        file.copy(
            plugin_path / file.name,
        )
        with file.open() as open_file:
            file_contents = Template(open_file.read())

        file_contents = file_contents.render(
            plugin_name=plugin_name,
            author=AUTHOR,
        )
        if not file_contents.endswith('\n'):
            file_contents += '\n'
        new_file = plugin_path / file.name
        with new_file.open("w") as open_file:
            open_file.write(file_contents)

    for option, path in (
        ("config", CONFIG_BASE_PATH),
        ("data", DATA_BASE_PATH),
        ("docs", DOCS_BASE_PATH),
        ("events", EVENTS_BASE_PATH),
        ("logs", LOGS_BASE_PATH),
        ("sound", SOUND_BASE_PATH),
        ("translations", TRANSLATIONS_BASE_PATH),
    ):
        value = options[option] or False
        if value is False:
            continue

        elif value == "file":
            _create_directory(
                plugin_base_path,
                path,
                filename=f"{plugin_name}.ini",
            )

        else:
            _create_directory(
                plugin_base_path,
                path,
                plugin_name,
                filename="readme.md",
            )

    # Copy repo base files
    for file in PLUGIN_ROOT_FILES_DIR.files():
        file.copy(
            plugin_base_path / file.name,
        )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _create_directory(base_path, *args, filename):
    """Create the directory using the given arguments."""
    current_path = base_path.joinpath(*args)
    current_path.makedirs()
    current_path.joinpath(filename).touch()


def _get_plugin_name():
    """Return a new plugin name."""
    clear_screen()

    name = input(
        "What is the name of the plugin that should be created?\n\n"
    )

    # Is the plugin name invalid?
    if not name.replace("_", "").isalnum():
        return _ask_retry(
            f'Invalid characters used in plugin name "{name}".\n'
            f'Only alpha-numeric and underscores allowed.',
        )

    # Does the plugin already exist?
    if name in PLUGIN_LIST:
        return _ask_retry(f'Plugin name "{name}" already exists.')

    return name


def _ask_retry(reason):
    """Ask if another plugin name should be given."""
    clear_screen()

    value = input(
        f"{reason}\n\nDo you want to try again?\n\n\t(1) Yes\n\t(2) No\n\n",
    ).lower()

    # Was the retry value invalid?
    if value not in _boolean_values:
        return _ask_retry(reason)

    # Yes?
    if _boolean_values[value]:
        return _get_plugin_name()

    return None


def _get_directory(name):
    """Return whether to create the given directory."""
    clear_screen()
    value = input(
        f"Do you want to include a {name} directory?\n\n"
        f"\t(1) Yes\n\t(2) No\n\n",
    ).lower()

    # Was the given value invalid?
    if value not in _boolean_values:
        return _get_directory(name)

    return _boolean_values[value]


def _get_directory_or_file(name):
    """Return whether to create the given directory or file."""
    clear_screen()
    value = input(
        f"Do you want to include a {name} file, directory, or neither?\n\n"
        f"\t(1) File\n\t(2) Directory\n\t(3) Neither\n\n",
    )

    # Was the given value invalid?
    if value not in _directory_or_file:
        _get_directory_or_file(name)

    return _directory_or_file[value]


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == "__main__":

    _plugin_name = _get_plugin_name()

    # Was a valid plugin name given?
    if _plugin_name is not None:
        _config = _get_directory("config")
        _data = _get_directory_or_file("data")
        _docs = _get_directory("docs")
        _events = _get_directory("events")
        _logs = _get_directory("logs")
        _sound = _get_directory("sound")
        _translations = _get_directory_or_file("translations")
        create_plugin(
            plugin_name=_plugin_name,
            config=_config,
            data=_data,
            docs=_docs,
            events=_events,
            logs=_logs,
            sound=_sound,
            translations=_translations,
        )
