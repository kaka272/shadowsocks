@echo off

python3 -m pip install PySocks
python3 get_cpolar.py

for /f %%i in ('python3 get_cpolar.py 2 1 <nul') do set url=%%i
for /f %%i in ('python3 get_cpolar.py 2 2 <nul') do set port=%%i

set PYTHON2_PATH=C:\Python27
set "PATH=%PYTHON2_PATH%;%PATH%"

python2  local.py -s %url% -p %port% -l 1085 -k hello

