@ECHO off

SET testing=Checking for Python:
WHERE python >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
	ECHO %testing% [OK]
) ELSE (
	ECHO %testing% [NA]
	ECHO Please install Python 2.x or 3.x from https://www.python.org/downloads/ and ensure that it is added to PATH during installation.
    ECHO If Python is installed, run this program as Administrator.
    IF NOT %0 == "%~0" PAUSE
	EXIT 1
)

python %~dp0\install.py nt

IF NOT %0 == "%~0" PAUSE