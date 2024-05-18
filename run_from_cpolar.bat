@echo on

chcp 65001

python3 -m pip install PySocks

set /p confirm=是否获取cpolar信息？(Y/N):

if /i "%confirm%"=="Y" (
    python3 get_cpolar.py
)

if %errorlevel% neq 0 (
    exit /b %errorlevel%
)

for /f %%i in ('python3 get_cpolar.py 2 1') do set url=%%i
for /f %%i in ('python3 get_cpolar.py 2 2') do set port=%%i

set PYTHON2_PATH=C:\Python27
set "PATH=%PYTHON2_PATH%;%PATH%"

python  local.py -s %url% -p %port% -l 1086 -k hello

