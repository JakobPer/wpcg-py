@echo off
echo - building
pyinstaller -y --noconsole -i .\src\main\python\icons\Icon.ico --add-data "src\main\python\icons;icons" .\src\main\python\wpcg.py
echo - done