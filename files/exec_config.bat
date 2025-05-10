@echo off

:: Store the current directory for later use
set STARTDIR=%CD%

:: Does the config.ini file exist?
if not exist %STARTDIR%\config.ini (
    echo No config.ini file found.
    echo Please execute the setup.bat file to create the config.ini before proceeding.
    exit 1
)

:: Get all the configuration values
for /f "eol=# delims=" %%a in (config.ini) do (
    set "%%a"
)

:: Is SUBMODULE_DIRECTORY defined in the config?
if not defined SUBMODULE_DIRECTORY (
    echo SUBMODULE_DIRECTORY not defined in your config.ini.
    exit 1
)

if "%SUBMODULE_DIRECTORY%"=="" (
    echo SUBMODULE_DIRECTORY not set in your config.ini.
    echo Please set this value before continuing.
    exit 1
)

if not exist "%STARTDIR%\%SUBMODULE_DIRECTORY%" (
    echo The SUBMODULE_DIRECTORY is not setup correctly in you config.ini file.
    echo Please set this value to the correct directory name for the PluginHelpers-Base submodule directory.
    exit 1
) else (
    set PLUGIN_HELPERS_DIR=%STARTDIR%/%SUBMODULE_DIRECTORY%
)

:: Is PYTHON_EXECUTABLE defined in the config?
if not defined PYTHON_EXECUTABLE (
    echo SUBMODULE_DIRECTORY not defined in your config.ini.
    exit 1
)

if "%PYTHON_EXECUTABLE%"=="" (
    echo SUBMODULE_DIRECTORY not set in your config.ini.
    echo Please set this value before continuing.
    exit 1
)
