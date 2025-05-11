# ../plugin_releaser.py

"""Creates a release for a plugin with its current version number."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from os import sep
from zipfile import ZIP_DEFLATED, ZipFile

# Package
from common.constants import (
    ALLOWED_FILETYPES,
    EXCEPTION_FILETYPES,
    PLUGIN_BASE_PATH,
    RELEASE_DIR,
    SEMANTIC_VERSIONING_COUNT,
    START_DIR,
)
from common.functions import clear_screen, get_plugin

# Site-package
from configobj import ConfigObj
from git import Repo
from git.exc import InvalidGitRepositoryError


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_version_updates = {
    1: "MAJOR",
    2: "MINOR",
    3: "PATCH",
    4: None,
}


# =============================================================================
# >> CLASSES
# =============================================================================
class PluginReleaser:
    plugin_repo = None
    info_file = None
    info = None
    version = None
    check_version = None
    update_type = None
    zip_path = None

    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        self.plugin_repo_path = START_DIR / self.plugin_name

    def validate_diff(self):
        """Validate that the plugin does not have uncommitted changes."""
        try:
            self.plugin_repo = Repo(START_DIR / self.plugin_name)
        except InvalidGitRepositoryError:
            print(f'Plugin "{self.plugin_name}" is not a git repository.')
            return False

        if (
                bool(self.plugin_repo.index.diff('HEAD')) or
                bool(self.plugin_repo.index.diff(None)) or
                bool(self.plugin_repo.untracked_files)
        ):
            print(f'Plugin "{self.plugin_name}" has uncommitted changes.')
            return False

        return True

    def validate_version_exists(self):
        """Find if we need to update the version."""
        self.info_file = self.plugin_repo_path.joinpath(
            PLUGIN_BASE_PATH,
            self.plugin_name,
            "info.ini",
        )
        if not self.info_file.is_file():
            print("No info.ini file found")
            return False

        self.info = ConfigObj(self.info_file)
        self.version = self.info.get("version")
        if self.version is None:
            print('"version" not found in info.ini')
            return False

        try:
            self.check_version = [int(x) for x in self.version.split(".")]
        except ValueError:
            print(f'Invalid "version" in info.ini: "{self.version}"')
            return False

        if len(self.check_version) != SEMANTIC_VERSIONING_COUNT:
            print(f'Invalid "version" in info.ini: "{self.version}"')
            return False

        return True

    def find_new_version(self):
        self.update_type = self.get_version_update_type()
        if self.update_type <= SEMANTIC_VERSIONING_COUNT:
            self.check_version[self.update_type - 1] += 1
            self.check_version[self.update_type:] = [0] * (3 - self.update_type)
            return True
        return False

    def get_version_update_type(self, previous=None):
        """Retrieve input on which part of the version should be updated."""
        clear_screen()
        message = ""
        if previous is not None:
            message += f'Invalid value given "{previous}"\n\n'

        message += "Which type of version update should this be?\n\n"
        for number, choice in sorted(_version_updates.items()):
            message += f"\t({number}) {choice}\n"

        value = input(message + "\n").strip()
        if not value.isdigit():
            return self.get_version_update_type(value)

        value = int(value)
        if value not in _version_updates:
            return self.get_version_update_type(value)

        return value

    def commit_update(self):
        self.version = self.info["version"] = ".".join(
            map(str, self.check_version)
        )
        self.info.write()
        self.plugin_repo.index.add([
            self.info_file.filename.replace(self.plugin_repo_path, "")[1:]
        ])
        self.plugin_repo.index.commit(
            f"{_version_updates[self.update_type]} version"
            f" update ({self.version})"
        )
        self.plugin_repo.remotes.origin.push()

    def create_release(self):
        """Verify the plugin name and create the current release."""
        # Get the directory to save the release in
        save_path = RELEASE_DIR / self.plugin_name

        # Create the directory if it doesn't exist
        if not save_path.is_dir():
            save_path.makedirs()

        # Get the zip file location
        self.zip_path = save_path / f"{self.plugin_name} - v{self.version}.zip"

        # Does the release already exist?
        if self.zip_path.is_file():
            print("Release already exists for current version.")
            return

        repo_files = self.plugin_repo.git.ls_files().splitlines()

        # Create the zip file
        with ZipFile(self.zip_path, "w", ZIP_DEFLATED) as zip_file:

            for repo_file in repo_files:
                if self.validate_file_by_base_path(repo_file):
                    self.add_file(repo_file, zip_file)

    @staticmethod
    def validate_file_by_base_path(file):
        for allowed_path in ALLOWED_FILETYPES:
            if file.startswith(allowed_path):
                if (
                    allowed_path in EXCEPTION_FILETYPES and
                    file.endswith(*EXCEPTION_FILETYPES[allowed_path])
                ):
                    return False
                return True
        return False

    def add_file(self, relative_file_path, zip_file):
        """Add the given file and all parent directories to the zip."""
        full_file_path = self.plugin_repo_path / relative_file_path
        zip_file.write(full_file_path, relative_file_path)
        directory = full_file_path.parent

        # Get all parent directories to add to the zip
        while directory != self.plugin_repo_path:

            # Is the current directory not yet included in the zip?
            current = directory.replace(
                self.plugin_repo_path,
                "",
            )[1:].replace("\\", "/") + "/"
            if current not in zip_file.namelist():
                zip_file.write(directory, current)

            directory = directory.parent


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == "__main__":

    # Get the plugin to check
    _plugin_name = get_plugin(suffix="release", allow_all=False)

    # Was a valid plugin chosen?
    if _plugin_name is not None:
        clear_screen()

        plugin_releaser = PluginReleaser(_plugin_name)
        if (
            plugin_releaser.validate_diff() and
            plugin_releaser.validate_version_exists()
        ):
            if plugin_releaser.find_new_version():
                plugin_releaser.commit_update()
            plugin_releaser.create_release()
            print(
                f"Successfully created {plugin_releaser.plugin_name} version"
                f" {plugin_releaser.version} release:\n\t"
                f'"{plugin_releaser.zip_path}"\n\n'
            )
