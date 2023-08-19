class DeviceConfig():
    def __init__(self,
                    device_id,
                    config_id,
                    config_name,
                    dpi=(1000),
                    user_device_id=None,
                    date_added=None,
                    is_activated=None,
                    last_modified=None,
                    is_selected=None,
                    smartshift_on=None,
                    smartshift_threshold=None,
                    default_smartshift_threshold=None,
                    hiresscroll_hires=None,
                    hiresscroll_invert=None,
                    hiresscroll_target=None,
                    thumbwheel_divert=None,
                    thumbwheel_invert=None,
                    scroll_direction_up_action=None,
                    scroll_direction_up_mode=None,
                    scroll_direction_up_threshold=None,
                    scroll_direction_down_action=None,
                    scroll_direction_down_mode=None,
                    scroll_direction_down_threshold=None,
                    scroll_direction_left_action=None,
                    scroll_direction_left_mode=None,
                    scroll_direction_left_threshold=None,
                    scroll_direction_right_action=None,
                    scroll_direction_right_mode=None,
                    scroll_direction_right_threshold=None,
                 ):
        
        self.device_id = device_id
        self.config_id = config_id
        self.config_name = config_name
        self.user_device_id = user_device_id
        self.date_added = date_added
        self.is_activated = is_activated
        self.last_modified = last_modified
        self.is_selected = is_selected
        self.smartshift_on = smartshift_on
        self.smartshift_threshold = smartshift_threshold
        self.default_smartshift_threshold = default_smartshift_threshold
        self.hiresscroll_hires = hiresscroll_hires
        self.hiresscroll_invert = hiresscroll_invert
        self.hiresscroll_target = hiresscroll_target
        self.thumbwheel_divert = thumbwheel_divert
        self.thumbwheel_invert = thumbwheel_invert



class ButtonConfig:
    def __init__(self, button_config_id, button_id, config_id, action):
        self.button_config_id = button_config_id
        self.button_id = button_id
        self.config_id = config_id
        self.action = action



class Keypress:
    def __init__(self, 
                 keypress_id, 
                 keypresses,
                 config_id=None, # TODO: double check whether none specification is appropriate here.
                 button_config_id=None,
                 gesture_id=None, 
                 scroll_action_id=None
                 ):
        self.keypress_id = keypress_id
        self.keypresses = keypresses
        self.config_id = config_id
        self.button_config_id = button_config_id
        self.gesture_id = gesture_id
        self.scroll_action_id = scroll_action_id

