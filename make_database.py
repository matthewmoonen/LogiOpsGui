from LogitechDeviceData import logitech_devices, get_button_function






def add_devices(cursor):

    for device in logitech_devices:



        cursor.execute("""
                        INSERT INTO Devices (
                            device_id,
                            device_name,
                            is_user_device,
                            config_file_device_name,
                            device_pids,
                            min_dpi,
                            max_dpi,
                            default_dpi,
                            has_thumbwheel,
                            thumbwheel_tap,
                            thumbwheel_proxy,
                            thumbwheel_touch,
                            thumbwheel_timestamp,
                            smartshift_support,
                            hires_scroll_support,
                            number_of_sensors


                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                        
                        device.device_id,
                        device.device_name,
                        0,
                        device.config_file_device_name,
                        str(device.product_ids),
                        device.min_dpi,
                        device.max_dpi,
                        device.default_dpi,
                        device.thumbwheel.has_thumbwheel,
                        device.thumbwheel.tap,
                        device.thumbwheel.proxy, 
                        device.thumbwheel.touch, 
                        device.thumbwheel.timestamp,
                        device.smartshift_support, 
                        device.hires_scroll_support, 
                        device.number_of_sensors))
        
        for button in device.buttons:

            cursor.execute("""
                            INSERT INTO Buttons (
                                device_id,
                                button_cid,
                                button_name,
                                reprog,
                                fn_key,
                                mouse_key,
                                gesture_support,
                                accessible
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                            
                            device.device_id,
                            button.button_cid,
                            get_button_function(button.button_cid),
                            button.reprogrammable,
                            button.fn_key,
                            button.mouse_key,
                            button.gesture_support,
                            button.accessible))

