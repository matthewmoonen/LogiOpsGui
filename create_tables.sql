CREATE TABLE IF NOT EXISTS UserSettings(
    key TEXT PRIMARY KEY,
    value TEXT
);

-- ### QUERY_SEPARATOR ###

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
    smartshift_support INTEGER NOT NULL DEFAULT 1 CHECK (smartshift_support in (0,1)),
    hires_scroll_support INTEGER NOT NULL DEFAULT 1,
    number_of_sensors INTEGER NOT NULL DEFAULT 1 CHECK (number_of_sensors >=1),
    date_added TEXT,
    is_activated INTEGER NOT NULL DEFAULT 0,
    last_edited TEXT
);



-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###
    
CREATE TABLE IF NOT EXISTS Configurations (
    configuration_id INTEGER PRIMARY KEY,
    device_id INTEGER NOT NULL,
    configuration_name TEXT NOT NULL,
    date_added TEXT,
    last_modified TEXT,
    is_selected INTEGER NOT NULL CHECK (is_selected IN (0, 1)),
    dpi INTEGER,
    smartshift_on INTEGER CHECK (smartshift_on IN (0, 1) OR smartshift_on IS NULL),
    -- Threshold or torque of 0 denotes smartshift support but deactivated. NULL = No smartshift support
    smartshift_threshold INTEGER CHECK (smartshift_threshold BETWEEN 0 AND 255 OR smartshift_threshold IS NULL), 
    smartshift_torque INTEGER CHECK (smartshift_torque BETWEEN 0 AND 255 OR smartshift_torque IS NULL),
    hiresscroll_hires INTEGER CHECK (hiresscroll_hires IN (0, 1) OR hiresscroll_hires IS NULL),
    hiresscroll_invert INTEGER CHECK (hiresscroll_invert IN (0, 1 OR hiresscroll_invert IS NULL)),
    hiresscroll_target INTEGER CHECK (hiresscroll_target IN (0, 1) OR hiresscroll_target IS NULL),
    thumbwheel_divert INTEGER CHECK (thumbwheel_divert IN (0, 1) OR thumbwheel_divert IS NULL),
    thumbwheel_invert INTEGER CHECK (thumbwheel_invert IN (0, 1) OR thumbwheel_invert IS NULL),

FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
);

-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ScrollActions (
    scroll_action_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    scroll_direction TEXT NOT NULL CHECK (scroll_direction IN ('Up', 'Down', 'Left', 'Right')),
    action_type TEXT NOT NULL CHECK (action_type IN ('Default', 'NoPress', 'ToggleSmartShift', 'ToggleHiresScroll', 'Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')),
    is_selected INTEGER NOT NULL DEFAULT 0 CHECK (is_selected IN (0, 1)),
    date_added TEXT,
    last_edited TEXT,


FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);

-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ScrollActionProperties (
    scroll_action_property_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    scroll_direction TEXT CHECK (scroll_direction IN ('Up', 'Down', 'Left', 'Right')),
    threshold INTEGER NOT NULL DEFAULT 50,
    mode TEXT NOT NULL DEFAULT 'OnInterval' CHECK (mode IN ('OnInterval', 'OnThreshold')),

    FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS TouchTapProxy (
    touch_tap_proxy_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    touch_tap_proxy TEXT CHECK (touch_tap_proxy IN ('Touch', 'Tap', 'Proxy')),
    action_type TEXT NOT NULL CHECK (action_type IN ('NoPress', 'ToggleSmartShift', 'ToggleHiresScroll', 'Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')),
    -- action_id INTEGER,
    is_selected INTEGER NOT NULL DEFAULT 0 CHECK (is_selected IN (0, 1)),
    date_added TEXT,
    last_edited TEXT,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ButtonConfigs (
    button_config_id INTEGER PRIMARY KEY,
    device_id INTEGER NOT NULL,
    button_id INTEGER NOT NULL,
    configuration_id INTEGER NOT NULL,
    action_type TEXT NOT NULL CHECK (action_type IN ('Default', 'NoPress', 'ToggleSmartShift', 'ToggleHiresScroll', 'Gestures', 'Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')),
    is_selected INTEGER NOT NULL DEFAULT 0 CHECK (is_selected IN (0,1)),
    date_added TEXT,
    last_edited TEXT,

FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE,
FOREIGN KEY (button_id) REFERENCES Buttons(button_id) ON DELETE CASCADE,
FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);





-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Gestures (
    gesture_id INTEGER PRIMARY KEY,
    button_config_id INTEGER NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('Up', 'Down', 'Left', 'Right', 'None')),
    gesture_action TEXT NOT NULL CHECK (gesture_action IN ('NoPress', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeDPI', 'ChangeHost')),
    is_selected INTEGER NOT NULL DEFAULT 0 CHECK (is_selected IN (0,1)),

    FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
);

-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS GestureProperties (
    gesture_property_id INTEGER PRIMARY KEY,
    button_config_id INTEGER NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('Up', 'Down', 'Left', 'Right', 'None')),
    threshold INTEGER NOT NULL DEFAULT 50,
    mode TEXT NOT NULL DEFAULT 'OnRelease' CHECK (mode IN ('OnRelease', 'OnInterval', 'OnThreshold', 'Axis', 'NoPress')),

    FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
);



-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Axes (
    axis_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    source_table TEXT NOT NULL CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy')),
    axis_button TEXT,
    axis_multiplier REAL,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS CycleDPI (
    cycle_dpi_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    source_table TEXT NOT NULL CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy')),
    dpi_array TEXT,
    sensor INTEGER,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ChangeDPI (
    change_dpi_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    source_table TEXT NOT NULL CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy')),
    increment INTEGER, 

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Keypresses (
    keypress_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    source_table TEXT NOT NULL CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy')),
    keypresses TEXT,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);





-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ChangeHost (
    host_id INTEGER PRIMARY KEY,
    configuration_id INTEGER,
    action_id INTEGER,
    source_table TEXT NOT NULL CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy')),
    host_change TEXT DEFAULT 'next' CHECK (host_change IN ('prev', 'next', '1', '2', '3')),
    
FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


