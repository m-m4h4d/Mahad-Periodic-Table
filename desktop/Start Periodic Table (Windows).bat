@echo off
rem Starts the MTH Periodic Table with the installed Python 3.
cd /d "%~dp0"
where pyw >nul 2>nul && (start "" pyw -3 launcher.py & exit /b 0)
where pythonw >nul 2>nul && (start "" pythonw launcher.py & exit /b 0)
where py >nul 2>nul && (py -3 launcher.py & exit /b)
where python >nul 2>nul && (python launcher.py & exit /b)
echo Python 3 is required to run the MTH Periodic Table.
echo Download it from https://www.python.org/downloads/ and run this file again.
pause