create_tables = [


    """
        CREATE TABLE IF NOT EXISTS Devices (
            device_id INTEGER PRIMARY KEY,
            device_name TEXT NOT NULL,
            is_user_device INTEGER NOT NULL DEFAULT 0,
            config_file_device_name TEXT NOT NULL,
            device_pids TEXT NOT NULL,
            min_dpi INTEGER NOT NULL,
            max_dpi INTEGER NOT NULL,
            default_dpi INTEGER NOT NULL DEFAULT 1000,
            has_thumbwheel INTEGER NOT NULL CHECK (has_thumbwheel IN (0, 1)),
            thumbwheel_tap INTEGER,
            thumbwheel_proxy INTEGER,
            thumbwheel_touch INTEGER,
            thumbwheel_timestamp INTEGER,
            smartshift_support INTEGER NOT NULL DEFAULT 1,
            hires_scroll_support INTEGER NOT NULL DEFAULT 1,
            number_of_sensors INTEGER NOT NULL DEFAULT 1 CHECK (number_of_sensors >=1)
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS UserDevices (
            user_device_id INTEGER PRIMARY KEY,
            device_id INTEGER NOT NULL,
            date_added INTEGER NOT NULL,
            is_activated INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (device_id) REFERENCES Devices(device_id)
        );
    """,




    """
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
    """,


    """
        CREATE TABLE IF NOT EXISTS Configurations (
            configuration_id INTEGER PRIMARY KEY,
            user_device_id INTEGER NOT NULL,
            configuration_name TEXT NOT NULL,
            last_modified INTEGER NOT NULL,
            is_selected INTEGER NOT NULL CHECK (is_selected IN (0, 1)),
            smartshift_on INTEGER CHECK (smartshift_on IN (0, 1) OR smartshift_on IS NULL),
            smartshift_threshold INTEGER CHECK (smartshift_threshold BETWEEN 1 AND 255 OR smartshift_threshold IS NULL),
            default_smartshift_threshold INTEGER CHECK (default_smartshift_threshold BETWEEN 1 AND 255 OR default_smartshift_threshold IS NULL),
            hiresscroll_hires INTEGER CHECK (hiresscroll_hires IN (0, 1) OR hiresscroll_hires IS NULL),
            hiresscroll_invert INTEGER CHECK (hiresscroll_invert IN (0, 1 OR hiresscroll_invert IS NULL)),
            hiresscroll_target INTEGER CHECK (hiresscroll_target IN (0, 1) OR hiresscroll_target IS NULL),
            thumbwheel_divert INTEGER CHECK (thumbwheel_divert IN (0, 1) OR thumbwheel_divert IS NULL),
            thumbwheel_invert INTEGER CHECK (thumbwheel_invert IN (0, 1) OR thumbwheel_invert IS NULL),

        FOREIGN KEY (user_device_id) REFERENCES UserDevices(user_device_id) ON DELETE CASCADE
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS Gestures (
            gesture_id INTEGER PRIMARY KEY,
            button_config_id INTEGER NOT NULL,
            direction TEXT NOT NULL CHECK (direction IN ('Up', 'Down', 'Left', 'Right', 'None')),
            action TEXT NOT NULL CHECK (action IN ('None', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),
            threshold INTEGER NOT NULL DEFAULT 50,
            mode TEXT NOT NULL DEFAULT 'OnRelease' CHECK (mode IN ('OnRelease', 'OnInterval', 'OnThreshold', 'Axis', 'NoPress')),

        UNIQUE (button_config_id, direction),
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
        );
    """,



    """
        CREATE TABLE IF NOT EXISTS ScrollActions (
            scroll_action_id INTEGER PRIMARY KEY,
            configuration_id INTEGER NOT NULL,
            scroll_direction TEXT CHECK (scroll_direction IN ('Up', 'Down', 'Left', 'Right', 'touch', 'tap', 'proxy')),
            scroll_action TEXT CHECK (scroll_action in ('Default', 'None', 'Keypress', 'Axis', 'ToggleSmartShift', 'CycleDPI', 'ChangeHost')),
            threshold INTEGER NOT NULL DEFAULT 50,
            mode TEXT NOT NULL DEFAULT 'OnInterval' CHECK (mode IN ('OnInterval', 'OnThreshold', 'Axis', 'NoPress')),

        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
        UNIQUE (scroll_direction, configuration_id)
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS ButtonConfigs (
            button_config_id INTEGER PRIMARY KEY,
            button_id INTEGER NOT NULL,
            configuration_id INTEGER NOT NULL,
            action TEXT NOT NULL CHECK (action IN ('Default', 'None', 'Keypress', 'Axis', 'Gestures', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),

        FOREIGN KEY (button_id) REFERENCES Buttons(button_id) ON DELETE CASCADE,
        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS Axes (
            axis_id INTEGER PRIMARY KEY,
            configuration_id INTEGER,
            button_config_id INTEGER,
            gesture_id INTEGER,
            scroll_action_id INTEGER,
            axis_button TEXT NOT NULL,
            axix_multiplier REAL,

        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE,
        FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE,
        FOREIGN KEY (scroll_action_id) REFERENCES ScrollActions(scroll_action_id) ON DELETE CASCADE
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS CycleDPI (
            cycle_dpi_id INTEGER PRIMARY KEY,
	        configuration_id INTEGER,
        	button_config_id INTEGER,
        	scroll_action_id INTEGER,                           
            gesture_id INTEGER,
            dpi_array TEXT NOT NULL,
            sensor INTEGER,

        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
	    FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE,
	    FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE,
	    FOREIGN KEY (scroll_action_id) REFERENCES ScrollActions(scroll_action_id) ON DELETE CASCADE
        );
    """,

	
    """
        CREATE TABLE IF NOT EXISTS Keypresses (
            keypress_id INTEGER PRIMARY KEY,
            configuration_id INTEGER,
            button_config_id INTEGER,
            gesture_id INTEGER,
            scroll_action_id INTEGER,
            keypresses TEXT NOT NULL,

        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE,
        FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE,
        FOREIGN KEY (scroll_action_id) REFERENCES ScrollActions(scroll_action_id) ON DELETE CASCADE
        );
    """,


    """
        CREATE TABLE IF NOT EXISTS ChangeHost (
            host_id INTEGER PRIMARY KEY,
            configuration_id INTEGER,
            button_config_id INTEGER,
            gesture_id INTEGER,
            scroll_action_id INTEGER,
            host_change TEXT NOT NULL DEFAULT 'next' CHECK (host_change IN ('prev', 'next', '1', '2', '3')),
            
        FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
        FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE,
        FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE,
        FOREIGN KEY (scroll_action_id) REFERENCES ScrollActions(scroll_action_id) ON DELETE CASCADE
        );     
    """,


]




