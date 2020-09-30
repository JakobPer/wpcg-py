# wpcg - a simple random wallpaper changer

wpcg is a randmo wallpaper changed developed in Python3 with Qt5 for the GUI. It shows you all the wallpapers in the defined directory randomly and never shows you a wallpaper twice, unless all the wallpapers were already shown. It does that by keeping a history of shown wallpapers in a Sqlite3 database. It also comes with 5 default wallpaper.

Currently supported operating Systems:
 * Windows 10 (others are not tested but might also work)
 * Linux (Cinnamon, Gnome 3)

# Building the app

Although it can be used as a standard Python script, I encourage you to create a binary and or installer, so you can easily add it to your startup programs. For that I use the fbs python package, instructions follow below.

## Dependencies

 * Python 3
 * PyQt5
 * fbs
 * PyInstaller
 
### Linux

First install python3 and pip.

`sudo apt install python3 python-pip`

Then clone the project to a directory of your liking.

`git clone https://github.com/JakobPer/wpcg.git`

Navigate into the directory and create a python virtual environment to keep your standard environment clean.

`python3 -m venv venv`

Activate the venv.

`source venv/bin/activate`

If it is activated you see the venv name in front of your shell like `(venv) user@host: `. After that install the dependencies.

`pip install PyQt5 fbs PyInstaller`

Then to generate the binaries call:

`python3 -m fbs freeze`

Binaries will be generated in the directory `target/wpcg`. Then you can generate an installer if you want with `python3 -m fbs installer` or just copy the binary folder to a installation directory of your liking.

Then you can add the binary to your startup projects

### Windows

Most of the commands are the same on Windows. You only have to download Python3 form the website. The command to activate the venv is `call venv\scripts\activate.bat`. everything else is the same.

If you want to create an installer on windows you also have to install NSIS (https://nsis.sourceforge.io/Main_Page). For further information consult the fbs-tutorial and documentation (https://github.com/mherrmann/fbs-tutorial). 

# Usage

Once started, it is only shown as a TrayIcon in the Taskbar. 
Double clicking the icon will change to the next wallpaper.
Right clicking opens a context menu where you can switch to the next or previous wallpaper, open the settings or exit the application.
In the settings you can the define the wallpaper directory and the interval in which the wallpapers should be changed automatically. 

# Development

If you want to contribute to the project, you can use PyCharm as an IDE. The project files are checked in.
