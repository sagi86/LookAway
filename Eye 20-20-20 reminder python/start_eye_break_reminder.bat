@echo off
setlocal
REM Run from the folder this BAT is in:
cd /d "%~dp0"
REM Prefer the Python launcher (windowless)
py -3w "%~dp0eye_break_popup.pyw" %* && goto :eof

REM Fallbacks: edit if needed
if exist "%LocalAppData%\Programs\Python\Python311\pythonw.exe" (
  start "" "%LocalAppData%\Programs\Python\Python311\pythonw.exe" "%~dp0eye_break_popup.pyw" %*
  goto :eof
)
if exist "%UserProfile%\anaconda3\pythonw.exe" (
  start "" "%UserProfile%\anaconda3\pythonw.exe" "%~dp0eye_break_popup.pyw" %*
  goto :eof
)
echo Could not find a windowless Python. Install Python or edit this file with the correct path.
pause
endlocal
