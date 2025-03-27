# LogiOpsGui

## What is this?
An unofficial, open source GUI configuration tool for the Linux Logiops mouse drivers.

This app allows you to customize the buttons of your Logitech MX Series mouse. You can create, edit, rename, modify, and delete configuration profiles. It supports customisations like keyboard shortcuts, scroll actions, gestures, axes, SmartShift configurations, DPI settings, and more.

It supports multiple configurations and devices. You can load a new configuration and restart the Logiops service directly from within the app.

This app is intended as a companion to [PixlOne's drivers](https://github.com/PixlOne/logiops).

## Installation

First install the [Logiops drivers](https://github.com/PixlOne/logiops) following the instructions on that page.

If you're already using Logiops, I recommend backing up your current configuration file.

### Requirements
You will need **Python**, **Git** and **Tkinter** installed. 

Below are the installation commands for common distros:

Debian-based systems:
`sudo apt install python3-tk`

Arch:
`sudo pacman -S tk`

Fedora:
`sudo dnf install python3-tkinter`


You may also need to install the virtual environment module separately.


### Getting Started

Clone the repository:

`git clone https://github.com/matthewmoonen/LogiOpsGui`

Navigate to the directory:

`cd LogiOpsGui`

Run the install script:

`./install.sh`

To verify the installation, activate the virtual environment 

`source venv/bin/activate`

run the application from the terminal:

`python3 logui.py`


If there are no errors, you're good to go. You can close the terminal and open the app from your app launcher.


## Screenshots
![image](/screenshots/001.png)

![image](/screenshots/003.png)

![image](/screenshots/002.png)


## Use

### Using the GUI



* Add your device from the dropdown menu
* In the left panel, you can name your configuration and change DPI, SmartShift, and scroll wheel settings.
* The panel on the right gives access to the button, gesture and scrollwheel customisations. 
* Select the button/scrollwheel you want to customise. A menu will appear on the right with some pre-populated options.
* Select one of the radio buttons or click the green button to add a customisation. 
* If your device supports gestures, you will see a radio button for this. Selecting the radio button will open another page where you can add customisations for each gesture direction (up, down, left, right, none).


### Saving the configuration

Navigate back to the main page. There are a few options. 

* **Save as Copy:**

    This generates a configuration file in the directory you choose. You'll need to copy this file to /etc/ and restart the Logiops service manually.

* **Apply and Restart:**

    This button generates the configuration file, copies it to /etc/, and restarts the Logiops service.

    To do this, elevated privileges are required. You have two options:

    1. Use pkexec (you'll be prompted to enter your password each time). Depending on your distro, pkexec may already be installed. If not, you will need to install it.
    2. Permanently grant elevated permissions to the BASH script (a tutorial for this is coming soon).


## Issues


There are inherent DPI scaling issues with the GUI library that has been used to make this app, which make it challenging to maintain a consistent appearance across different monitors, distros, and desktop environments. You might experience some inconsistencies with the appearance of buttons and menus depending on your setup.

There are a few things I can do to improve this, such as building custom button classes using SVG files. I've already done this for the radio buttons. Ultimately, however, the best solution will be to rewrite everything in C++. That's my plan, but I'll need to brush up on my C++ skills, so it will take some time.

In the meantime, this tool is pretty effective for creating Logiops configuration files, and it certainly speeds up the process.

Feel free to reach out with any bugs you encounter or issues getting it to work.


## Saving a backup 

You can save a copy of all your configurations by making a copy of your sql file. This is the `app_records.db` file in your `/app_data` folder.
