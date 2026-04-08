@echo off
setlocal
set ROOT=C:\backup_nosql
cd /d %ROOT%

set PY=%ROOT%\venv\Scripts\python.exe
if not exist "%PY%" (
  echo Python venv not found at %PY%
  echo Create it first: python -m venv venv
  exit /b 1
)

set PORT=%1
if "%PORT%"=="" set PORT=8000

echo Starting FastAPI on http://127.0.0.1:%PORT%
"%PY%" -m uvicorn --app-dir %ROOT% main:app --reload --host 127.0.0.1 --port %PORT%
endlocal
