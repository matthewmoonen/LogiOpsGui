-- -- Add new configuration to the Configurations table automatically when a new device is added.

CREATE TRIGGER IF NOT EXISTS add_first_config
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 0 AND NEW.is_user_device = 1 OR OLD.is_user_device = 1 AND NEW.is_user_device = 2
BEGIN
    INSERT INTO Configurations (
        device_id,
        configuration_name,
        -- date_added,
        -- last_modified,
        is_selected,


        smartshift_on,
        smartshift_threshold,
        smartshift_torque,
        hiresscroll_hires,
        hiresscroll_invert,
        hiresscroll_target,
        thumbwheel_divert,
        thumbwheel_invert
    )
    VALUES (
        NEW.device_id,
        (SELECT device_name FROM Devices WHERE device_id = NEW.device_id),
        -- CURRENT_TIMESTAMP,
        -- NULL,
        1,

        CASE WHEN NEW.smartshift_support = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 10 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 10 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END
    );
END;



-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS update_user_device
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 1 AND NEW.is_user_device = 2
BEGIN
    UPDATE Devices
    SET is_user_device = 1
    WHERE is_user_device = 2;
END;

-- ### QUERY_SEPARATOR ###


-- Creates a timestamp when a user adds a new device from the dropdown (so the most recently added devices can be displayed at the top)

CREATE TRIGGER IF NOT EXISTS add_date_added_for_new_device
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 0 AND NEW.is_user_device = 1
BEGIN
	UPDATE Devices
    SET date_added = CURRENT_TIMESTAMP
    WHERE device_id = NEW.device_id;
END;




-- ### QUERY_SEPARATOR ###

-- Delete all configurations associated with a device when a deletes it from their user device list

CREATE TRIGGER IF NOT EXISTS delete_config_on_is_user_device_update
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 1 AND NEW.is_user_device = 0
BEGIN
	DELETE FROM Configurations WHERE device_id = NEW.device_id;
END;



-- ### QUERY_SEPARATOR ###

-- Adds configuration options for each button for each newly added configuration.

CREATE TRIGGER add_button_configs
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'NoPress', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;

    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'ToggleSmartShift', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1;

    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'ToggleHiresScroll', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1;

    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'Gestures', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND b.gesture_support = 1;

    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, is_selected, device_id)
    SELECT b.button_id, NEW.configuration_id, 'Default', 1, NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;
END





-- ### QUERY_SEPARATOR ###

-- Adds the option for no action to happen when a user touches the thumbwheel for a newly added configuration. Set this automatically as the default selected option.

CREATE TRIGGER add_touch_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'NoPress', 1);
END


-- ### QUERY_SEPARATOR ###

-- Adds the option for touching the thumbwheel to toggle smartshift for a newly added configuration.

CREATE TRIGGER add_touch_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

-- Adds the option for touching the thumbwheel to toggle hires scroll for a newly added configuration.

CREATE TRIGGER add_touch_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'ToggleHiresScroll', 0);
END


-- ### QUERY_SEPARATOR ###

-- Adds the option for no action to happen when a user taps the thumbwheel for a newly added configuration. Set this automatically as the default selected option.

CREATE TRIGGER add_tap_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'NoPress', 1);
END



-- ### QUERY_SEPARATOR ###

-- Adds the option for tapping the thumbwheel to toggle smartshift for a newly added configuration.

CREATE TRIGGER add_tap_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

-- Adds the option for tapping the thumbwheel to toggle hires scroll for a newly added configuration.

CREATE TRIGGER add_tap_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'ToggleHiresScroll', 0);
END




-- ### QUERY_SEPARATOR ###

-- Adds the option for no action to happen when a user's thumb is within proximity of the thumbwheel for a newly added configuration. Set this automatically as the default selected option.

CREATE TRIGGER add_proxy_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'NoPress', 1);
END


-- ### QUERY_SEPARATOR ###

-- Adds the option to toggle smartshift for a newly added configuration when a user's thumb is near the thumbwheel.

CREATE TRIGGER add_proxy_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

