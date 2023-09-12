CREATE TRIGGER IF NOT EXISTS add_first_config
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
        thumbwheel_invert
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
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END
    );
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS delete_config_on_is_user_device_update
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 1 AND NEW.is_user_device = 0
BEGIN
	DELETE FROM Configurations WHERE device_id = NEW.device_id;
END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS update_config_on_is_user_device_change
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
        thumbwheel_invert
    )
    VALUES (
        NEW.device_id,
        (SELECT device_name FROM Devices WHERE device_id = NEW.device_id),
        NULL,  -- last_modified can be NULL
        1,     -- is_selected is 1
        CASE WHEN NEW.smartshift_support = 1 THEN 1 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 10 ELSE NULL END,
        CASE WHEN NEW.smartshift_support = 1 THEN 10 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.hires_scroll_support = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END,
        CASE WHEN NEW.has_thumbwheel = 1 THEN 0 ELSE NULL END
    );
END;

-- ### QUERY_SEPARATOR ###


CREATE TRIGGER add_button_configs_default
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, is_selected, device_id)
    SELECT b.button_id, NEW.configuration_id, 'Default', 1, NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_button_configs_nopress
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'NoPress', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_button_configs_smartshift_toggle
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'ToggleSmartShift', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1;
END

-- ### QUERY_SEPARATOR ###


CREATE TRIGGER add_button_configs_hires_scroll_toggle
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'ToggleHiresScroll', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1;
END

-- ### QUERY_SEPARATOR ###



CREATE TRIGGER add_button_configs_gestures
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_id, configuration_id, action_type, device_id)
    SELECT b.button_id, NEW.configuration_id, 'Gestures', NEW.device_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1 AND b.gesture_support = 1;
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_touch_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'NoPress', 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_touch_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_touch_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Touch', 'ToggleHiresScroll', 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_tap_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'NoPress', 1);
END



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_tap_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_tap_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Tap', 'ToggleHiresScroll', 0);
END




-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_proxy_option_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'NoPress', 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_proxy_option_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'ToggleSmartShift', 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_proxy_option_toggle_hires_scroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Proxy', 'ToggleHiresScroll', 0);
END






-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_up_action_default
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Up', 0, 'Default', NULL, 1);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_down_action_default
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Down', 0, 'Default', NULL, 1);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_left_action_default
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Left', 0, 'Default', NULL, 1);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_right_action_default
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Right', 0, 'Default', NULL, 1);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_up_action_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Up', 0, 'NoPress', 'NoPress', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_down_action_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Down', 0, 'NoPress', 'NoPress', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_left_action_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Left', 0, 'NoPress', 'NoPress', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_right_action_do_nothing
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, threshold, action_type, mode, is_selected)
    VALUES (NEW.configuration_id, 'Right', 0, 'NoPress', 'NoPress', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_up_action_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Up', 'ToggleSmartShift', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_down_action_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Down', 'ToggleSmartShift', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_left_action_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Left', 'ToggleSmartShift', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_right_action_toggle_smartshift
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Right', 'ToggleSmartShift', 0);
END


-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_up_action_toggle_hiresscroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Up', 'ToggleHiresScroll', 0);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_down_action_toggle_hiresscroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Down', 'ToggleHiresScroll', 0);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_left_action_toggle_hiresscroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Left', 'ToggleHiresScroll', 0);
END

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER add_scroll_right_action_toggle_hiresscroll
AFTER INSERT ON Configurations
FOR EACH ROW
WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type, is_selected)
    VALUES (NEW.configuration_id, 'Right', 'ToggleHiresScroll', 0);
END



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_default_null_gesture_up
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, threshold, mode, is_selected)
    VALUES (NEW.button_config_id, 'Up', 'None', 0, NULL, 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_default_null_gesture_down
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, threshold, mode, is_selected)
    VALUES (NEW.button_config_id, 'Down', 'None', 0, NULL, 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_default_null_gesture_left
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, threshold, mode, is_selected)
    VALUES (NEW.button_config_id, 'Left', 'None', 0, NULL, 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_default_null_gesture_right
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, threshold, mode, is_selected)
    VALUES (NEW.button_config_id, 'Right', 'None', 0, NULL, 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_default_null_gesture_none
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures'
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, threshold, mode, is_selected)
    VALUES (NEW.button_config_id, 'None', 'None', 0, NULL, 1);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_smartshift_option_gesture_up
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Up', 'ToggleSmartShift', NULL, 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_smartshift_option_gesture_down
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Down', 'ToggleSmartShift', NULL, 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_smartshift_option_gesture_left
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Left', 'ToggleSmartShift', NULL, 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_smartshift_option_gesture_right
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Right', 'ToggleSmartShift', NULL, 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_smartshift_option_gesture_none
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT smartshift_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'None', 'ToggleSmartShift', NULL, 0);
END


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_hires_scroll_option_gesture_up
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Up', 'ToggleHiresScroll', NULL, 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_hires_scroll_option_gesture_down
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Down', 'ToggleHiresScroll', NULL, 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_hires_scroll_option_gesture_left
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Left', 'ToggleHiresScroll', NULL, 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_hires_scroll_option_gesture_right
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'Right', 'ToggleHiresScroll', NULL, 0);
END

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER add_hires_scroll_option_gesture_none
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN NEW.action_type = 'Gestures' AND (SELECT hires_scroll_support FROM Devices WHERE device_id = NEW.device_id) = 1
BEGIN
    INSERT INTO Gestures(button_config_id, direction, gesture_action, mode, is_selected)
    VALUES (NEW.button_config_id, 'None', 'ToggleHiresScroll', NULL, 0);
END









































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
