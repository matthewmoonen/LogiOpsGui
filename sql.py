import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("sql.db")
cursor = conn.cursor()



def create_app_tables():

    conn = sqlite3.connect("user_devices.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Devices (
            device_id INTEGER PRIMARY KEY,
            device_name TEXT NOT NULL,
            config_file_device_name TEXT NOT NULL,
            device_pid TEXT NOT NULL,
            has_thumbwheel INTEGER NOT NULL CHECK (has_thumbwheel IN (0, 1)),
            thumbwheel_tap INTEGER,
            thumbwheel_proxy INTEGER,
            thumbwheel_touch INTEGER,
            thumbwheel_timestamp INTEGER,
            date_added INTEGER NOT NULL,
            smartshift_support INTEGER NOT NULL DEFAULT 1,
            hires_scroll_support INTEGER NOT NULL DEFAULT 1,
            number_of_sensors INTEGER NOT NULL DEFAULT 1 CHECK (number_of_sensors >=1),
            is_activated INTEGER NOT NULL DEFAULT 1
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Buttons (
            button_id INTEGER PRIMARY KEY,
            device_id INTEGER NOT NULL,
            button_cid TEXT NOT NULL,
            button_name TEXT NOT NULL,
            reprog INTEGER NOT NULL CHECK (reprog IN (0, 1)),
            fn_key INTEGER NOT NULL CHECK (fn_key IN (0, 1)),
            mouse_key INTEGER NOT NULL CHECK (mouse_key IN (0, 1)),
            gesture_support INTEGER NOT NULL CHECK (gesture_support IN (0, 1)),
            accessible INTEGER NOT NULL DEFAULT 1 CHECK (accessible IN (0, 1)),
        FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Configurations (
            configuration_id INTEGER PRIMARY KEY,
            device_id INTEGER NOT NULL,
            configuration_name TEXT NOT NULL,
            last_modified INTEGER NOT NULL,
            is_selected INTEGER NOT NULL CHECK (is_selected IN (0, 1)),
            smartshift_on INTEGER CHECK (smartshift_on IN (0, 1) OR smartshift_on IS NULL),
            smartshift_threshold INTEGER CHECK (smartshift_threshold BETWEEN 1 AND 255 OR smartshift_threshold IS NULL),
            default_smartshift_threshold INTEGER CHECK (default_smartshift_threshold BETWEEN 1 AND 255 OR default_smartshift_threshold IS NULL),
            hiresscroll_hires INTEGER CHECK (hiresscroll_hires IN (0, 1) OR hiresscroll_hires IS NULL),
            hiresscroll_invert INTEGER CHECK (hiresscroll_invert IN (0, 1 OR hiresscroll_invert IS NULL)),
            hiresscroll_target INTEGER CHECK (hiresscroll_target IN (0, 1) OR hiresscroll_target IS NULL),
        FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
        );
    """)







    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ScrollActions (
            scroll_action_id INTEGER PRIMARY KEY,
            configuration_id INTEGER NOT NULL,
            scroll_direction TEXT CHECK (scroll_direction IN ('Up', 'Down', 'Left', 'Right', 'touch', 'tap', 'proxy'))
            scroll_action TEXT CHECK (scroll_action in ('Default', 'None', 'Keypress', 'Axis', 'ToggleSmartShift', 'CycleDPI', 'ChangeHost'))
        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
        UNIQUE (scroll_direction, configuration_id)
        );
    """)




    # Insert new rows into appropriate tables for scroll wheel up actions
    cursor.execute("""
        CREATE TRIGGER add_scrollwheel_columns
        AFTER INSERT ON Configurations
        FOR EACH ROW
        BEGIN
            INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Left', 'Default');
            INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Right', 'Default');
			
			DECLARE thumbwheel_proxy_value, thumbwheel_touch_value, thumbwheel_tap_value INTEGER;
			SELECT thumbwheel_proxy, thumbwheel_touch, thumbwheel_tap INTO thumbwheel_proxy_value, thumbwheel_touch_value, thumbwheel_tap_value
			FROM Devices
			WHERE device_id = NEW.device_id;
            
			IF thumbwheel_proxy_value = 1 THEN
				INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action)
					VALUES (NEW.configuration_id, 'proxy', 'None');
			END IF;
                   
			IF thumbwheel_touch_value = 1 THEN
                   INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action)
					VALUES (NEW.configuration_id, 'touch', 'None');
			END IF;
                   
            IF thumbwheel_tap_value = 1 THEN
				INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action)
					VALUES (NEW.configuration_id, 'tap', 'None');
			END IF;
		END;
""")



    # Insert new rows into appropriate tables for scroll wheel down actions
    cursor.execute("""
        CREATE TRIGGER after_configuration_scroll_down_change
        AFTER INSERT ON Configurations
        FOR EACH ROW
        BEGIN
            IF NEW.scroll_down_action = 'Keypress' THEN 
                INSERT INTO Keypresses (configuration_id) VALUES NEW.(configuration_id)
            ELSEIF NEW.scroll_down_action = 'Axis' THEN 
                INSERT INTO Axes (configuration_id) VALUES NEW.(configuration_id)
            ELSEIF NEW.scroll_down_action = 'CycleDPI' THEN 
                INSERT INTO CycleDPI (configuration_id) VALUES NEW.(configuration_id)
            ELSEIF NEW.scroll_down_action = 'ChangeHost' THEN 
                INSERT INTO ChangeHost (configuration_id) VALUES NEW.(configuration_id)
        END
                   """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ButtonConfigs (
            button_config_id INTEGER PRIMARY KEY,
            button_id INTEGER NOT NULL,
            configuration_id INTEGER NOT NULL,
            action TEXT NOT NULL CHECK (action IN ('Default', 'None', 'Keypress', 'Axis', 'Gestures', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),
        FOREIGN KEY (button_id) REFERENCES Buttons(button_id) ON DELETE CASCADE
        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
        );
    """)


    cursor.execute("""
        CREATE TRIGGER after_button_action_insert
        AFTER INSERT ON ButtonConfigs
        FOR EACH ROW
        BEGIN
            IF NEW.action = 'Keypress' THEN 
                INSERT INTO Keypresses (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'Gestures' THEN 
                INSERT INTO Gestures (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'Axis' THEN 
                INSERT INTO Axes (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'CycleDPI' THEN 
                INSERT INTO CycleDPI (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'ChangeHost' THEN 
                INSERT INTO ChangeHost (button_config_id) VALUES NEW.(button_config_id)
        END;
                   """)


    cursor.execute("""
        CREATE TRIGGER after_button_action_update
        AFTER UPDATE OF action ON ButtonConfigs
        FOR EACH ROW
        BEGIN
            CASE OLD.action
                WHEN 'Keypress' THEN
                   DELETE FROM Keypresses WHERE button_config_id = OLD.button_config_id;
                WHEN 'Axis' THEN
                   DELETE FROM Axes WHERE button_config_id = OLD.button_config_id;
                WHEN 'Gestures' THEN
                   DELETE FROM Gestures WHERE button_config_id = OLD.button_config_id;
                WHEN 'CycleDPI' THEN
                   DELETE FROM CycleDPI WHERE button_config_id = OLD.button_config_id;
                WHEN 'ChangeHost' THEN
                   DELETE FROM ChangeHost WHERE button_config_id = OLD.button_config_id;
            END CASE;
        END;
    """)





    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Gestures (
            gesture_id INTEGER PRIMARY KEY,
            button_config_id INTEGER NOT NULL,
            direction TEXT NOT NULL CHECK (direction IN ('Up', 'Down', 'Left', 'Right', 'None')),
            action TEXT NOT NULL CHECK (action IN ('None', 'Axis' 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),
            threshold INTEGER NOT NULL DEFAULT 50,
            mode TEXT NOT NULL DEFAULT 'OnRelease' (mode IN ('OnRelease', 'OnInterval', 'OnThreshold', 'Axis')),
        UNIQUE (button_config_id, direction)
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
        );
    """)


    cursor.execute("""
        CREATE TRIGGER after_gesture_insert
        AFTER INSERT ON Gestures
        FOR EACH ROW
        BEGIN
            IF NEW.action = 'Keypress' THEN 
                INSERT INTO Keypresses (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'Axis' THEN 
                INSERT INTO Axes (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'CycleDPI' THEN 
                INSERT INTO CycleDPI (button_config_id) VALUES NEW.(button_config_id)
            ELSEIF NEW.action = 'ChangeHost' THEN 
                INSERT INTO ChangeHost (button_config_id) VALUES NEW.(button_config_id)
        END;
            """)



    cursor.execute("""
        CREATE TRIGGER after_gesture_update
        AFTER UPDATE OF action ON Gestures
        FOR EACH ROW
        BEGIN
            CASE OLD.action
                WHEN 'Keypress' THEN
                   DELETE FROM Keypresses WHERE button_config_id = OLD.button_config_id;
                WHEN 'Axis' THEN
                   DELETE FROM Axes WHERE button_config_id = OLD.button_config_id;
                WHEN 'Axis' THEN
                   DELETE FROM Axes WHERE button_config_id = OLD.button_config_id;
                WHEN 'CycleDPI' THEN
                   DELETE FROM CycleDPI WHERE button_config_id = OLD.button_config_id;
                WHEN 'ChangeHost' THEN
                   DELETE FROM ChangeHost WHERE button_config_id = OLD.button_config_id;
            END CASE;
        END;
    """)






    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Axes (
            axis_id INTEGER PRIMARY KEY,
            configuration_id INTEGER NOT NULL,
            button_config_id INTEGER,
            gesture_id INTEGER,
            axis_button TEXT NOT NULL,
            axix_multiplier REAL
        FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE
        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
        );
    """)

















    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cycle_dpi (
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
        CREATE TABLE IF NOT EXISTS Thumbwheel (
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
        # Practice:
        # https://chat.openai.com/share/bfcb59f7-1945-4298-bea9-82d2574f51da


    # cursor.execute("""
                   
    #     CREATE TABLE Sportspeople (
    #         sportsperson_id INTEGER PRIMARY KEY,
    #         sportsperson_name TEXT,
    #         sport_name TEXT
    #     );

    #     CREATE TABLE RugbyLeague (
    #         league_player_id INTEGER PRIMARY KEY,
    #         sportsperson_id INTEGER NOT NULL,
    #         position TEXT,
    #         team TEXT
    #     FOREIGN KEY (sportsperson_id) REFERENCES Sportspeople(sportsperson_id)
    #     );
                      
    #     CREATE TABLE Boxing (
    #         boxer_id INTEGER PRIMARY KEY,
    #         sportsperson_id INTEGER NOT NULL,
    #         weight_class TEXT
    #     FOREIGN KEY (sportsperson_id) REFERENCES Sportspeople(sportsperson_id)
    #     );
                   
    #                """)