create_db_triggers = [


"""
CREATE TRIGGER after_userdevices_insert
AFTER INSERT ON UserDevices
FOR EACH ROW
BEGIN
    UPDATE Devices
    SET is_user_device = 1
    WHERE device_id = NEW.device_id;
END;


""",



"""
CREATE TRIGGER after_userdevices_delete
AFTER DELETE ON UserDevices
FOR EACH ROW
BEGIN
    UPDATE Devices
    SET is_user_device = 0
    WHERE device_id = OLD.device_id;
END;


""",




"""

CREATE TRIGGER add_scroll_columns_vertical
    AFTER INSERT ON Configurations
    FOR EACH ROW
    BEGIN      
        -- Inserts columns for vertical scrollwheel
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Up', 'Default');
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Down', 'Default');
    END;

""",


"""
CREATE TRIGGER add_scroll_columns_horizontal
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT has_thumbwheel FROM UserDevices WHERE user_device_id = NEW.user_device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Left', 'Default');
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Right', 'Default');
    END;

""",

"""
CREATE TRIGGER add_thumbwheel_column_tap
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_tap FROM UserDevices WHERE user_device_id = NEW.user_device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'tap', 'None');
    END;
""",

"""
CREATE TRIGGER add_thumbwheel_column_touch
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_touch FROM UserDevices WHERE user_device_id = NEW.user_device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'touch', 'None');
    END;
""",

"""
CREATE TRIGGER add_thumbwheel_column_proxy
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_proxy FROM UserDevices WHERE user_device_id = NEW.user_device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'proxy', 'None');
    END;
""",




]









create_db_triggers2 = [





    """
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
                   """,


    """
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
    """,








    """
        CREATE TRIGGER after_gesture_insert
        AFTER INSERT ON Gestures
        FOR EACH ROW
        BEGIN
            IF NEW.action = 'Keypress' THEN 
                INSERT INTO Keypresses (gesture_id) VALUES NEW.(gesture_id)
            ELSEIF NEW.action = 'Axis' THEN 
                INSERT INTO Axes (gesture_id) VALUES NEW.(gesture_id)
            ELSEIF NEW.action = 'CycleDPI' THEN 
                INSERT INTO CycleDPI (gesture_id) VALUES NEW.(gesture_id)
            ELSEIF NEW.action = 'ChangeHost' THEN 
                INSERT INTO ChangeHost (gesture_id) VALUES NEW.(gesture_id)
        END;
            """,



    """
        CREATE TRIGGER after_gesture_update
        AFTER UPDATE OF action ON Gestures
        FOR EACH ROW
        BEGIN
            CASE OLD.action
                WHEN 'Keypress' THEN
                   DELETE FROM Keypresses WHERE gesture_id = OLD.gesture_id;
                WHEN 'Axis' THEN
                   DELETE FROM Axes WHERE gesture_id = OLD.gesture_id;
                WHEN 'Axis' THEN
                   DELETE FROM Axes WHERE gesture_id = OLD.gesture_id;
                WHEN 'CycleDPI' THEN
                   DELETE FROM CycleDPI WHERE gesture_id = OLD.gesture_id;
                WHEN 'ChangeHost' THEN
                   DELETE FROM ChangeHost WHERE gesture_id = OLD.gesture_id;
            END CASE;
        END;
    """,







]