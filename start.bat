@echo off
title TPS - Debug console

chdir /d F:\Running Projects\TPS\src
echo _____________________  _________ 
echo \__    ___/\______   \/   _____/ 
echo   ^|    ^|    ^|     ___/\_____  \  
echo   ^|    ^|    ^|    ^|    /        \ 
echo   ^|____^|    ^|____^|   /_______  / 
echo                              \/  
echo.
echo.
echo TPS Development server ...
echo Current directory: %cd%
echo.
start firefox http://127.0.0.1:5000/
set FLASK_APP=main.py
set FLASK_ENV=development

flask run --host=0.0.0.0 && exit
