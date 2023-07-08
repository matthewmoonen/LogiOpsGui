import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("user_settings.db")
cursor = conn.cursor()

# Create a table to store user settings
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_settings (
        id INTEGER PRIMARY KEY,
        selected_device TEXT,
        on_state INTEGER,
        threshold_value INTEGER,
        torque_value INTEGER,
        hires_state INTEGER,
        invert_state INTEGER,
        target_state INTEGER
    )
""")
conn.commit()

# Function to save user settings to the database
def save_user_settings():
    selected = selected_device.get()
    on = int(on_var.get())
    threshold = int(threshold_value.get())
    torque = int(torque_value.get())
    hires = int(hires_var.get())
    invert = int(invert_var.get())
    target = int(target_var.get())
    
    # Check if an entry already exists in the database
    cursor.execute("SELECT COUNT(*) FROM user_settings")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert a new entry
        cursor.execute("""
            INSERT INTO user_settings (
                selected_device, on_state, threshold_value, torque_value, hires_state, invert_state, target_state
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (selected, on, threshold, torque, hires, invert, target))
    else:
        # Update the existing entry
        cursor.execute("""
            UPDATE user_settings SET
            selected_device = ?, on_state = ?, threshold_value = ?, torque_value = ?,
            hires_state = ?, invert_state = ?, target_state = ?
            WHERE id = 1
        """, (selected, on, threshold, torque, hires, invert, target))
    
    conn.commit()

# Function to load user settings from the database
def load_user_settings():
    cursor.execute("SELECT * FROM user_settings ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        selected_device.set(row[1])
        on_var.set(row[2])
        threshold_value.set(row[3])
        torque_value.set(row[4])
        hires_var.set(row[5])
        invert_var.set(row[6])
        target_var.set(row[7])
        
        # Update the state of the spinboxes based on the value of on_state
        if row[2]:
            threshold_spinbox.configure(state="normal")
            torque_spinbox.configure(state="normal")
        else:
            threshold_spinbox.configure(state="disabled")
            torque_spinbox.configure(state="disabled")

# Create main window
window = tk.Tk()
window.title('LogiOpsGUI')  # Define app title
window.geometry('800x800')  # Define window size




# Load the user settings from the database and set the corresponding variables
cursor.execute("SELECT * FROM user_settings ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

# Create first widget
title_label = ttk.Label(master=window, text="LogiOpsGUI", font='Calibri 24 bold')
title_label.pack()  # Put widget on root window

# Create label for the dropdown menu
label = ttk.Label(master=window, text="Select your device")
label.pack()

# Create dropdown menu
options = ['MX Master 3', 'MX Master 3 for Mac', 'MX Master 2S', 'MX Master']  # List of options for the dropdown menu
selected_device = tk.StringVar()  # Variable to store the selected option
dropdown = ttk.Combobox(master=window, textvariable=selected_device, values=options, state="readonly")
dropdown.pack()

if row:
    selected_device.set(row[1])




# Create container for SmartShift widgets
smartshift_frame = ttk.LabelFrame(master=window, text="SmartShift")
smartshift_frame.pack(pady=10)

# Create boolean selection box
on_var = tk.BooleanVar()
on_checkbox = ttk.Checkbutton(master=smartshift_frame, text="On", variable=on_var)
on_checkbox.grid(row=0, column=0, padx=5, pady=5)

# Create threshold input
threshold_value = tk.StringVar(value="30")  # Default value for threshold
threshold_label = ttk.Label(master=smartshift_frame, text="Threshold")
threshold_label.grid(row=0, column=1, padx=5, pady=5)
threshold_spinbox = ttk.Spinbox(master=smartshift_frame, from_=0, to=100, textvariable=threshold_value, validate="key")
threshold_spinbox.grid(row=0, column=2, padx=5, pady=5)

# Create torque input
torque_value = tk.StringVar(value="50")  # Default value for torque
torque_label = ttk.Label(master=smartshift_frame, text="Torque")
torque_label.grid(row=1, column=1, padx=5, pady=5)
torque_spinbox = ttk.Spinbox(master=smartshift_frame, from_=0, to=100, textvariable=torque_value, validate="key")
torque_spinbox.grid(row=1, column=2, padx=5, pady=5)

# Configure threshold and torque spinbox widgets
threshold_spinbox.configure(state="disabled")  # Disable threshold spinbox by default
torque_spinbox.configure(state="disabled")  # Disable torque spinbox by default

# Function to enable/disable threshold and torque spinboxes based on the state of the "on" checkbox
def toggle_spinboxes():
    if on_var.get():
        threshold_spinbox.configure(state="normal")
        torque_spinbox.configure(state="normal")
    else:
        threshold_spinbox.configure(state="disabled")
        torque_spinbox.configure(state="disabled")
        if not threshold_value.get():
            threshold_value.set("0")
        if not torque_value.get():
            torque_value.set("0")

# Toggle spinboxes when the "on" checkbox is clicked
on_checkbox.configure(command=toggle_spinboxes)

# Validate input in threshold and torque spinboxes to allow only integer values between 0 and 100
def validate_integer(value):
    if value.isdigit() or value == "":
        if value == "":
            return True
        else:
            int_value = int(value)
            if 0 <= int_value <= 100:
                return True
    return False

validate_command = (window.register(validate_integer), "%P")
threshold_spinbox.configure(validate="key", validatecommand=validate_command)
torque_spinbox.configure(validate="key", validatecommand=validate_command)

# Update threshold spinbox to display 0 when focus is lost and value is empty
def update_threshold_value(event):
    if not threshold_value.get():
        threshold_value.set("0")

# Bind <FocusOut> event to threshold spinbox
threshold_spinbox.bind("<FocusOut>", update_threshold_value)

# Update torque spinbox to display 0 when focus is lost and value is empty
def update_torque_value(event):
    if not torque_value.get():
        torque_value.set("0")

# Bind <FocusOut> event to torque spinbox
torque_spinbox.bind("<FocusOut>", update_torque_value)

# Open dropdown when clicking anywhere in the box
def open_dropdown(event):
    dropdown.event_generate("<Down>")

# Bind <1> event to dropdown box
dropdown.bind("<1>", open_dropdown)

# Create container for HiRes mouse-scrolling widgets
hires_frame = ttk.LabelFrame(master=window, text="HiRes mouse-scrolling")
hires_frame.pack(pady=10)

# Create HiRes checkbox with default value True
hires_var = tk.BooleanVar(value=True)
hires_checkbox = ttk.Checkbutton(master=hires_frame, text="HiRes", variable=hires_var)
hires_checkbox.grid(row=0, column=0, padx=5, pady=5)

# Create Invert checkbox with default value False
invert_var = tk.BooleanVar(value=False)
invert_checkbox = ttk.Checkbutton(master=hires_frame, text="Invert", variable=invert_var)
invert_checkbox.grid(row=0, column=1, padx=5, pady=5)

# Create Target checkbox with default value False
target_var = tk.BooleanVar(value=False)
target_checkbox = ttk.Checkbutton(master=hires_frame, text="Target", variable=target_var)
target_checkbox.grid(row=0, column=2, padx=5, pady=5)




# Load the user settings from the database
load_user_settings()

# Save user settings to the database when the window is closed
def save_and_close():
    save_user_settings()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", save_and_close)

# Run the main window
window.mainloop()

# Close the database connection
cursor.close()
conn.close()