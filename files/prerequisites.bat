@echo off

:: Execute the configuration
call exec_config

:: Did the configuration encounter no errors?
if %errorlevel% == 0 (
    %PYTHON_EXECUTABLE% -m pip install --upgrade pip
    %PYTHON_EXECUTABLE% -m pip install --upgrade -r %SUBMODULE_DIRECTORY%/tools/requirements.txt
)
pause
