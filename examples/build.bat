@echo off
IF NOT EXIST "src\build" GOTO error

cmake --build src\build\. --config Release
EXIT /b 1

:error
ECHO Please configure build before building (call configure.bat)
EXIT /b 1
