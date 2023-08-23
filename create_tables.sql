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
    scroll_up_action TEXT NOT NULL CHECK (scroll_up_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')) DEFAULT 'Default',
    scroll_down_action TEXT NOT NULL CHECK (scroll_down_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')) DEFAULT 'Default',
    scroll_left_action TEXT CHECK (scroll_left_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR scroll_left_action IS NULL) DEFAULT 'Default',
    scroll_right_action TEXT CHECK (scroll_right_action IN ('Default', 'NoPress', 'AxisScroll', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR scroll_right_action IS NULL) DEFAULT 'Default',
    proxy_action TEXT CHECK (proxy_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR proxy_action IS NULL) DEFAULT NULL,
    tap_action TEXT CHECK (tap_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR tap_action IS NULL) DEFAULT NULL,
    touch_action TEXT CHECK (touch_action IN ('Default', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost') OR touch_action IS NULL) DEFAULT NULL,

FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ButtonConfigs (
    button_config_id INTEGER PRIMARY KEY,
    button_id INTEGER NOT NULL,
    configuration_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('Default', 'NoPress', 'Keypress', 'Axis', 'Gestures', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),

FOREIGN KEY (button_id) REFERENCES Buttons(button_id) ON DELETE CASCADE,
FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###

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


-- ### QUERY_SEPARATOR ###

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

