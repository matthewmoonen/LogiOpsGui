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

FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Gestures (
    gesture_id INTEGER PRIMARY KEY,
    button_config_id INTEGER,
    action_source_id INTEGER,
    action_destination_id INTEGER,
    direction TEXT NOT NULL CHECK (direction IN ('Up', 'Down', 'Left', 'Right', 'None')),
    -- gesture_action TEXT NOT NULL CHECK (gesture_action IN ('None', 'Axis', 'Keypress', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),
    threshold INTEGER NOT NULL DEFAULT 50,
    mode TEXT NOT NULL DEFAULT 'OnRelease' CHECK (mode IN ('OnRelease', 'OnInterval', 'OnThreshold', 'Axis', 'NoPress')),

-- UNIQUE (action_source_id, direction),
FOREIGN KEY (button_config_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE,
FOREIGN KEY (action_source_id) REFERENCES Actions(action_id) ON DELETE CASCADE,
FOREIGN KEY (action_destination_id) REFERENCES Actions(action_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ScrollActions (
    scroll_action_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    scroll_direction TEXT CHECK (scroll_direction IN ('Up', 'Down', 'Left', 'Right')),
    action_id INTEGER,
    threshold INTEGER NOT NULL DEFAULT 50,
    mode TEXT NOT NULL DEFAULT 'OnInterval' CHECK (mode IN ('OnInterval', 'OnThreshold', 'Axis', 'NoPress')),

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
UNIQUE (scroll_direction, configuration_id)
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS TouchTapProxy (
    touch_tap_proxy_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    touch_tap_proxy TEXT CHECK (touch_tap_proxy IN ('Touch', 'Tap', 'Proxy')),
    action_id INTEGER,
    -- touch_tap_proxy_action TEXT NOT NULL CHECK (action IN ('None', 'Keypress', 'Axis', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
UNIQUE (touch_tap_proxy, configuration_id)
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Actions (
    action_id INTEGER PRIMARY KEY,
    configuration_id INTEGER NOT NULL,
    source_id INTEGER,
    source_table TEXT CHECK (source_table IN ('ButtonConfigs', 'Gestures', 'ScrollActions', 'TouchTapProxy'))
    destination_id INTEGER,
    action_type TEXT NOT NULL CHECK (action_type IN ('Default', 'NoPress', 'Keypress', 'Axis', 'Gestures', 'ToggleSmartShift', 'ToggleHiresScroll', 'CycleDPI', 'ChangeHost')),
    is_selected INTEGER NOT NULL CHECK (is_selected IN (0,1)),

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
CHECK source_table <> action_type
-- FOREIGN KEY (source_id) REFERENCES ButtonConfigs(button_config_id) ON DELETE CASCADE
-- FOREIGN KEY (source_id) REFERENCES ScrollActions(scroll_action_id) ON DELETE CASCADE,
-- FOREIGN KEY (source_id) REFERENCES TouchTapProxy(touch_tap_proxy_id) ON DELETE CASCADE,
-- FOREIGN KEY (source_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE,
-- FOREIGN KEY (destination_id) REFERENCES Keypresses(keypress_id) ON DELETE CASCADE,
-- FOREIGN KEY (destination_id) REFERENCES Axes(axis_id) ON DELETE CASCADE,
-- FOREIGN KEY (destination_id) REFERENCES CycleDPI(cycle_dpi_id) ON DELETE CASCADE,
-- FOREIGN KEY (destination_id) REFERENCES ChangeHost(host_id) ON DELETE CASCADE

);



-- ### QUERY_SEPARATOR ###
CREATE TABLE IF NOT EXISTS SourceKeyGenerator (
    id INTEGER PRIMARY KEY,
    next_source_key INTEGER
);


-- ### QUERY_SEPARATOR ###
INSERT INTO SourceKeyGenerator (next_source_key)
SELECT 1
WHERE NOT EXISTS (SELECT 1 FROM SourceKeyGenerator);



-- ### QUERY_SEPARATOR ###
CREATE TABLE IF NOT EXISTS DestinationKeyGenerator (
    id INTEGER PRIMARY KEY,
    next_destination_key INTEGER
);


-- ### QUERY_SEPARATOR ###
INSERT INTO DestinationKeyGenerator (next_destination_key)
SELECT 1
WHERE NOT EXISTS (SELECT 1 FROM DestinationKeyGenerator);






-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ButtonConfigs (
    button_config_id INTEGER,
    button_id INTEGER NOT NULL,
    configuration_id INTEGER NOT NULL,
    destination_table TEXT CHECK (destination_table in ('Gestures', 'Actions'))
    -- action_id INTEGER,

FOREIGN KEY (button_id) REFERENCES Buttons(button_id) ON DELETE CASCADE,
FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE
-- FOREIGN KEY (action_id) REFERENCES Actions(action_id) 
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Axes (
    axis_id INTEGER PRIMARY KEY,
    configuration_id INTEGER,
    action_id INTEGER,
    axis_button TEXT NOT NULL,
    axis_multiplier REAL,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
FOREIGN KEY (action_id) REFERENCES Actions(action_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS CycleDPI (
    cycle_dpi_id INTEGER PRIMARY KEY,
    configuration_id INTEGER,
    action_id INTEGER,
    dpi_array TEXT NOT NULL,
    sensor INTEGER,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
FOREIGN KEY (action_id) REFERENCES Actions(action_id) ON DELETE CASCADE
);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS Keypresses (
    keypress_id INTEGER PRIMARY KEY,
    configuration_id INTEGER,
    action_id INTEGER,
    keypresses TEXT NOT NULL,

FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
FOREIGN KEY (action_id) REFERENCES Actions(action_id) ON DELETE CASCADE

);


-- ### QUERY_SEPARATOR ###

CREATE TABLE IF NOT EXISTS ChangeHost (
    host_id INTEGER PRIMARY KEY,
    configuration_id INTEGER,
    action_id INTEGER,
    host_change TEXT NOT NULL DEFAULT 'next' CHECK (host_change IN ('prev', 'next', '1', '2', '3')),
    
FOREIGN KEY (configuration_id) REFERENCES Configurations(configuration_id) ON DELETE CASCADE,
FOREIGN KEY (action_id) REFERENCES Actions(action_id) ON DELETE CASCADE

);     

