@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Virtual env not found. Create it with:
  echo   py -3.14 -m venv .venv
  echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
  pause
  exit /b 1
)
echo Starting Django on local network: http://0.0.0.0:8000/
echo Open from other devices: http://YOUR_PC_IP:8000/
".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
pause
