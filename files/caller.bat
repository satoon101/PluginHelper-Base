@echo off

:: Execute the configuration
call exec_config

if %errorlevel% == 0 (
    %PYTHON_EXECUTABLE% %STARTDIR%/%SUBMODULE_DIRECTORY%/packages/%~n0.py
    pause
)
