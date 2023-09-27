import execute_db_queries

class Device:
    def __init__(
        self,
        device_id,
        device_name,
    ):
        self.device_id = device_id
        self.device_name = device_name


class Configuration:
    def __init__(
            self,
            configuration_id,
            device_id,
            configuration_name,
            is_selected,
            date_configuration_added = None,
            date_configuration_last_modified = None,
    ):
        self.configuration_id = configuration_id
        self.device_id = device_id
        self.configuration_name = configuration_name
        self.is_selected = bool(is_selected)
        self.date_configuration_added = date_configuration_added
        self.date_configuration_last_modified = date_configuration_last_modified


class ConfigurationSettings(Configuration):
    def __init__(
            self,
            configuration_id,
            device_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,
            dpi,
            smartshift_on,
            smartshift_threshold,
            smartshift_torque,
            hiresscroll_hires,
            hiresscroll_invert,
            hiresscroll_targer,
            thumbwheel_divert,
            thumbwheel_invert
    ):
        super().__init__(
            configuration_id,
            device_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,        
        )
        self.dpi = dpi
        self.smartshift_on = smartshift_on
        self.smartshift_threshold = smartshift_threshold
        self.smartshift_torque = smartshift_torque
        self.hiresscroll_hires = hiresscroll_hires
        self.hiresscroll_invert = hiresscroll_invert
        self.hiresscroll_targer = hiresscroll_targer
        self.thumbwheel_divert = thumbwheel_divert
        self.thumbwheel_invert = thumbwheel_invert



def get_main_page_user_devices():
    conn, cursor = execute_db_queries.create_db_connection()

    cursor.execute("""
        SELECT device_id, device_name, is_activated
        FROM Devices
        WHERE is_user_device = 1
        ORDER BY date_added DESC
                   """)

    devices = cursor.fetchall()

    user_devices_objects = []
    for device in devices:
        device_id, device_name, is_activated = device
        
        cursor.execute("""
            SELECT configuration_id, configuration_name, is_selected
            FROM Configurations
            WHERE device_id = ?
            ORDER BY date_added DESC
        """, (device_id,))

        configs_data = cursor.fetchall()

        configs = []

        for config_data in configs_data:
        
            config_id, configuration_name, is_selected = config_data
        
            user_config = Configuration(config_id, device_id, configuration_name, is_selected)

            configs.append(user_config)


        user_device = UserDevice(device_id, device_name, is_activated, configs)
        user_devices_objects.append(user_device)

    execute_db_queries.close_without_committing_changes(conn)
    return user_devices_objects



class UserDevice(Device):
    def __init__(
      self,
      device_id,
      device_name,
      is_activated,
      configurations = None,
      date_device_added = None,
      date_device_last_edited = None,
    ):
        super().__init__(
            device_id,
            device_name,
    )
        self.is_activated = is_activated
        self.configurations = configurations
        self.date_device_added = date_device_added
        self.date_device_last_edited = date_device_last_edited


class DeviceProperties(Device):
    def __init__(
                self,
                device_id,
                device_name,
                is_user_device,
                buttons,
                min_dpi,
                max_dpi,
                default_dpi,
                has_scrollwheel,
                smartshift_support,
                hires_scroll_support,
                has_thumbwheel,
                thumbwheel_tap_support,
                thumbwheel_proxy_support,
                thumbwheel_touch_support,
                thumbwheel_timestamp_support,
                number_of_sensors,
                config_file_device_name,
                device_pids,
                device_is_activated,

    ):


        super().__init__(
                device_id,
                device_name,
                is_user_device)

        self.buttons = buttons
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.has_scrollwheel = has_scrollwheel
        self.smartshift_support = smartshift_support
        self.hires_scroll_support = hires_scroll_support
        self.has_thumbwheel = has_thumbwheel
        self.thumbwheel_tap_support = thumbwheel_tap_support
        self.thumbwheel_proxy_support = thumbwheel_proxy_support
        self.thumbwheel_touch_support = thumbwheel_touch_support
        self.thumbwheel_timestamp_support = thumbwheel_timestamp_support
        self.number_of_sensors = number_of_sensors
        self.config_file_device_name = config_file_device_name
        self.device_pids = device_pids
        self._device_is_activated = device_is_activated