-- Adds the option to toggle hires scroll for a newly added configuration when a user's thumb is near the thumbwheel.

CREATE TRIGGER add_proxy_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
AND (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'ToggleHiresScroll', 0);
END




-- ### QUERY_SEPARATOR ###



CREATE TRIGGER add_vertical_scroll_properties
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1

BEGIN
    INSERT INTO ScrollActionProperties (configuration_id, scroll_direction)
    VALUES
    (NEW.configuration_id, 'Down'),
    (NEW.configuration_id, 'Up');

END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_horizontal_scroll_properties
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActionProperties (configuration_id, scroll_direction)
    VALUES
    (NEW.configuration_id, 'Right'),
    (NEW.configuration_id, 'Left');
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_scroll_actions
AFTER INSERT ON ScrollActionProperties
FOR EACH ROW
BEGIN
    -- Insert default actions
    INSERT INTO ScrollActions (scroll_action_property_id, configuration_id, action_type, is_selected)
    VALUES
    (NEW.scroll_action_property_id, NEW.configuration_id, 'Default', 1),
    (NEW.scroll_action_property_id, NEW.configuration_id, 'NoPress', 0);

    -- Insert ToggleSmartShift action if smartshift_support is true
    INSERT INTO ScrollActions (scroll_action_property_id, configuration_id, action_type, is_selected)
    SELECT NEW.scroll_action_property_id, NEW.configuration_id, 'ToggleSmartShift', 0
    FROM Devices
    WHERE device_id = (SELECT Configurations.device_id FROM Configurations JOIN ScrollActionProperties ON Configurations.configuration_id = ScrollActionProperties.configuration_id WHERE ScrollActionProperties.scroll_action_property_id = NEW.scroll_action_property_id) AND smartshift_support = 1;

    -- Insert ToggleHiresScroll action if hires_scroll_support is true
    INSERT INTO ScrollActions (scroll_action_property_id, configuration_id, action_type, is_selected)
    SELECT NEW.scroll_action_property_id, NEW.configuration_id, 'ToggleHiresScroll', 0
    FROM Devices
    WHERE device_id = (SELECT Configurations.device_id FROM Configurations JOIN ScrollActionProperties ON Configurations.configuration_id = ScrollActionProperties.configuration_id WHERE ScrollActionProperties.scroll_action_property_id = NEW.scroll_action_property_id) AND hires_scroll_support = 1;
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_gesture_properties_and_null_selection
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, action_type, is_selected)
    VALUES
    (NEW.button_config_id, 'Up', 'NoPress', 1),
    (NEW.button_config_id, 'Down', 'NoPress', 1),
    (NEW.button_config_id, 'Left', 'NoPress', 1),
    (NEW.button_config_id, 'Right', 'NoPress', 1),
    (NEW.button_config_id, 'None', 'NoPress', 1);

    INSERT INTO GestureProperties(button_config_id, direction)
    VALUES
    (NEW.button_config_id, 'Up'),
    (NEW.button_config_id, 'Down'),
    (NEW.button_config_id, 'Left'),
    (NEW.button_config_id, 'Right'),
    (NEW.button_config_id, 'None');
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_smartshift_gesture_option
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, action_type, is_selected)
    VALUES
    (NEW.button_config_id, 'Up', 'ToggleSmartShift', 0),
    (NEW.button_config_id, 'Down', 'ToggleSmartShift', 0),
    (NEW.button_config_id, 'Left', 'ToggleSmartShift', 0),
    (NEW.button_config_id, 'Right', 'ToggleSmartShift', 0),
    (NEW.button_config_id, 'None', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_hires_scroll_gesture_option
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, action_type, is_selected)
    VALUES
    (NEW.button_config_id, 'Up', 'ToggleHiresScroll', 0),
    (NEW.button_config_id, 'Down', 'ToggleHiresScroll', 0),
    (NEW.button_config_id, 'Left', 'ToggleHiresScroll', 0),
    (NEW.button_config_id, 'Right', 'ToggleHiresScroll', 0),
    (NEW.button_config_id, 'None', 'ToggleHiresScroll', 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS gestures_update_selected_after_delete
AFTER DELETE ON Gestures
BEGIN
    UPDATE Gestures
    SET is_selected = 1
    WHERE button_config_id = OLD.button_config_id
    AND direction = OLD.direction
    AND action_type = "NoPress"
    AND OLD.is_selected = 1
    AND EXISTS (SELECT 1 FROM Gestures WHERE button_config_id = OLD.button_config_id AND direction = OLD.direction);
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS scroll_actions_update_selected_after_delete
AFTER DELETE ON ScrollActions
BEGIN
    UPDATE ScrollActions
    SET is_selected = 1
    WHERE scroll_action_property_id = OLD.scroll_action_property_id
    AND action_type = "Default"
    AND OLD.is_selected = 1
    AND EXISTS (SELECT 1 FROM ScrollActions WHERE scroll_action_property_id = OLD.scroll_action_property_id);
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS button_configs_update_selected_after_delete
AFTER DELETE ON ButtonConfigs
BEGIN
    UPDATE ButtonConfigs
    SET is_selected = 1
    WHERE configuration_id = OLD.configuration_id
    AND button_id = OLD.button_id
    AND action_type = "Default"
    AND OLD.is_selected = 1
    AND EXISTS (SELECT 1 FROM ButtonConfigs WHERE configuration_id = OLD.configuration_id AND button_id = OLD.button_id);
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS touch_tap_proxy_update_selected_after_delete
AFTER DELETE ON TouchTapProxy
BEGIN
    UPDATE TouchTapProxy
    SET is_selected = 1
    WHERE configuration_id = OLD.configuration_id
    AND touch_tap_proxy = OLD.touch_tap_proxy
    AND action_type = "NoPress"
    AND OLD.is_selected = 1
    AND EXISTS (SELECT 1 FROM TouchTapProxy WHERE configuration_id = OLD.configuration_id AND touch_tap_proxy = OLD.touch_tap_proxy);
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS configuration_update_selected_after_delete
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
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS configuration_update_selected_after_insert
AFTER INSERT ON Configurations
WHEN NEW.is_selected = 1
BEGIN
    UPDATE Configurations
    SET is_selected = 0
    WHERE device_id = NEW.device_id
        AND is_selected = 1
        AND configuration_id <> NEW.configuration_id;
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS configuration_update_selected_after_insert_where_not_secleted
AFTER INSERT ON Configurations
WHEN (SELECT COUNT(*) FROM Configurations WHERE device_id = NEW.device_id) = 1
BEGIN
    UPDATE Configurations
    SET is_selected = 1
    WHERE device_id = NEW.device_id;
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS configuration_update_selected_after_update
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
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS auto_insert_default_dpi
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    UPDATE Configurations
    SET dpi = (SELECT default_dpi FROM Devices WHERE device_id = NEW.device_id)
    WHERE configuration_id = NEW.configuration_id;
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS button_configs_update_selected_after_update
AFTER UPDATE ON ButtonConfigs
FOR EACH ROW
BEGIN
    UPDATE ButtonConfigs
    SET is_selected = CASE
        WHEN NEW.is_selected = 1 AND OLD.is_selected = 0 THEN 0
        ELSE is_selected
        END
    WHERE button_id = NEW.button_id
        AND configuration_id = NEW.configuration_id
        AND button_config_id != NEW.button_config_id;
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS getures_update_selected_after_update
AFTER UPDATE ON Gestures
FOR EACH ROW
BEGIN
    UPDATE Gestures
    SET is_selected = CASE
        WHEN NEW.is_selected = 1 AND OLD.is_selected = 0 THEN 0
        ELSE is_selected
        END
    WHERE button_config_id = NEW.button_config_id
        AND direction = NEW.direction
        AND gesture_id != NEW.gesture_id;
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS scroll_actions_update_selected_after_update
AFTER UPDATE ON ScrollActions
FOR EACH ROW
BEGIN
    UPDATE ScrollActions
    SET is_selected = CASE
        WHEN NEW.is_selected = 1 AND OLD.is_selected = 0 THEN 0
        ELSE is_selected
        END
    WHERE scroll_action_property_id = NEW.scroll_action_property_id
        AND scroll_action_id != NEW.scroll_action_id;
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS touch_tap_proxy_update_selected_after_update
AFTER UPDATE ON TouchTapProxy
FOR EACH ROW
BEGIN
    UPDATE TouchTapProxy
    SET is_selected = CASE
        WHEN NEW.is_selected = 1 AND OLD.is_selected = 0 THEN 0
        ELSE is_selected
        END
    WHERE configuration_id = NEW.configuration_id
        AND touch_tap_proxy = NEW.touch_tap_proxy
        AND touch_tap_proxy_id != NEW.touch_tap_proxy_id;
END;



-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_axis_from_button_config
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Axis'
BEGIN
    INSERT INTO Axes (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'ButtonConfigs');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_axis_from_gestures
AFTER INSERT ON Gestures
FOR EACH ROW
WHEN NEW.action_type = 'Axis'
BEGIN
    INSERT INTO Axes (configuration_id, action_id, source_table)
    VALUES ((SELECT configuration_id FROM ButtonConfigs WHERE button_config_id = NEW.button_config_id), NEW.gesture_id, 'Gestures');
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_axis_from_scroll_actions
AFTER INSERT ON ScrollActions
FOR EACH ROW
WHEN NEW.action_type = 'Axis'
BEGIN
    INSERT INTO Axes (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.scroll_action_id, 'ScrollActions');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_axis_from_touch_tap_proxy
AFTER INSERT ON TouchTapProxy
FOR EACH ROW
WHEN NEW.action_type = 'Axis'
BEGIN
    INSERT INTO Axes (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.touch_tap_proxy_id, 'TouchTapProxy');
END;




-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_keypress_from_button_config
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Keypress'
BEGIN
    INSERT INTO Keypresses (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'ButtonConfigs');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_keypress_from_gestures
AFTER INSERT ON Gestures
FOR EACH ROW
WHEN NEW.action_type = 'Keypress'
BEGIN
    INSERT INTO Keypresses (configuration_id, action_id, source_table)
    VALUES ((SELECT configuration_id FROM ButtonConfigs WHERE button_config_id = NEW.button_config_id), NEW.gesture_id, 'Gestures');
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_keypress_from_scroll_actions
AFTER INSERT ON ScrollActions
FOR EACH ROW
WHEN NEW.action_type = 'Keypress'
BEGIN
    INSERT INTO Keypresses (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.scroll_action_id, 'ScrollActions');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_keypress_from_touch_tap_proxy
AFTER INSERT ON TouchTapProxy
FOR EACH ROW
WHEN NEW.action_type = 'Keypress'
BEGIN
    INSERT INTO Keypresses (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.touch_tap_proxy_id, 'TouchTapProxy');
END;



-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_cycledpi_from_button_config
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'CycleDPI'
BEGIN
    INSERT INTO CycleDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'ButtonConfigs');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_cycledpi_from_gestures
