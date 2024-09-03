#!/bin/bash

# Define the script's directory
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Copy the logid.cfg file from app_data to /etc/
cp "$SCRIPT_DIR/app_data/logid.cfg" /etc/logid.cfg

# Restart the logid service
systemctl restart logid

systemctl status logid
