@echo off

set "python_script=security_manager_off.py"
reg add "HKCU\Software\Policies\Microsoft\Windows\System" /v DisableCMD /t REG_DWORD /d 0 /f

powershell -Command "Start-Process 'python' -ArgumentList '%python_script%' -Verb 'RunAs'"

echo Everything reverted
