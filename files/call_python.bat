@echo off

:: Did the configuration encounter no errors?
if %errorlevel% == 0 (

    :: Call the given package
    %PYTHON_EXECUTABLE% %PLUGIN_HELPERS_DIR%\packages\%~n1.py
)
