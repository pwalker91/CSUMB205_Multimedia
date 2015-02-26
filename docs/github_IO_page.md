# CSU Monterey Bay CST205

## Simple Multimedia Classes

## Current Version: v0.8.5

This project offers students access to a simple RGB Image class, which is built on the use of the Image module in the PIL package. As PIL is no longer updated for Python 3, this package relies on *Pillow*.

This package assumes that the user is using at least Python 3.4.

**If you have not installed Python 3.4.2 or greater, please download it from** [python.org](https://www.python.org/downloads/release/python-342/).


***
## INSTALLATION on WINDOWS

If you are using Windows, make sure to check the option to *add the* **python.exe** *to your path*. PIP will not work otherwise.
![What option to check](https://cloud.githubusercontent.com/assets/6844526/6278829/204e939c-b84f-11e4-8aae-4a7f1e73a6aa.PNG)
Be sure to change the red X to the same symbols as the above options

Windows 8 users will also need to download and install the [numpy package](http://sourceforge.net/projects/numpy/files/NumPy/1.9.1/numpy-1.9.1-win32-superpack-python3.4.exe/download) manually from the link given.

Please start the Command Prompt program and try typing `python`. If you get back the error message `"python" is not a recognized command`, please restart your computer.

You can download this package through the use of PIP, a built-in package installer that comes with Python 3.4.2. Go to the start menu and open an administrator command prompt. Then run...

     pip install csumb205-multimedia

Before pressing enter, your Command Prompt screen should look similar to this...
![Command to type](https://cloud.githubusercontent.com/assets/6844526/6278828/204da70c-b84f-11e4-9f6a-32816d371379.PNG)

***
## INSTALLATION on MAC OSX

On Mac OSX, you will have multiple versions of Python. You *still* need to install Python 3.4.2, but you will open Terminal, and type the command...

     pip3 install csumb205-multimedia

Before pressing enter, your Terminal screen should look like this...
![Command to type](https://cloud.githubusercontent.com/assets/6844526/6278864/71274c64-b84f-11e4-8c04-254c4686cc7d.jpg)

***
## UPDATING your VERSION

If you already downloaded the package with PIP, but see that the version number has changed, you can simply update the package using PIP. Simply type this command...

     pip install --upgrade csumb205-multimedia

If you are on Mac OSX, please use `pip3` instead of `pip`.

***
## USAGE

For an introduction into how to use the different available classes, please [see this page](./how_to.html)

For a more complete documentation of the different available classes, please [see this page](./docu.html)

***
### PyPI:
The Python Package Index page for this package can be [found here](https://pypi.python.org/pypi/csumb205-multimedia).