AFTER INSERT ON Gestures
FOR EACH ROW
WHEN NEW.action_type = 'CycleDPI'
BEGIN
    INSERT INTO CycleDPI (configuration_id, action_id, source_table)
    VALUES ((SELECT configuration_id FROM ButtonConfigs WHERE button_config_id = NEW.button_config_id), NEW.gesture_id, 'Gestures');
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_cycledpi_from_scroll_actions
AFTER INSERT ON ScrollActions
FOR EACH ROW
WHEN NEW.action_type = 'CycleDPI'
BEGIN
    INSERT INTO CycleDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.scroll_action_id, 'ScrollActions');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_cycledpi_from_touch_tap_proxy
AFTER INSERT ON TouchTapProxy
FOR EACH ROW
WHEN NEW.action_type = 'CycleDPI'
BEGIN
    INSERT INTO CycleDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.touch_tap_proxy_id, 'TouchTapProxy');
END;



-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changedpi_from_button_config
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'ChangeDPI'
BEGIN
    INSERT INTO ChangeDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'ButtonConfigs');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changedpi_from_gestures
AFTER INSERT ON Gestures
FOR EACH ROW
WHEN NEW.action_type = 'ChangeDPI'
BEGIN
    INSERT INTO ChangeDPI (configuration_id, action_id, source_table)
    VALUES ((SELECT configuration_id FROM ButtonConfigs WHERE button_config_id = NEW.button_config_id), NEW.gesture_id, 'Gestures');
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changedpi_from_scroll_actions
AFTER INSERT ON ScrollActions
FOR EACH ROW
WHEN NEW.action_type = 'ChangeDPI'
BEGIN
    INSERT INTO ChangeDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.scroll_action_id, 'ScrollActions');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changedpi_from_touch_tap_proxy
