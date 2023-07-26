import customtkinter as ctk
# import tkinter as tk
import sqlite3
# import datetime
import time
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
        last_modified INTEGER,
        smartshift_on_state INTEGER,
        threshold_value INTEGER,
        torque_value INTEGER,
        hires_state INTEGER,
        invert_state INTEGER,
        target_state INTEGER,
        dpi INTEGER
    )
""")
conn.commit()



class LogitechDevice:
    def __init__(self, name, min_dpi, max_dpi, default_dpi, buttons, has_thumbwheel):
        self.name = name
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.buttons = buttons
        self.has_thumbwheel = has_thumbwheel

# Creating instances of LogitechDevice for each device
logitech_devices = [
    LogitechDevice("MX Master 3S", 200, 8000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3", "0x00c4"], True),
    LogitechDevice("MX Master 3 for Mac", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3", "0x00c4"], True),
    LogitechDevice("MX Master 3", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3", "0x00c4"], True),
    # 2S Buttons: SEE HERE: https://michael-verschoof.medium.com/setting-up-mx-master-mouse-on-linux-aae0e2ce3962
    LogitechDevice("MX Master 2S", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3", "0x00c4"], True),

    # Based on https://github.com/PixlOne/logiops/blob/main/logid.example.cfg
    # https://github.com/PixlOne/logiops/issues/98
    LogitechDevice("MX Master", 400, 1600, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c3", "0x00c4"], True), 





    # https://harry.sufehmi.com/archives/2021-05-01-linux-and-logitech-mx-anywhere-3/
    LogitechDevice("MX Anywhere 3", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c4", "0x005d", "0x005b"], False),

    # TODO: MX ANYWHERE DOESN'T HAVE THUMB WHEEL    
    # https://gist.github.com/trustin/56ee795930b6eb186bc6a43cedd389f0
    # Based on info found here: https://gist.github.com/trustin/56ee795930b6eb186bc6a43cedd389f0#comments
    # Note: DPI must increment by 200? https://www.anandtech.com/show/9852/the-logitech-mx-anywhere-2-mouse-portable-performance
    LogitechDevice("MX Anywhere 2", 400, 1600, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c4", "0x005d", "0x005b"], False),

    # Increments of 50? https://www.reddit.com/r/MouseReview/comments/7li0wj/logitech_mx_anywhere_2s_dpi_setting/
    LogitechDevice("MX Anywhere 2S", 200, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00c4", "0x005d", "0x005b"], False),



    # no hori scroll
    # https://github.com/PixlOne/logiops/issues/30
    LogitechDevice("MX Vertical", 400, 4000, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x00fd"], False),


    # https://github.com/PixlOne/logiops/issues/65
    # https://github.com/PixlOne/logiops/issues/214
    # No hori scroll
    LogitechDevice("MX Ergo", 512, 2048, 1000, ["0x0050", "0x0051", "0x00ed", "0x005b", "0x005d", "0x0056", "0x0052", "0x0053"], False),
    

    # No hori scroll
    LogitechDevice("MX Ergo M575", 400, 2000, 1000, ["0x0050", "0x0051"], False),

    # Horizontal scroll on vertical scroll wheel
    # Can be customised similar to 
    # https://github.com/PixlOne/logiops/issues/153
    # https://segmentfault.com/a/1190000039985213
    # https://forums.linuxmint.com/viewtopic.php?t=347020
    # https://github.com/PixlOne/logiops/issues/66
    LogitechDevice("M720 Triathlon", 200, 3200, 1000, ["0x0050", "0x0051", "0x0052", "0x0053", "0x0056", "0x005b", "0x005d", "0x00d0", "0x00d7"], False),

    # Has left/right scroll wheel option
    # https://gist.github.com/epassaro/262d435f6449d6b2fff6925e0fad4cd1
    LogitechDevice("M585/M590", 1000, 2000, 1000, ["0x0050", "0x0051", "0x0053", "0x0056", "0x005b", "0x005d", "0x00d7"], False),
    

    LogitechDevice("M500s Corded Mouse", 200, 4000, 1000, ["0x0050", "0x0051"], False),
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
    Control('0x00ed', 'Trackball Sensitivity'),
    Control('0x00ef', 'F key'),
    Control('0x00f0', 'F key'),
    Control('0x00f1', 'F key'),
    Control('0x00f2', 'F key'),
    Control('0x00f3', 'F key'),
    Control('0x00f4', 'F key'),
    Control('0x00f5', 'F key'),
    Control('0x00f6', 'F key'),
    Control('0x00fd', 'Sensitivity Switch'),
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
    current_datetime = int(time.time() * 1e9)
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
    cursor = conn.cursor()

    # Fetch devices from user_devices ordered by date_added descending
    cursor.execute("SELECT device_name FROM user_devices ORDER BY date_added DESC")
    devices = cursor.fetchall()

    # Clear previous widgets from the frame
    for widget in your_devices_frame.winfo_children():
        widget.destroy()


    index = 0
    # Display the devices and their configurations in the frame
    for (device_name,) in devices:
        device_label = ctk.CTkLabel(your_devices_frame, text=device_name)
        device_label.grid(row=index, column=0)

        # Fetch configurations for the current device ordered by last_modified descending
        cursor.execute("SELECT config_name, id FROM user_configs WHERE device_name=? ORDER BY last_modified DESC", (device_name,))
        configs = cursor.fetchall()


        add_config_btn = ctk.CTkButton(your_devices_frame, text="Add Configuration", command=lambda name=device_name: add_config(name))
        add_config_btn.grid(row=index, column=1)
        # Create delete buttons that warn the user if they have a config for that device, simply delete if not
        if len(configs) == 0:
            delete_btn = ctk.CTkButton(your_devices_frame, text="Delete Device", command=lambda name=device_name: delete_device(name))
        else:
            delete_btn = ctk.CTkButton(your_devices_frame, text="Delete Device", command=lambda name=device_name: device_deletion_warning(name))
        delete_btn.grid(row=index, column=2)
        index += 1
        # print(configs)

        for config in configs:
            config_name, config_id = config
            # print(f"Config name: {config_name}, config ID: {config_id}")
            config_label = ctk.CTkLabel(your_devices_frame, text=config_name)
            config_label.grid(row=index, column=0)
            # edit_btn = ctk.CTkButton(your_devices_frame, text="Edit Config", command=lambda name=device_name, cfg=config_name: edit_config(name, cfg))
            edit_btn = ctk.CTkButton(your_devices_frame, text="Edit Config", command=lambda id=config_id: edit_config(id))
            edit_btn.grid(row=index, column=1)
            index += 1

        # for (config_name,) in configs:





def edit_config(cfg):
    print(f"cfg: {cfg}")


def device_deletion_warning(device_name):
    msg = CTkMessagebox(title="Delete Device?",
                        message="Deleting this device will also delete all configurations.",
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
    cursor.execute("DELETE FROM user_configs WHERE device_name=?", (device_name,))
    conn.commit()


    display_devices() # Update the displayed devices
    create_and_update_device_dropdown() # Update device dropdown


def check_highest_config_number(device_name):
    cursor.execute("""
        SELECT config_name
        FROM user_configs
        WHERE device_name LIKE ?
    """, (device_name,))
    default_named_configs = cursor.fetchall()
    highest_config_number = 0
    for i in default_named_configs:
        potential_new_highest = 0
        if i[0][:len(device_name)] == device_name:
            if len(i[0]) == len(device_name):
                potential_new_highest = 1
            elif i[0][len(device_name):len(device_name)+2] == " (" and i[0][-1] == ")":
                try:
                    potential_new_highest = int(i[0][len(device_name)+2:-1])
                except ValueError:
                    continue
        if potential_new_highest > highest_config_number:
            highest_config_number = potential_new_highest

    return highest_config_number




def add_config(device_name):

    new_config_number = check_highest_config_number(device_name) + 1

    if new_config_number == 1:
        new_config_name = device_name
    else:
        new_config_name = f"{device_name} ({new_config_number})"

    current_datetime = int(time.time() * 1e9)


    cursor.execute("""
        INSERT INTO user_configs (
            device_name,
            config_name,
            last_modified
        ) VALUES (?, ?, ?)
    """, (device_name, new_config_name, current_datetime))
    conn.commit()

    display_devices() # Update the displayed devices
    create_and_update_device_dropdown() # Update device dropdown





















display_devices()






if __name__=="__main__":
    window.mainloop()
