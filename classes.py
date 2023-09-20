class Device:
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
        self.device_id = device_id
        self.device_name = device_name
        self._is_user_device = is_user_device
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


class DeviceConfig(Device):
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
                device_is_activated,
                configuration_id,
                dpi,
                smartshift_on,
                smartshift_threshold,
                smartshift_torque,
                hiresscroll_hires,
                hiresscroll_invert,
                hiresscroll_target,

                thumbwheel_divert,
                thumbwheel_invert,


                date_added,
                device_last_edited,

    ): 

        super().__init__(
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
                device_is_activated,
        )

        self._configuration_id = configuration_id
        self._dpi = dpi
        self._smartshift_on = smartshift_on
        self._smartshift_threshold = smartshift_threshold
        self._smartshift_torque = smartshift_torque
        self._hiresscroll_hires = hiresscroll_hires
        self._hiresscroll_invert = hiresscroll_invert
        self._hiresscroll_target = hiresscroll_target
        self._thumbwheel_divert = thumbwheel_divert
        self._thumbwheel_invert = thumbwheel_invert
        self._date_added = date_added
        self._device_last_edited = device_last_edited


class Button(Device):
    def __init__(
                    self,
                    button_id,
                    device_id, 
                    button_cid, 
                    button_name,
                    is_reprogrammable,
                    is_function_key,
                    is_mouse_key,
                    is_accessible,
                    gesture_support,
                    ):
        self.button_id, = button_id,
        self.device_id = device_id
        self.button_cid = button_cid
        self.button_name = button_name
        self.is_reprogrammable = is_reprogrammable
        self.is_function_key = is_function_key
        self.is_mouse_key = is_mouse_key
        self.is_accessible = is_accessible

        self.gesture_support = gesture_support


class ButtonSettings(Button):
    def __init__(
                    self,
                    button_id,
                    device_id,
                    button_cid, 
                    button_name,
                    gesture_support,
                    configuration_id,
                    gestures,
                    button_actions,

    ):
        super().__init__(
                    self,
                    button_id,
                    device_id, 
                    button_cid, 
                    button_name,
                    gesture_support,
        )
        
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



class SingleInstanceActions:
    def __init__(
            self,
            device_id,
            button_id,
            configuration_id,
            is_selected,
            action_type,
    ):
    # Actions that have no futher configuration other than on or off
    # Default
    # NoPress
    # ToggleSmartShift
    # ToggleHiresScroll
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected
        self.action_type = action_type





# TODO these subclasses of the above class if possible
class Keypress:
    def __init__(
        self,
        button_config_id,
        device_id,
        button_id,
        configuration_id,
        is_selected,
    ):
        self.button_config_id = button_config_id
        self.device_id = device_id
        self.button_id = button_id        
        self.configuration_id = configuration_id
        self.is_selected = is_selected


class Axis:
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

        