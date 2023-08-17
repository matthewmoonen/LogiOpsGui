import re


class DeviceButton:
    def __init__(self, button_id, reprogrammable, fn_key, mouse_key, gesture_support, accessible):
        self.button_id = button_id
        self.reprogrammable=reprogrammable
        self.fn_key=fn_key
        self.mouse_key=mouse_key
        self.gesture_support = gesture_support
        self.accessible = accessible


class Device:
    def __init__(self, name, config_file_device_name, min_dpi=None, max_dpi=None, default_dpi=None, buttons=None, has_thumbwheel=None):
        self.name = name
        self.config_file_device_name=config_file_device_name
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.buttons = buttons
        self.has_thumbwheel = has_thumbwheel


    def generate_snake_name(self, name):
        # Replace spaces with underscores
        snake_name = name.replace(' ', '_')
        # Remove non-alphanumeric characters using regex
        snake_name = re.sub(r'\W+', '', snake_name)
        # Convert the string to lowercase
        snake_name = snake_name.lower()
        return snake_name

