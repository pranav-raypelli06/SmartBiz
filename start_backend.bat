@echo off
echo ========================================================
echo Starting SmartBiz Analytics Backend API (FastAPI)
echo ========================================================
cd /d "%~dp0"
py -3.14 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause
