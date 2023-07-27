import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("sql.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE Devices (
        device_id INTEGER PRIMARY KEY,
        device_name TEXT NOT NULL,
        cfg_file_name TEXT NOT NULL,
        has_thumbwheel INTEGER NOT NULL,
        date_created INTEGER NOT NULL
    );
    """)

cursor.execute("""
    CREATE TABLE Configurations (
        configuration_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        configuration_name TEXT NOT NULL,
        last_modified INTEGER NOT NULL
               
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """)

cursor.execute("""
    CREATE TABLE Buttons (
        button_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        button_cid TEXT NOT NULL,
        button_name TEXT NOT NULL,
        reprog INTEGER NOT NULL,
        fn_key INTEGER NOT NULL,
        mouse_key INTEGER NOT NULL,
        gesture_support INTEGER NOT NULL
               
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """)
               
cursor.execute("""
    CREATE TABLE User_Button_Customisations (
        user_button_customisation_id INTEGER NOT NULL,
        device_id INTEGER NOT NULL,
        configuration_id INTEGER NOT NULL,
        button_id INTEGER NOT NULL,
        action TEXT
               
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id)
    FOREIGN KEY (button_id) REFERENCES Buttons(button_id)
    );
    """)






cursor.execute("""
    CREATE TABLE Gestures (
        gesture_id INTEGER PRIMARY KEY,
        button_id INTEGER NOT NULL,
        user_button_customisation_id INTEGER NOT NULL,
        direction TEXT NOT NULL,
        action TEXT NOT NULL,
        threshold INTEGER NOT NULL,
        mode TEXT,
        axis TEXT,
        axis_multiplier INTEGER,
        keys TEXT
    FOREIGN KEY (button_id) REFERENCES Buttons(button_id)
    FOREIGN KEY (user_button_customisation_id) REFERENCES User_Button_Customisations(user_button_customisation_id)
    );
    """)






cursor.execute("""
    CREATE TABLE cycle_dpi (
    cycle_dpi_id INTEGER PRIMARY KEY,
    user_button_customisation_id INTEGER NOT NULL,
    gesture_id INTEGER,
    dpi_array TEXT NOT NULL,
    sensor INTEGER,
    FOREIGN KEY (user_button_customisation_id) REFERENCES User_Button_Customisations(button_id)
    FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id)
    );
    """)



cursor.execute("""
    CREATE TABLE axis
               
    """)
               

cursor.execute("""
    CREATE TABLE Thumbwheel (
        device_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        touch INTEGER NOT NULL,
        proxy INTEGER NOT NULL,
        single_tap INTEGER NOT NULL,
        divert INTEGER NOT NULL,
        invert INTEGER NOT NULL,
        left INTEGER NOT NULL,
        right INTEGER NOT NULL
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
""")


"""
Possible gesture modes:
    NoPress
    OnRelease
    OnInterval
    OnThreshold
    Axis
"""



"""
Possible action types:
    None
    Keypress
    Gestures
    ToggleSmartShift
    ToggleHiresScroll
    CycleDPI
"""