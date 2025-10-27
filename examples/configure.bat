@echo off
IF NOT EXIST "src\build" MD "src\build"
CD src\build

cmake .. 

IF ERRORLEVEL 0 echo CMake configuration complete. Type build to compile project
cd ..\..