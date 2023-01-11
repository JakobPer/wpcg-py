# wpcg-py - a simple random wallpaper changer

wpcg-py is a random wallpaper changed developed in Python3 with Qt6 for the GUI. It shows you all the wallpapers in the defined directory randomly and never shows you a wallpaper twice, unless all the wallpapers were already shown. It does that by keeping a history of shown wallpapers in a Sqlite3 database.

It supports different wallpaper sources that can be enabled separately. Check the wiki for current sources.

Wallpaper 'beautification' is also available if enabled. This allows for images that do not fit the screens aspect ratio to be be repeated, blurred and or blended to create a better fitting wallpaper.

Currently supported operating Systems:
 * Windows 10/11 (others are not tested but might also work)
 * Linux [not tested _yet_] (Cinnamon, Gnome 3)

# Building the app

Although it can be used as a standard Python script, I encourage you to create a binary and so you can easily add it to your startup programs.

Some build scripts are provided, though a better build system will be implemented sometime.

## Dependencies

install the `requirements.txt` with `pip install -r requirements.txt`

The project uses PyQt6 as an UI the UI framework but also had a dependency for pyside6 so we can use the resource compiler that comes with it. Hopefully this will not be necessary in the future.
 
### Linux

First install python3 and pip.

`sudo apt install python3 python-pip`

Then clone the project to a directory of your liking.

`git clone https://github.com/JakobPer/wpcg-py.git`

Navigate into the directory and create a python virtual environment to keep your standard environment clean.

`python3 -m venv .venv`

Activate the venv.

`source .venv/bin/activate`

If it is activated you see the venv name in front of your shell like `(.venv) user@host: `. After that install the dependencies.

`pip install -r requirements`

Generate the binaries with the provided build scripts.

`buid.sh`

The resulting binary will be in the dist folder.

Then you can add the binary to your startup projects

### Windows

For windows building is mostly similar. First install Python version >= 3.10 from the website.

Open a powershell and create the venv with

`python -m venv .venv`

Then activate it with

`.venv\Scripts\Activate.ps1`

Install the dependencies

`pip install -r requirements.txt`

Build the app with the build script

`.\build.ps1`

Binaries will also be in the dist folder

# Usage

Once started, it is only shown as a TrayIcon in the Taskbar. 
Double clicking the icon will change to the next wallpaper.
Right clicking opens a context menu where you can switch to the next or previous wallpaper, open the settings or exit the application.
In the settings you can the define the wallpaper directory and the interval in which the wallpapers should be changed automatically. 

# Development

If you want to contribute to the project, you can use VSCode or PyCharm as an IDE. The project files are checked in.
