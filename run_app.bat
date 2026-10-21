@echo off
echo ========================================================
echo   Launching SmartBiz Analytics Full-Stack Platform
echo ========================================================

:: 1. Check if MySQL is listening on 3307
powershell -Command "if (!(Test-NetConnection -ComputerName 127.0.0.1 -Port 3307 -InformationLevel Quiet)) { Start-Process -FilePath cmd -ArgumentList '/k start_mysql.bat' -WindowStyle Minimized }"

:: Wait 2 seconds for MySQL to be ready
timeout /t 2 /nobreak >nul

:: 2. Start Backend API in a separate window
start "SmartBiz Backend API (Port 8000)" cmd /k "start_backend.bat"

:: 3. Start Frontend UI in a separate window
start "SmartBiz Frontend Web (Port 5173)" cmd /k "start_frontend.bat"

:: Wait 3 seconds and launch browser
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================================
echo   SmartBiz Analytics is now running!
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ========================================================
