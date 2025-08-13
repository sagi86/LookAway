@echo off
setlocal
cd /d "%~dp0"
py -3w "%~dp0eye_break_popup.pyw" --quiet && goto :eof
if exist "%LocalAppData%\Programs\Python\Python311\pythonw.exe" (
  start "" "%LocalAppData%\Programs\Python\Python311\pythonw.exe" "%~dp0eye_break_popup.pyw" --quiet
  goto :eof
)
if exist "%UserProfile%\anaconda3\pythonw.exe" (
  start "" "%UserProfile%\anaconda3\pythonw.exe" "%~dp0eye_break_popup.pyw" --quiet
  goto :eof
)
echo Could not find a windowless Python. Install Python or edit this file with the correct path.
pause
endlocal
