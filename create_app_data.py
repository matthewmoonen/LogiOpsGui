import DeviceData
import logging
import os
import execute_db_queries
import sqlite3


def configure_logging():

    if not os.path.exists("app_data"):
        os.mkdir("app_data")

    logging.basicConfig(
        filename='app_data/error_log.txt',  # Log file name
        level=logging.DEBUG,       # Set the log level to ERROR
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def initialise_database():

    database_path = 'app_data/app_records.db'

    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        execute_db_queries.execute_queries(cursor, table_creation_queries)
        execute_db_queries.execute_queries(cursor, create_db_triggers)
        add_devices(cursor)

        conn.commit()
        conn.close()



def add_devices(cursor):
    try:
        for device in DeviceData.logitech_devices:



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
                                number_of_sensors,
                                has_scrollwheel


                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                            
                            device.device_id,
                            device.device_name,
                            0,
                            device.config_file_device_name,
                            str(device.device_pids),
                            device.min_dpi,
                            device.max_dpi,
                            device.default_dpi,
                            device.has_thumbwheel,
                            device.thumbwheel_tap_support,
                            device.thumbwheel_proxy_support,
                            device.thumbwheel_touch_support,
                            device.thumbwheel_timestamp_support,
                            device.smartshift_support, 
                            device.hires_scroll_support, 
                            device.number_of_sensors,
                            device.has_scrollwheel
                            ))
            
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
                                DeviceData.cid_button_functions.get(button.button_cid, "Unknown Button"),
                                button.reprogrammable,
                                button.fn_key,
                                button.mouse_key,
                                button.gesture_support,
                                button.accessible))

    except sqlite3.Error as e:
        logging.error(e)

