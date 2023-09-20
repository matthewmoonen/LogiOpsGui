UPDATE Devices SET is_user_device = 1 WHERE device_id = 4;
UPDATE Devices SET is_user_device = 1 WHERE device_id = 14;
INSERT INTO Configurations(device_id, configuration_name, is_selected, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert) VALUES (4, 'MX Master 3 1', 0, 1, 10, 10, 0, 0, 0, 0, 0);





INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type) VALUES (4, 31, 1, 'Axis');
INSERT INTO Gestures (button_config_id, direction, gesture_action) VALUES (39, 'Down', 'Axis');
INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type) VALUES (1, 'Down', 'Axis');
INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (1, 'Tap', 'Axis');

DELETE FROM Gestures WHERE gesture_action = 'Axis';
DELETE FROM ButtonConfigs WHERE action_type = 'Axis';
DELETE FROM ScrollActions WHERE action_type = 'Axis';
DELETE FROM TouchTapProxy WHERE action_type = 'Axis';



INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type) VALUES (4, 31, 1, 'CycleDPI');
INSERT INTO Gestures (button_config_id, direction, gesture_action) VALUES (39, 'Down', 'CycleDPI');
INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type) VALUES (1, 'Down', 'CycleDPI');
INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (1, 'Tap', 'CycleDPI');

DELETE FROM Gestures WHERE gesture_action = 'CycleDPI';
DELETE FROM ButtonConfigs WHERE action_type = 'CycleDPI';
DELETE FROM ScrollActions WHERE action_type = 'CycleDPI';
DELETE FROM TouchTapProxy WHERE action_type = 'CycleDPI';



INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type) VALUES (4, 31, 1, 'ChangeHost');
INSERT INTO Gestures (button_config_id, direction, gesture_action) VALUES (39, 'Down', 'ChangeHost');
INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type) VALUES (1, 'Down', 'ChangeHost');
INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (1, 'Tap', 'ChangeHost');

DELETE FROM Gestures WHERE gesture_action = 'ChangeHost';
DELETE FROM ButtonConfigs WHERE action_type = 'ChangeHost';
DELETE FROM ScrollActions WHERE action_type = 'ChangeHost';
DELETE FROM TouchTapProxy WHERE action_type = 'ChangeHost';



INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type) VALUES (4, 31, 1, 'Keypress');
INSERT INTO Gestures (button_config_id, direction, gesture_action) VALUES (39, 'Down', 'Keypress');
INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type) VALUES (1, 'Down', 'Keypress');
INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (1, 'Tap', 'Keypress');

DELETE FROM Gestures WHERE gesture_action = 'Keypress';
DELETE FROM ButtonConfigs WHERE action_type = 'Keypress';
DELETE FROM ScrollActions WHERE action_type = 'Keypress';
DELETE FROM TouchTapProxy WHERE action_type = 'Keypress';













UPDATE Devices SET is_user_device = 1 WHERE device_id = 4;
UPDATE Devices SET is_user_device = 1 WHERE device_id = 14;
INSERT INTO Configurations(device_id, configuration_name, is_selected, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert) VALUES (4, 'MX Master 3 1', 0, 1, 10, 10, 0, 0, 0, 0, 0);
INSERT INTO ButtonConfigs (device_id, button_id, configuration_id, action_type) VALUES (4, 31, 1, 'Axis');
INSERT INTO Gestures (button_config_id, direction, gesture_action) VALUES (39, 'Down', 'CycleDPI');
INSERT INTO ScrollActions (configuration_id, scroll_direction, action_type) VALUES (1, 'Down', 'ChangeHost');
INSERT INTO TouchTapProxy (configuration_id, touch_tap_proxy, action_type) VALUES (1, 'Tap', 'Keypress');

