@echo off
rem Force only the primary monitor
displayswitch /internal
timeout /t 2 /nobreak >nul
displayswitch /extend
timeout /t 2 /nobreak >nul

rem Restart AMD Adrenalin Software
taskkill /F /IM "RadeonSoftware.exe"
timeout /t 3 /nobreak >nul
start "" "C:\Program Files\AMD\CNext\CNext\RadeonSoftware.exe"
timeout /t 5 /nobreak >nul
echo AMD ReLive should now record the correct monitor.
pause