AFTER INSERT ON TouchTapProxy
FOR EACH ROW
WHEN NEW.action_type = 'ChangeDPI'
BEGIN
    INSERT INTO ChangeDPI (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.touch_tap_proxy_id, 'TouchTapProxy');
END;




-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changehost_from_button_config
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'ChangeHost'
BEGIN
    INSERT INTO ChangeHost (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'ButtonConfigs');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changehost_from_gestures
AFTER INSERT ON Gestures
FOR EACH ROW
WHEN NEW.action_type = 'ChangeHost'
BEGIN
    INSERT INTO ChangeHost (configuration_id, action_id, source_table)
    VALUES ((SELECT configuration_id FROM ButtonConfigs WHERE button_config_id = NEW.button_config_id), NEW.gesture_id, 'Gestures');
END;


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changehost_from_scroll_actions
AFTER INSERT ON ScrollActions
FOR EACH ROW
WHEN NEW.action_type = 'ChangeHost'
BEGIN
    INSERT INTO ChangeHost (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.scroll_action_id, 'ScrollActions');
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS insert_changehost_from_touch_tap_proxy
AFTER INSERT ON TouchTapProxy
FOR EACH ROW
WHEN NEW.action_type = 'ChangeHost'
BEGIN
    INSERT INTO ChangeHost (configuration_id, action_id, source_table)
    VALUES (NEW.configuration_id, NEW.touch_tap_proxy_id, 'TouchTapProxy');
