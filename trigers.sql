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






CREATE TRIGGER delete_config_on_is_user_device_update
    AFTER UPDATE ON Devices
    FOR EACH ROW
    WHEN OLD.is_user_device = 1 AND NEW.is_user_device = 0
BEGIN
	DELETE FROM Configurations WHERE device_id = NEW.device_id;
END



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



