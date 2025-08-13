@echo off
setlocal
cd /d "%~dp0"
echo.>"%~dp0STOP_20BREAK.flag"
echo Sent stop signal. The app will exit within a second or two.
timeout /t 2 >nul
del "%~dp0STOP_20BREAK.flag" 2>nul
endlocal
