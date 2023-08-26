@echo off
setlocal

REM Check if pyinstaller is installed
pyinstaller --version > nul 2>&1
if %errorlevel% neq 0 (
    echo pyinstaller is not installed. Installing...
    python -m pip install pyinstaller
    echo pyinstaller installation completed.
)

REM Create executable for security_manager.py
C:\Users\vboxuser\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\Scripts\pyinstaller --onefile security_manager.py

REM Create executable for security_manager_off.py
C:\Users\vboxuser\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\Scripts\pyinstaller --onefile security_manager_off.py

pause

endlocal