END;




-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_gesture_destination_axis
AFTER DELETE ON Gestures 
FOR EACH ROW
WHEN OLD.action_type = 'Axis'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.gesture_id AND source_table = 'Gestures';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_gesture_destination_keypress
AFTER DELETE ON Gestures
FOR EACH ROW
WHEN OLD.action_type = 'Keypress'
BEGIN
DELETE FROM Keypresses WHERE action_id = OLD.gesture_id AND source_table = 'Gestures';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_gesture_destination_cycledpi
AFTER DELETE ON Gestures
FOR EACH ROW
WHEN OLD.action_type = 'CycleDPI'
BEGIN
DELETE FROM CycleDPI WHERE action_id = OLD.gesture_id AND source_table = 'Gestures';
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_gesture_destination_changedpi
AFTER DELETE ON Gestures
FOR EACH ROW
WHEN OLD.action_type = 'ChangeDPI'
BEGIN
DELETE FROM ChangeDPI WHERE action_id = OLD.gesture_id AND source_table = 'Gestures';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_gesture_destination_changehost
AFTER DELETE ON Gestures
FOR EACH ROW
WHEN OLD.action_type = 'ChangeHost'
BEGIN
DELETE FROM ChangeHost WHERE action_id = OLD.gesture_id AND source_table = 'Gestures';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_button_config_destination_axes
AFTER DELETE ON ButtonConfigs 
FOR EACH ROW
WHEN OLD.action_type = 'Axis'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.button_config_id AND source_table = 'ButtonConfigs';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_button_config_destination_keypresses
AFTER DELETE ON ButtonConfigs 
FOR EACH ROW
WHEN OLD.action_type = 'Keypress'
BEGIN
DELETE FROM Keypresses WHERE action_id = OLD.button_config_id AND source_table = 'ButtonConfigs';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_button_config_destination_cycledpi
AFTER DELETE ON ButtonConfigs 
FOR EACH ROW
WHEN OLD.action_type = 'CycleDPI'
BEGIN
DELETE FROM CycleDPI WHERE action_id = OLD.button_config_id AND source_table = 'ButtonConfigs';
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_button_config_destination_changedpi
AFTER DELETE ON ButtonConfigs 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeDPI'
BEGIN
DELETE FROM ChangeDPI WHERE action_id = OLD.button_config_id AND source_table = 'ButtonConfigs';
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_button_config_destination_changehost
AFTER DELETE ON ButtonConfigs 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeHost'
BEGIN
DELETE FROM ChangeHost WHERE action_id = OLD.button_config_id AND source_table = 'ButtonConfigs';
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_axes
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'Axis'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_keypresses
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'Keypress'
BEGIN
DELETE FROM Keypresses WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_cycledpi
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'CycleDPI'
BEGIN
DELETE FROM CycleDPI WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_changedpi
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeDPI'
BEGIN
DELETE FROM ChangeDPI WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_changehost
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeHost'
BEGIN
DELETE FROM ChangeHost WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_scroll_action_destination_axes
AFTER DELETE ON ScrollActions 
FOR EACH ROW
WHEN OLD.action_type = 'ButtonConfigs'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.scroll_action_id AND source_table = 'ScrollActions';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_axes
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'Axis'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_keypresses
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'Keypress'
BEGIN
DELETE FROM Keypresses WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_cycledpi
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'CycleDPI'
BEGIN
DELETE FROM CycleDPI WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_changehost
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeHost'
BEGIN
DELETE FROM ChangeHost WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_changedpi
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'ChangeDPI'
BEGIN
DELETE FROM ChangeDPI WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS delete_touch_tap_proxy_action_destination_axes
AFTER DELETE ON TouchTapProxy 
FOR EACH ROW
WHEN OLD.action_type = 'ButtonConfigs'
BEGIN
DELETE FROM Axes WHERE action_id = OLD.touch_tap_proxy_id AND source_table = 'TouchTapProxy';
END;

