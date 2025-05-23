# ../plugin_checker.py

"""Checks plugins for standards issues."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from os import system

# Package
from common.constants import PLUGIN_BASE_PATH, START_DIR, PLUGIN_LIST
from common.functions import clear_screen, get_plugin


# =============================================================================
# >> MAIN FUNCTION
# =============================================================================
def check_plugin(plugin_name):
    """Check the given plugin for standards issues."""
    # Was an invalid plugin name given?
    if plugin_name not in PLUGIN_LIST:
        print(f'Invalid plugin name "{plugin_name}"')
        return

    # Get the plugin's path
    plugin_path = START_DIR.joinpath(
        plugin_name,
        PLUGIN_BASE_PATH,
        plugin_name,
    )

    system(f"ruff check {plugin_path}")


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == "__main__":

    # Get the plugin to check
    _plugin_name = get_plugin("check")
    if _plugin_name is not None:

        clear_screen()
        if _plugin_name == "ALL":
            for _plugin_name in PLUGIN_LIST:
                print(f'Checking plugin "{_plugin_name}"')
                check_plugin(_plugin_name)

        else:
            check_plugin(_plugin_name)
