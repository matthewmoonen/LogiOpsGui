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
        -- scroll_left_action,
        -- scroll_right_action,
        -- proxy_action,
        -- tap_action,
        -- touch_action
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
        -- CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        -- CASE WHEN NEW.has_thumbwheel = 1 THEN 'Default' ELSE NULL END,
        -- CASE WHEN NEW.thumbwheel_proxy = 1 THEN 'Default' ELSE NULL END,
        -- CASE WHEN NEW.thumbwheel_tap = 1 THEN 'Default' ELSE NULL END,
        -- CASE WHEN NEW.thumbwheel_touch = 1 THEN 'Default' ELSE NULL END
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
CREATE TRIGGER IF NOT EXISTS add_button_configs
AFTER INSERT ON Configurations
FOR EACH ROW
BEGIN
    INSERT INTO ButtonConfigs (button_config_id, button_id, configuration_id)
    SELECT
        (SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1) + ROW_NUMBER() OVER (),
        b.button_id,
        NEW.configuration_id
    FROM Buttons AS b
    WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1;

    -- Update the next_source_key for the next use
    UPDATE SourceKeyGenerator SET next_source_key = next_source_key + (SELECT COUNT(*) FROM Buttons AS b WHERE b.device_id = NEW.device_id AND b.reprog = 1 AND b.accessible = 1) WHERE id = 1;
END;

-- ### QUERY_SEPARATOR ###
CREATE TRIGGER IF NOT EXISTS add_gesture_actions
AFTER INSERT ON ButtonConfigs
FOR EACH ROW
WHEN (SELECT gesture_support FROM Buttons WHERE button_id = NEW.button_id) = 1
BEGIN
    INSERT INTO Actions (configuration_id, source_id, action_type, is_selected)
    VALUES (NEW.configuration_id, NEW.button_config_id, 'Gestures', 0);
END;

-- CREATE TRIGGER IF NOT EXISTS add_gesture_destination_to_actions
-- AFTER INSERT ON Gestures
-- FOR EACH ROW
-- BEGIN
--     UPDATE Actions SET destination_id = NEW.gesture_id WHERE action_id = NEW.action_source_id;
-- END;


    -- WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    -- BEGIN
    --     INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Left');
    --     INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Right');
    -- END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_gestures_to_gestures
AFTER INSERT ON Actions
FOR EACH ROW
WHEN (NEW.action_type = 'Gestures')
BEGIN
    INSERT INTO Gestures (gesture_id, action_source_id, button_config_id, direction, threshold, mode)
    VALUES ((SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1), NEW.action_id, NEW.source_id, 'Up', 50, 'OnRelease');

    INSERT INTO Gestures (gesture_id, action_source_id, button_config_id, direction, threshold, mode)
    VALUES ((SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1), NEW.action_id, NEW.source_id, 'Down', 50, 'OnRelease');
    
    INSERT INTO Gestures (gesture_id, action_source_id, button_config_id, direction, threshold, mode)
    VALUES ((SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1), NEW.action_id, NEW.source_id, 'Left', 50, 'OnRelease');
    
    INSERT INTO Gestures (gesture_id, action_source_id, button_config_id, direction, threshold, mode)
    VALUES ((SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1), NEW.action_id, NEW.source_id, 'Right', 50, 'OnRelease');


    INSERT INTO Gestures (gesture_id, action_source_id, button_config_id, direction, threshold, mode)
    VALUES ((SELECT next_source_key FROM SourceKeyGenerator WHERE id = 1), NEW.action_id, NEW.source_id, 'None', 50, 'OnRelease');

END;



-- -- ### QUERY_SEPARATOR ###

-- CREATE TRIGGER IF NOT EXISTS add_gesture_destination_to_actions
-- AFTER INSERT ON Gestures
-- FOR EACH ROW
-- BEGIN
--     UPDATE Actions SET destination_id = NEW.gesture_id WHERE action_id = NEW.action_source_id;
-- END;


    -- WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    -- BEGIN
    --     INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Left');
    --     INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Right');
    -- END;




-- BEGIN

--     INSERT INTO Gestures (button_config_id, direction, threshold, mode)
--     SELECT NEW.button_config_id, 'Up', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Down', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Left', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Right', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'None', 50, 'OnRelease'
--     WHERE EXISTS (
--         SELECT 1 FROM Buttons AS b
--         WHERE b.button_id = NEW.button_id AND b.gesture_support = 1
--     );
-- END;





-- CREATE TRIGGER IF NOT EXISTS add_gestures_to_gestures
-- AFTER INSERT ON Actions

-- FOR EACH ROW
-- BEGIN
--     INSERT INTO Gestures (button_config_id, direction, threshold, mode)
--     SELECT NEW.button_config_id, 'Up', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Down', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Left', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Right', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'None', 50, 'OnRelease'
--     WHERE EXISTS (
--         SELECT 1 FROM Buttons AS b
--         WHERE b.button_id = NEW.button_id AND b.gesture_support = 1
--     );
-- END;





