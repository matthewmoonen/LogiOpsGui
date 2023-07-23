import customtkinter as ctk
import tkinter as tk
import sqlite3


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Connect to the SQLite database
conn = sqlite3.connect("user_devices.db")
cursor = conn.cursor()

# Create a table to store user settings
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_devices (
        id INTEGER PRIMARY KEY,
        is_saved INTEGER,
        device_name TEXT,
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
    def __init__(self, name, min_dpi, max_dpi, default_dpi, buttons):
        self.name = name
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.buttons = buttons

# Creating instances of LogitechDevice for each device
devices = [
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
















# Function to load currently edited device from the database
def load_current_device():
    cursor.execute("SELECT * FROM user_devices WHERE is_saved = 0 ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    if row:
        selected_device.set(row[2])
        smartshift_on_var.set(row[3])
        threshold_value.set(row[4])
        torque_value.set(row[5])
        hires_var.set(row[6])
        invert_var.set(row[7])
        target_var.set(row[8])
        dpi_value.set(row[9])
        is_saved.set(row[10])
        
        # Update the state of the spinboxes based on the value of smartshift_on_state
        if row[3]:
            threshold_spinbox.configure(state="normal")
            torque_spinbox.configure(state="normal")
        else:
            threshold_spinbox.configure(state="disabled")
            torque_spinbox.configure(state="disabled")


# Function to save values of the device the user is currently editing into the DB.
def save_current_device():
    is_saved = 0
    device_name = selected_device.get()
    smartshift_on = int(smartshift_on_var.get())
    threshold = int(threshold_value.get())
    torque = int(torque_value.get())
    hires = int(hires_var.get())
    invert = int(invert_var.get())
    target = int(target_var.get())
    dpi = int(dpi_value.get())
    
    # Check if an entry already exists in the database
    cursor.execute("SELECT COUNT(*) FROM user_devices WHERE is_saved = 0")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert a new entry
        cursor.execute("""
            INSERT INTO user_devices (
                is_saved
                device_name,
                smartshift_on_state,
                threshold_value,
                torque_value,
                hires_state,
                invert_state,
                target_state,
                dpi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (is_saved, device_name, smartshift_on, threshold, torque, hires, invert, target, dpi))
    else:
        # Update the existing entry
        cursor.execute("""
            UPDATE user_devices SET
                is_saved
                device_name = ?,
                smartshift_on_state = ?,
                threshold_value = ?,
                torque_value = ?,
                hires_state = ?,
                invert_state = ?,
                target_state = ?,
                dpi = ?
            WHERE is_saved = 0 AND id = (SELECT MAX(id) FROM user_devices WHERE is_saved = 0);
        """, (is_saved, device_name, smartshift_on, threshold, torque, hires, invert, target, dpi))
    
    conn.commit()


def save_as_entry():
    # TODO: create function that saves the currently edited device to the array.
    print('todo')












# Create main window
window = ctk.CTk()
window.title('LogiOpsGUI')  # Define app title
window.geometry('1000x800')  # Define window size
window.resizable(True, True)


# Create label for devices section
your_devices_label = ctk.CTkLabel(master=window, 
    text="Your Devices",
    font=ctk.CTkFont(family="Roboto", size=24),
    padx=20,
    pady=20
    )
your_devices_label.pack(anchor='w')

# Create frame for user's devices
your_devices_frame = ctk.CTkFrame(master=window)
your_devices_frame.pack(padx=20, pady=20, fill="both", expand=True)


# # Load the user settings from the database and set the corresponding variables
# cursor.execute("SELECT * FROM user_devices ORDER BY id DESC LIMIT 1")
# row = cursor.fetchone()



def get_user_devices():
    cursor.execute("""
        SELECT DISTINCT device_name
        FROM user_devices
        WHERE is_saved = 1;
    """)

    user_devices = cursor.fetchall()

    user_devices_list = [row[0] for row in user_devices]
    return user_devices_list


def get_unconfigured_devices():
    all_devices = [device.name for device in devices]
    devices_already_configured = get_user_devices()
    return sorted([i for i in all_devices if i not in devices_already_configured], reverse=True)


# Create dropdown menu
def device_dropdown(new_device):
    print(new_device)

options = get_unconfigured_devices()
add_device_dropdown = ctk.CTkOptionMenu(master=your_devices_frame, variable=ctk.StringVar(value='Select Your Device'), values=options, state="normal", width=300, height=35, command=device_dropdown)
add_device_dropdown.pack(padx=20, pady=10)







def slider_event(value):
    print(value)

slider = ctk.CTkSlider(window, from_=0, to=100, command=slider_event)
slider.pack()



if __name__=="__main__":
    window.mainloop()