-- -- ### QUERY_SEPARATOR ###
-- CREATE TRIGGER IF NOT EXISTS insert_date_on_scroll_action
-- AFTER INSERT ON ScrollActions
-- FOR EACH ROW
-- WHEN NEW.action_type IN ('Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')
-- BEGIN
--     UPDATE ScrollActions
--     SET date_added = CURRENT_TIMESTAMP
--     WHERE scroll_action_id = NEW.scroll_action_id;
-- END;

-- -- ### QUERY_SEPARATOR ###
-- CREATE TRIGGER IF NOT EXISTS insert_date_on_touch_tap_proxy
-- AFTER INSERT ON TouchTapProxy
-- FOR EACH ROW
-- WHEN NEW.action_type IN ('Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')
-- BEGIN
--     UPDATE TouchTapProxy
--     SET date_added = CURRENT_TIMESTAMP
--     WHERE touch_tap_proxy_id = NEW.touch_tap_proxy_id;
-- END;

-- -- ### QUERY_SEPARATOR ###
-- CREATE TRIGGER IF NOT EXISTS insert_date_on_button_configs
-- AFTER INSERT ON ButtonConfigs
-- FOR EACH ROW
-- WHEN NEW.action_type IN ('Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')
-- BEGIN
--     UPDATE ButtonConfigs
--     SET date_added = CURRENT_TIMESTAMP
--     WHERE button_config_id = NEW.button_config_id;
-- END;

-- -- ### QUERY_SEPARATOR ###
-- CREATE TRIGGER IF NOT EXISTS insert_date_on_gestures
-- AFTER INSERT ON Gestures
-- FOR EACH ROW
-- WHEN NEW.action_type IN ('Keypress', 'Axis', 'CycleDPI', 'ChangeDPI', 'ChangeHost')
-- BEGIN
--     UPDATE Gestures
--     SET date_added = CURRENT_TIMESTAMP
--     WHERE gesture_id = NEW.gesture_id;
-- END;