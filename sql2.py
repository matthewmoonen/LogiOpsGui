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
    CREATE TABLE 
""")
















