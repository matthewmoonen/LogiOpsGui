

device_dict = {
    "MX Master 3" : "Wireless Mouse MX Master 3",
    "MX Master 3 for Mac" : "MX Master 3 for Mac",
    "MX Master 2S" : "Wireless Mouse MX Master 2S",
    "MX Master" : "Wireless Mouse MX Master"
}

# print(device_dict["MX Master"])

import sqlite3

# Connect to the database
conn = sqlite3.connect('user_settings.db')
cursor = conn.cursor()

# Retrieve data from the "user_settings" table
cursor.execute("SELECT * FROM user_settings")
rows = cursor.fetchall()

# Generate the .cfg file
with open("logid.cfg", "w") as cfg_file:
    for row in rows:
        id_, selected_device, on_state, threshold_value, torque_value, hires_state, invert_state, target_state = row
        cfg_file.write(f"devices: (\n")
        cfg_file.write(f"{{\n")
        cfg_file.write(f'    name: "{device_dict[selected_device]}";\n')
        
        cfg_file.write(f"    smartshift:\n")
        cfg_file.write(f"    {{\n")
        cfg_file.write(f"        on: {'true' if on_state else 'false'};\n")
        cfg_file.write(f"        threshold: {threshold_value};\n")
        cfg_file.write(f"        torque: {torque_value};\n")
        cfg_file.write(f"    }};\n")

        cfg_file.write(f"    hiresscroll:\n")
        cfg_file.write(f"    {{\n")
        cfg_file.write(f"        hires: {'true' if hires_state else 'false'};\n")
        cfg_file.write(f"        invert: {'true' if invert_state else 'false'}\n")
        cfg_file.write(f"        target: {'true' if target_state else 'false'}\n")
        cfg_file.write(f"}}\n")
        cfg_file.write(f");")

# Close the database connection
conn.close()