table_creation_queries = [


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
            has_scrollwheel INTEGER NOT NULL CHECK (has_scrollwheel IN (0, 1)),
            has_thumbwheel INTEGER NOT NULL CHECK (has_thumbwheel IN (0, 1)),
            thumbwheel_tap INTEGER,
            thumbwheel_proxy INTEGER,
            thumbwheel_touch INTEGER,
            thumbwheel_timestamp INTEGER,
            smartshift_support INTEGER NOT NULL DEFAULT 1,
            hires_scroll_support INTEGER NOT NULL DEFAULT 1,
            number_of_sensors INTEGER NOT NULL DEFAULT 1 CHECK (number_of_sensors >=1),
            date_added TEXT,
            is_activated INTEGER NOT NULL DEFAULT 0,
            last_edited TEXT
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
            device_id INTEGER NOT NULL,
            configuration_name TEXT NOT NULL,
            date_added TEXT,
            last_modified TEXT,
            is_selected INTEGER NOT NULL CHECK (is_selected IN (0, 1)),
            smartshift_on INTEGER CHECK (smartshift_on IN (0, 1) OR smartshift_on IS NULL),
            -- Threshold or torque of 0 denotes smartshift support but deactivated. NULL = No smartshift support
            smartshift_threshold INTEGER CHECK (smartshift_threshold BETWEEN 0 AND 255 OR smartshift_threshold IS NULL), 
            smartshift_torque INTEGER CHECK (smartshift_torque BETWEEN 0 AND 255 OR smartshift_torque IS NULL),
            hiresscroll_hires INTEGER CHECK (hiresscroll_hires IN (0, 1) OR hiresscroll_hires IS NULL),
            hiresscroll_invert INTEGER CHECK (hiresscroll_invert IN (0, 1 OR hiresscroll_invert IS NULL)),
            hiresscroll_target INTEGER CHECK (hiresscroll_target IN (0, 1) OR hiresscroll_target IS NULL),
            thumbwheel_divert INTEGER CHECK (thumbwheel_divert IN (0, 1) OR thumbwheel_divert IS NULL),
            thumbwheel_invert INTEGER CHECK (thumbwheel_invert IN (0, 1) OR thumbwheel_invert IS NULL),
            scroll_up_action TEXT NOT NULL CHECK (scroll_up_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')) DEFAULT 'Default',
            scroll_down_action TEXT NOT NULL CHECK (scroll_down_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')) DEFAULT 'Default',
            scroll_left_action TEXT CHECK (scroll_left_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR scroll_left_action IS NULL) DEFAULT 'Default',
            scroll_right_action TEXT CHECK (scroll_right_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR scroll_right_action IS NULL) DEFAULT 'Default',
            proxy_action TEXT CHECK (proxy_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR proxy_action IS NULL) DEFAULT NULL,
            tap_action TEXT CHECK (tap_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR tap_action IS NULL) DEFAULT NULL,
            touch_action TEXT CHECK (touch_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR touch_action IS NULL) DEFAULT NULL,
        
        FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
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
            scroll_action TEXT CHECK (scroll_action in ('None', 'Keypress', 'Axis', 'ToggleSmartShift', 'CycleDPI', 'ChangeHost')),
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
            action TEXT NOT NULL CHECK (action IN ('Default', 'NoPress', 'Keypress', 'Axis', 'Gestures', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),

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


# TODO: Create a query for duplicating configs. 
    # - New ButtonConfigs will automatically propagate with default values, so need to create Python that forces copy of these
    # - New Gesture IDs will automatically propagate with default values, so as above
    # - Unique constraints prevent duplicate entries (good), so just need to get the values from the tables and duplicate them
    # OR COULD this be done somehow through triggers? Specify a way to denote a copy versus a new insertion, and then let 


create_db_triggers = [
    
]

create_db_triggers3 = [



"""
CREATE TRIGGER add_first_config
    AFTER INSERT ON Devices
    FOR EACH ROW
    WHEN NEW.is_user_device = 1
BEGIN
    INSERT INTO Configurations (
        device_id,
        configuration_name,
        last_modified,
        is_selected,
        smartshift_on,
        smartshift_threshold,
        smartshift_torque,
        hiresscroll_hires,
        hiresscroll_invert,
        hiresscroll_target,
        thumbwheel_divert,
        thumbwheel_invert,
        scroll_left_action,
        scroll_right_action,
        proxy_action,
        tap_action,
        touch_action
    )
    VALUES (
        NEW.device_id,
        (SELECT device_name FROM Devices WHERE device_id = NEW.device_id),
        NULL,  -- last_modified can be NULL
        1,     -- is_selected is 1
        CASE WHEN NEW.smartshift_support = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_proxy = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_tap = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_touch = 1 THEN 'Default' ELSE NULL END
    );
END
""",




"""
CREATE TRIGGER delete_config_on_is_user_device_update
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 1 AND NEW.is_user_device = 0
BEGIN
	DELETE FROM Configurations WHERE device_id = NEW.device_id;
END
""",

"""
CREATE TRIGGER update_config_on_is_user_device_change
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 0 AND NEW.is_user_device = 1
BEGIN
    INSERT INTO Configurations (
        device_id,
        configuration_name,
        last_modified,
        is_selected,
        smartshift_on,
        smartshift_threshold,
        smartshift_torque,
        hiresscroll_hires,
        hiresscroll_invert,
        hiresscroll_target,
        thumbwheel_divert,
        thumbwheel_invert,
        scroll_left_action,
        scroll_right_action,
        proxy_action,
        tap_action,
        touch_action
    )
    VALUES (
        NEW.device_id,
        (SELECT device_name FROM Devices WHERE device_id = NEW.device_id),
        NULL,  -- last_modified can be NULL
        1,     -- is_selected is 1
        CASE WHEN NEW.smartshift_support = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_proxy = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_tap = 1 THEN 'Default' ELSE NULL END,
        CASE WHEN NEW.thumbwheel_touch = 1 THEN 'Default' ELSE NULL END
    );
END
""",


"""

CREATE TRIGGER IF NOT EXISTS add_button_configs
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action)
    SELECT b.button_id, NEW.configuration_id, 'Default' 
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;
END;



CREATE TRIGGER IF NOT EXISTS add_gestures
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
BEGIN
    INSERT INTO Gestures (button_config_id, direction, action, threshold, mode)
    SELECT NEW.button_config_id, 'Up', 'None', 50, 'OnRelease'
    UNION ALL SELECT NEW.button_config_id, 'Down', 'None', 50, 'OnRelease'
    UNION ALL SELECT NEW.button_config_id, 'Left', 'None', 50, 'OnRelease'
    UNION ALL SELECT NEW.button_config_id, 'Right', 'None', 50, 'OnRelease'
    UNION ALL SELECT NEW.button_config_id, 'None', 'None', 50, 'OnRelease'
    WHERE EXISTS (
        SELECT 1 FROM Buttons AS b
        WHERE b.button_id = NEW.button_id AND b.gesture_support = 1
    );
END;

""",



"""

CREATE TRIGGER IF NOT EXISTS add_scroll_columns_vertical
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN      
        -- Inserts columns for vertical scrollwheel
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Up', 'None');
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Down', 'None');
    END;

""",


"""
CREATE TRIGGER IF NOT EXISTS add_scroll_columns_horizontal
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Left', 'None');
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'Right', 'None');
    END;

""",

"""
CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_tap
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'tap', 'None');
    END;
""",

"""
CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_touch
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'touch', 'None');
    END;
""",

"""
CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_proxy
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction, scroll_action) VALUES (NEW.configuration_id, 'proxy', 'None');
    END;
""",

"""
CREATE TRIGGER configuration_update_selected_after_delete
AFTER DELETE ON Configurations
BEGIN
    UPDATE Configurations
    SET is_selected = 1
    WHERE device_id = OLD.device_id
    AND configuration_id = (
        SELECT MAX(configuration_id)
        FROM Configurations
        WHERE device_id = OLD.device_id
    )
    AND NOT EXISTS (
        SELECT 1
        FROM Configurations
        WHERE device_id = OLD.device_id
        AND is_selected = 1
    );
END
""",

"""
CREATE TRIGGER configuration_update_selected_after_insert
AFTER INSERT ON Configurations
WHEN NEW.is_selected = 1
BEGIN
    UPDATE Configurations
    SET is_selected = 0
    WHERE device_id = NEW.device_id
        AND is_selected = 1
        AND configuration_id <> NEW.configuration_id;
END
""",


"""
CREATE TRIGGER configuration_update_selected_after_update
AFTER UPDATE ON Configurations
FOR EACH ROW
BEGIN
    SELECT COUNT(*) 
    FROM Configurations
    WHERE device_id = NEW.device_id
        AND is_selected = 1;
    UPDATE Configurations
    SET is_selected = CASE
        WHEN device_id = NEW.device_id AND configuration_id = NEW.configuration_id THEN 1
        ELSE 0
        END
    WHERE device_id = NEW.device_id
        AND is_selected = 1
        AND configuration_id <> NEW.configuration_id
        AND (
            SELECT COUNT(*) 
            FROM Configurations
            WHERE device_id = NEW.device_id
                AND is_selected = 1
        ) > 1;
END
""",



"""
-- Trigger for inserting the current date and time on row insertion
CREATE TRIGGER configuration_insert_last_modified
AFTER INSERT ON Configurations
BEGIN
    UPDATE Configurations
    SET last_modified = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;
""",

"""
-- Trigger for inserting the current date and time on row update
CREATE TRIGGER configuration_update_last_modified
AFTER UPDATE ON Configurations
BEGIN
    UPDATE Configurations
    SET last_modified = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;
""",

"""
-- Trigger for inserting the current date and time on row insertion
CREATE TRIGGER configuration_insert_date_added
AFTER INSERT ON Configurations
BEGIN
    UPDATE Configurations
    SET date_added = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;
""",






"""
-- Trigger for inserting the current date and time on device added to user devices
CREATE TRIGGER IF NOT EXISTS update_date_added_on_is_user_device_change
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 0 AND NEW.is_user_device = 1
BEGIN
    UPDATE Devices
    SET date_added = DATETIME('now')
    WHERE device_id = NEW.device_id;
END;
"""
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