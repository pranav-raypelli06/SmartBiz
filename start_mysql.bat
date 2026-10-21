@echo off
echo ========================================================
echo Starting SmartBiz Analytics MySQL Database on Port 3307
echo ========================================================
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" --port=3307 --datadir="%~dp0database\mysql_data" --console
pause
