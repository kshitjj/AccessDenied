@echo off

set "python_script=security_manager.py"

powershell -Command "Start-Process 'python' -ArgumentList '%python_script%' -Verb 'RunAs'"

echo Everything reverted
