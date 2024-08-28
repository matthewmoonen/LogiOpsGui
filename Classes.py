import button_cid_names


class DeviceID:
    def __init__(self, device_id):
        self.device_id = device_id

class Device(DeviceID):
    def __init__(self, device_id, device_name):
        DeviceID.__init__(self, device_id)
        self.device_name = device_name

class Button(DeviceID):
    def __init__(self, device_id, button_cid, button_name):
        DeviceID.__init__(self, device_id)
        self.button_cid = button_cid
        self.button_name = button_name

class ButtonProperties(Button):
    def __init__(
                    self,
                    button_cid, 
                    reprogrammable,
                    fn_key,
                    mouse_key,
                    gesture_support,
                    accessible,
                    button_name=None,
                    device_id=None,
                    ):
        Button.__init__(self, device_id, button_cid, button_name)
        self.reprogrammable = reprogrammable
        self.fn_key = fn_key
        self.mouse_key = mouse_key
        self.gesture_support = gesture_support
        self.accessible = accessible
        self.button_name = button_cid_names.names.get(button_cid, 'Button Name Undefined')


class DeviceProperties(Device):
    def __init__(
                self,
                device_id,
                device_name,
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
    ):
        super().__init__(
                device_id,
                device_name
                )

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

class DeviceDatabase(DeviceProperties):
    def __init__(
                self,
                device_id,
                device_name,
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
    ):
        super().__init__(
                device_id,
                device_name,
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
                number_of_sensors
                )
        self.config_file_device_name = config_file_device_name
        self.device_pids = device_pids


def main():
    pass

if __name__ == "__main__":
    main()




