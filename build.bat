@echo off
echo - building
pyinstaller --add-data "src\main\python\icons;icons" .\src\main\python\wpcg.py
echo - done