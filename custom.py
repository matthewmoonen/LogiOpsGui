import customtkinter as ctk
# import tkinter as tk
import sqlite3
import datetime
from CTkMessagebox import CTkMessagebox


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Connect to the SQLite database
conn = sqlite3.connect("user_devices.db")
cursor = conn.cursor()

# Create a table to store user settings
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_devices (
        id INTEGER PRIMARY KEY,
        device_name TEXT,
        date_added INTEGER,
        is_activated INTEGER
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_configs (
        id INTEGER PRIMARY KEY,
        device_name TEXT,
        config_name TEXT,
        last_modified INTEGER
    )
""")
conn.commit()



class LogitechDevice:
    def __init__(self, name, min_dpi, max_dpi, default_dpi, buttons):
        self.name = name
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.buttons = buttons

# Creating instances of LogitechDevice for each device
logitech_devices = [
    LogitechDevice("MX Master 3", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3"]),
    LogitechDevice("MX Master 3 for Mac", 200, 4000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Master 2S", 200, 4000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Master", 400, 1600, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Anywhere 2S", 200, 4000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Anywhere 3", 200, 4000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Vertical", 400, 4000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Ergo", 512, 2048, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("MX Ergo M575", 400, 2000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("M720 Triathlon", 200, 3200, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("M590 Multi-Device Silent", 1000, 2000, 1000, ["0x0050", "0x0051"]),
    LogitechDevice("M500s Advanced Corded Mouse", 200, 4000, 1000, ["0x0050", "0x0051"]),
]


class Control:
    def __init__(self, control_id, function):
        self.control_id = control_id
        self.function = function

table_data = [
    Control('0x0050', 'Left Mouse Button'),
    Control('0x0051', 'Right Mouse Button'),
    Control('0x0052', 'Middle Mouse Button'),
    Control('0x0053', 'Back Button'),
    Control('0x0054', 'Back Button'),
    Control('0x0056', 'Forward Button'),
    Control('0x0057', 'Forward Button'),
    Control('0x005b', 'Left Scroll'),
    Control('0x005d', 'Right Scroll'),
    Control('0x006e', 'Show Desktop'),
    Control('0x006f', 'Lock Screen'),
    Control('0x0090', 'Minimize'),
    Control('0x0091', 'Maximize'),
    Control('0x0095', 'Switch Screens'),
    Control('0x00ba', 'Switch Apps'),
    Control('0x00bb', 'Home'),
    Control('0x00bc', 'Menu'),
    Control('0x00bd', 'Back Button'),
    Control('0x00be', 'Generic'),
    Control('0x00bf', 'Print Screen'),
    Control('0x00c0', 'Generic'),
    Control('0x00c1', 'Generic'),
    Control('0x00c2', 'Lock Screen'),
    Control('0x00c3', 'Gesture Button'),
    Control('0x00c4', 'Toggle SmartShift'),
    Control('0x00c7', 'Decrease Brightness'),
    Control('0x00c8', 'Increase Brightness'),
    Control('0x00cc', 'Switch Apps'),
    Control('0x00ce', 'Back Button'),
    Control('0x00cf', 'Forward Button'),
    Control('0x00d0', 'Switch Apps'),
    Control('0x00d1', 'Generic'),
    Control('0x00d2', 'Generic'),
    Control('0x00d3', 'Generic'),
    Control('0x00d4', 'Search'),
    Control('0x00d5', 'Home'),
    Control('0x00d6', 'Menu'),
    Control('0x00d7', 'Switch Receivers'),
    Control('0x00dd', 'Select Language'),
    Control('0x00e0', 'Task View'),
    Control('0x00e1', 'Action Center'),
    Control('0x00e2', 'Decrease Backlight'),
    Control('0x00e3', 'Increase Backlight'),
    Control('0x00e4', 'Previous Track'),
    Control('0x00e5', 'Play/Pause'),
    Control('0x00e6', 'Next Track'),
    Control('0x00e7', 'Mute'),
    Control('0x00e8', 'Volume Down'),
    Control('0x00e9', 'Volume Up'),
    Control('0x00ea', 'App Menu'),
    Control('0x00ed', 'Trackball Sensitivity?'),
    Control('0x00ef', 'F key'),
    Control('0x00f0', 'F key'),
    Control('0x00f1', 'F key'),
    Control('0x00f2', 'F key'),
    Control('0x00f3', 'F key'),
    Control('0x00f4', 'F key'),
    Control('0x00f5', 'F key'),
    Control('0x00f6', 'F key'),
    Control('0x00fd', 'Mouse Sensitivity'),
    Control('0x00fe', 'Home')
]














def save_as_entry():
    # TODO: create function that saves the currently edited device to the array.
    pass












# Create main window
window = ctk.CTk()
window.title('LogiOpsGUI')  # Define app title
window.geometry('1000x800')  # Define window size
window.resizable(True, True)


# Create frame for 
add_device_frame = ctk.CTkFrame(master=window)
add_device_frame.pack(padx=20, pady=20, fill="x")

# Create frame for user's devices
your_devices_frame = ctk.CTkFrame(master=window)
your_devices_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Create label for devices section
your_devices_label = ctk.CTkLabel(master=your_devices_frame, 
    text="Your Devices",
    font=ctk.CTkFont(family="Roboto", size=24),
    padx=20,
    pady=20
    )
# your_devices_label.pack(anchor='w')
your_devices_label.grid(row=0, column=0, padx=20, pady=20)
                        
# # Load the user settings from the database and set the corresponding variables
# cursor.execute("SELECT * FROM user_devices ORDER BY id DESC LIMIT 1")
# row = cursor.fetchone()



def get_user_devices():
    cursor.execute("""
        SELECT DISTINCT device_name
        FROM user_devices
    """)

    user_devices = cursor.fetchall()

    user_devices_list = [row[0] for row in user_devices]
    return user_devices_list


def get_unconfigured_devices():
    all_devices = [device.name for device in logitech_devices]
    return sorted([i for i in all_devices if i not in get_user_devices()], reverse=True)


add_device_label = ctk.CTkLabel(your_devices_frame, text="Add New Device")
add_device_label.grid(row=1, column=0, padx=20, pady=20)

# Create dropdown menu
def device_dropdown(new_device):
    add_device_button.configure(state="normal")
    add_device_button.configure(fg_color="#208637")
    add_device_button.configure(command=lambda: on_button_click(new_device))  # Update button command with selected option




def create_and_update_device_dropdown():
    options = get_unconfigured_devices()
    selected_option_var = ctk.StringVar(value='Select Device To Add')
    add_device_dropdown = ctk.CTkOptionMenu(master=add_device_frame,
                                            variable=selected_option_var,
                                            values=options,
                                            state="normal",
                                            width=400,
                                            height=36,
                                            command=device_dropdown)
    add_device_dropdown.grid(row=0,
                            column=0,
                            padx=20,
                            pady=20)

create_and_update_device_dropdown()

def on_button_click(selected_option):
    add_device_button.configure(state="disabled", fg_color=("#545B62"))
    current_datetime = int(datetime.datetime.now().timestamp())
    cursor.execute("""
        INSERT INTO user_devices (
            device_name,
            date_added
        ) VALUES (?, ?)
    """, (selected_option, current_datetime))

    conn.commit()
    create_and_update_device_dropdown()
    display_devices()

add_device_button = ctk.CTkButton(master=add_device_frame,
                                  height=40,
                                  width=120,
                                  state="disabled",
                                  text="Add Device",
                                  text_color_disabled=("#9FA5AB"),
                                  fg_color=("#545B62"),
                                  hover_color=("#28A745"),
                                  command=lambda: on_button_click('Select Device To Add'))
add_device_button.grid(row=0, column=1)



def display_devices():

# Fetch devices and configurations in reverse chronological order
    cursor.execute("SELECT user_devices.device_name, user_configs.config_name, user_configs.last_modified "
                    "FROM user_devices "
                    "LEFT JOIN user_configs "
                    "ON user_devices.device_name = user_configs.device_name "
                    "ORDER BY user_devices.date_added DESC")

    devices_with_configs = {}
    for device_name, config_name, last_modified in cursor.fetchall():
        if device_name not in devices_with_configs:
            devices_with_configs[device_name] = []
        if config_name:
            devices_with_configs[device_name].append((config_name, last_modified))

    # Clear previous widgets from the frame
    for widget in your_devices_frame.winfo_children():
        widget.destroy()

    # Display the devices and their configurations in the frame
    for idx, (device_name, configs) in enumerate(devices_with_configs.items()):
        device_label = ctk.CTkLabel(your_devices_frame, text=device_name)
        device_label.grid(row=idx * 2, column=0)
        print(device_name)
        print(configs)
        # delete_btn = ctk.CTkButton(your_devices_frame, text="Delete Device", command=lambda name=device_name: delete_device(name))
        delete_btn = ctk.CTkButton(your_devices_frame, text="Delete Device", command=lambda name=device_name: device_deletion_warning(name))

        delete_btn.grid(row=idx * 2, column=1)

        for config_idx, (config_name, _) in enumerate(configs):
            config_label = ctk.CTkLabel(your_devices_frame, text=config_name)
            config_label.grid(row=idx * 2 + config_idx + 1, column=0)

            edit_btn = ctk.CTkButton(your_devices_frame, text="Edit Config", command=lambda name=device_name, cfg=config_name: edit_config(name, cfg))
            edit_btn.grid(row=idx * 2 + config_idx + 1, column=1)


def device_deletion_warning(device_name):
    msg = CTkMessagebox(title="Delete Device?",
                        message="Deleting this device will also delete all configurations.\n To suspend the device but keep your configurations, uncheck the uncheck button.",
                        # icon="warning",
                        option_1="Delete",
                        option_2="Cancel",
                        width=600,
                        height=300,
                        fade_in_duration=200
                        )
    
    if msg.get()=="Delete":
        delete_device(device_name)

def delete_device(device_name):
    # Function to delete the selected device from the database and the frame
    cursor.execute("DELETE FROM user_devices WHERE device_name=?", (device_name,))
    conn.commit()
    
    display_devices() # Update the displayed devices
    create_and_update_device_dropdown() # Update device dropdown






display_devices()






if __name__=="__main__":
    window.mainloop()
