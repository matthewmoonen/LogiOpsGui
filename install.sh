#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "This program needs Python to run. Install Python first and then re-run this utility."
    exit 1
fi  # Added missing 'fi' here

echo "Creating and activating virtual environment.
"

python3 -m venv venv

source venv/bin/activate

echo "Upgrading pip and installing dependencies

"

pip install --upgrade pip

pip install -r requirements.txt


# Check if an create desktop entry argument is provided
createDesktopEntry=true
if [ -n "$1" ]; then
  case "$1" in
    --createDesktopEntry=false)
      createDesktopEntry=false
      echo "No desktop entry will be created"
      ;;
    --createDesktopEntry=true|--createDesktopEntry)
      createDesktopEntry=true
      echo "Creating desktop entry"
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
fi

if [ "$createDesktopEntry" = true ]; then

    # Get the current working directory
    cwd=$(pwd)

echo "
Creating .Desktop entry
"

    # Create the content for the .desktop entry
desktop_entry="[Desktop Entry]
Version=1.0
Name=LogiOpsGUI
Comment=Configuration tool for Logitech mouse drivers
Exec=${cwd}/run.sh
Icon=${cwd}/images/icon.png
Terminal=false
Type=Application
Categories=Utility;"

    # Define the path to the applications directory
    desktop_path="${HOME}/.local/share/applications"

    # Create the directory if it doesn't exist
    mkdir -p "$desktop_path"

    # Define the full path to the .desktop file
    desktop_file_path="${desktop_path}/LogiOpsGUI.desktop"

    # Write the .desktop entry to the file
    echo "$desktop_entry" > "$desktop_file_path"

    # Set the correct permissions for the .desktop file
    chmod 755 "$desktop_file_path"

    echo "Desktop entry created at $desktop_file_path"

fi

echo "Installation complete."