class DeviceConfig(UserDevice, DeviceProperties, ConfigurationSettings):
    def __init__(
            self,
            device_id,
            device_name,
            is_user_device,
            date_device_added,
            date_device_last_edited,
            buttons,
            min_dpi,
            max_dpi,
            default_dpi,
            has_scrollwheel,
            smartshift_support,
            hires_scroll_support,
            has_thumbwheel,
            thumbwheel_tap_support,
            thumbwheel_proxy_support,
            thumbwheel_touch_support,
            thumbwheel_timestamp_support,
            number_of_sensors,
            device_is_activated,

            configuration_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,
            dpi,
            smartshift_on,
            smartshift_threshold,
            smartshift_torque,
            hiresscroll_hires,
            hiresscroll_invert,
            hiresscroll_target,
            thumbwheel_divert,
            thumbwheel_invert,
            config_file_device_name = None,
            device_pids = None,
    ): 

        super().__init__(
            device_id,
            device_name,
            is_user_device,
            date_device_added,
            date_device_last_edited,
            buttons,
            min_dpi,
            max_dpi,
            default_dpi,
            has_scrollwheel,
            smartshift_support,
            hires_scroll_support,
            has_thumbwheel,
            thumbwheel_tap_support,
            thumbwheel_proxy_support,
            thumbwheel_touch_support,
            thumbwheel_timestamp_support,
            number_of_sensors,
            device_is_activated,
            configuration_id,
            configuration_name,
            date_configuration_added,
            date_configuration_last_modified,
            is_selected,
            dpi,
            smartshift_on,
            smartshift_threshold,
            smartshift_torque,
            hiresscroll_hires,
            hiresscroll_invert,
            hiresscroll_target,
            thumbwheel_divert,
            thumbwheel_invert,
            )
        



class Button:
    def __init__(
                    self,
                    device_id,
                    button_cid, 
                    button_name,
                    ):
        self.device_id = device_id
        self.button_cid = button_cid
        self.button_name = button_name


class ButtonProperties(Button):
    def __init__(
                    self,
                    device_id,
                    button_cid, 
                    button_name,
                    is_reprogrammable,
                    is_function_key,
                    is_mouse_key,
                    gesture_support,
                    is_accessible,
                    button_id = None
                    ):
        super().__init__(
            device_id,
            button_cid,
            button_name
        )
        self.is_reprogrammable = is_reprogrammable
        self.is_function_key = is_function_key
        self.is_mouse_key = is_mouse_key
        self.gesture_support = gesture_support
        self.is_accessible = is_accessible


class ButtonSettings(Button):
    def __init__(
                    self,
                    device_id,
                    button_cid, 
                    button_name,
                    button_id,
                    gesture_support,
                    configuration_id,
                    gestures,
                    button_actions,
    ):
        super().__init__(
            device_id,
            button_cid,
            button_name,
            button_id
        )
        self.gesture_support = gesture_support
        self.configuration_id = configuration_id
        self.gestures = gestures
        self.button_actions = button_actions


class Gesture:
    def __init__(
            self,
            gesture_id,
            button_config_id,
            direction,
            gesture_action,
            gesture_mode,
            gesture_threshold

    ):
        self.gesture_id = gesture_id
        self.button_config_id = button_config_id
        self.direction = direction
        self.gesture_action = gesture_action
        self.gesture_mode = gesture_mode
        self.gesture_threshold = gesture_threshold



class Action:
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            origin,
            action_id,
            is_selected,
    ):
    # Actions that have no futher configuration other than on or off
    # Default
    # NoPress
    # ToggleSmartShift
    # ToggleHiresScroll
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.origin = origin
        self.action_id = action_id
        self.is_selected = is_selected

class DefaultAction(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )

class NoPress(Action):
    def __init__(
            self,
            device_id,


            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )

class ToggleSmartShift(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )



class ToggleHiresScroll(Action):
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
    ):
        super.__init__(
            device_id,
            button_id,
            configuration_id,
            is_selected
        )




# TODO these subclasses of the above class if possible
class Keypress(Action):
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_type,
        keypresses
    ):
        super().__init__(
            button_config_id,
            device_id,
            button_id,
            configuration_id,
            is_selected,
            action_type = "Keypresses"
        )
        self.action_type = action_type
        self.keypresses = keypresses


class Axis(Action):
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        axis_id,
        axis_button,
        axis_multiplier

    ):
        super().__init__(
            button_config_id,
            device_id,
            button_id,
            configuration_id,
            is_selected,
            action_type = "Keypresses"
        )
        self.action_type = action_type


        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected


        self.action_id = action_id
        self.axis_id = axis_id
        self.axis_button = axis_button
        self.axis_multiplier = axis_multiplier

class CycleDPI:
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        cycle_dpi_id,
        dpi_array,
        sensor

    ):
        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected

        self.action_id = action_id

        self.cycle_dpi_id = cycle_dpi_id
        self.dpi_array = dpi_array
        self.sensor = sensor



class ChangeHost:
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
        action_id,
        host_change

    ):
        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected

        self.action_id = action_id

        self.host_change = host_change

        