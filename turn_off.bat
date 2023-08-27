@echo off

set "python_script=security_manager_off.py"

powershell -Command "Start-Process 'python' -ArgumentList '%python_script%' -Verb 'RunAs'"

echo Everything reverted