-- CREATE TRIGGER IF NOT EXISTS add_gestures_to_gestures
-- AFTER INSERT ON Actions
-- FOR EACH ROW
-- BEGIN
--     INSERT INTO Gestures (button_config_id, direction, threshold, mode)
--     SELECT NEW.button_config_id, 'Up', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Down', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Left', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'Right', 50, 'OnRelease'
--     UNION ALL SELECT NEW.button_config_id, 'None', 50, 'OnRelease'
--     WHERE EXISTS (
--         SELECT 1 FROM Buttons AS b
--         WHERE b.button_id = NEW.button_id AND b.gesture_support = 1
--     );
-- END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_scroll_columns_vertical
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT has_scrollwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN      
        -- Inserts columns for vertical scrollwheel
        INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Up');
        INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Down');
    END;





-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_scroll_columns_horizontal
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT has_thumbwheel FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Left');
        INSERT INTO ScrollActions (configuration_id, scroll_direction) VALUES (NEW.configuration_id, 'Right');
    END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_tap
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_tap FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy) VALUES (NEW.configuration_id, 'Tap');
    END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_touch
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_touch FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy) VALUES (NEW.configuration_id, 'Touch');
    END;


-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS add_thumbwheel_column_proxy
    AFTER INSERT ON Configurations
    FOR EACH ROW
    WHEN (SELECT thumbwheel_proxy FROM Devices WHERE device_id = NEW.device_id) = 1
    BEGIN
        INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy) VALUES (NEW.configuration_id, 'Proxy');
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

-- Trigger for inserting the current date and time on row insertion
CREATE TRIGGER IF NOT EXISTS configuration_insert_last_modified
AFTER INSERT ON Configurations
BEGIN
    UPDATE Configurations
    SET last_modified = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;


-- ### QUERY_SEPARATOR ###

-- Trigger for inserting the current date and time on row update
CREATE TRIGGER IF NOT EXISTS configuration_update_last_modified
AFTER UPDATE ON Configurations
BEGIN
    UPDATE Configurations
    SET last_modified = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;


-- ### QUERY_SEPARATOR ###

-- Trigger for inserting the current date and time on row insertion
CREATE TRIGGER IF NOT EXISTS configuration_insert_date_added
AFTER INSERT ON Configurations
BEGIN
    UPDATE Configurations
    SET date_added = DATETIME('now')
    WHERE configuration_id = NEW.configuration_id;
END;


-- ### QUERY_SEPARATOR ###

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

CREATE TRIGGER IF NOT EXISTS generate_button_config_source_key
BEFORE INSERT ON ButtonConfigs
FOR EACH ROW
BEGIN
    UPDATE SourceKeyGenerator
    SET next_source_key = next_source_key + 1
    WHERE id = 1;
END;



-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS generate_gestures_source_key
BEFORE INSERT ON Gestures
FOR EACH ROW
BEGIN
    UPDATE SourceKeyGenerator
    SET next_source_key = next_source_key + 1
    WHERE id = 1;
END;








-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS generate_axis_destination_key
BEFORE INSERT ON Axes
FOR EACH ROW
BEGIN
    UPDATE DestinationKeyGenerator
    SET next_destination_key = next_destination_key + 1
    WHERE id = 1;

    UPDATE Axes
    SET axis_id = (SELECT next_destination_key FROM DestinationKeyGenerator WHERE id = 1)
    WHERE rowid = NEW.rowid;
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS generate_cycle_dpi_destination_key
BEFORE INSERT ON CycleDPI
FOR EACH ROW
BEGIN
    UPDATE DestinationKeyGenerator
    SET next_destination_key = next_destination_key + 1
    WHERE id = 1;

    UPDATE CycleDPI
    SET cycle_dpi_id = (SELECT next_destination_key FROM DestinationKeyGenerator WHERE id = 1)
    WHERE rowid = NEW.rowid;
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS generate_keypress_destination_key
BEFORE INSERT ON Keypresses
FOR EACH ROW
BEGIN
    UPDATE DestinationKeyGenerator
    SET next_destination_key = next_destination_key + 1
    WHERE id = 1;

    UPDATE Keypresses
    SET keypress_id = (SELECT next_destination_key FROM DestinationKeyGenerator WHERE id = 1)
    WHERE rowid = NEW.rowid;
END;

-- ### QUERY_SEPARATOR ###

CREATE TRIGGER IF NOT EXISTS generate_changehost_destination_key
BEFORE INSERT ON ChangeHost
FOR EACH ROW
BEGIN
    UPDATE DestinationKeyGenerator
    SET next_destination_key = next_destination_key + 1
    WHERE id = 1;

    UPDATE ChangeHost
    SET host_id = (SELECT next_destination_key FROM DestinationKeyGenerator WHERE id = 1)
    WHERE rowid = NEW.rowid;
END;



