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
                    scroll_directions=None,
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

# class ScrollActions:
#     def __init__(self,
#                  config_id,
#                  scroll_action_id,
#                  scroll_direction,

#                  )
class UserDevices:
    def __init__(
        self,
        device_id,
        device_name,
        is_activated,
        configs
    ):
        self.device_id = device_id
        self.device_name = device_name
        self.is_activated = is_activated
        self.configs = configs


class UserConfigs:
    def __init__(self,
                 device_id,
                 config_id,
                 config_name,
                 is_selected,
                 ):
        self.device_id = device_id
        self.config_id = config_id
        self.config_name = config_name
        self.is_selected = is_selected




class ButtonConfig:
    def __init__(self,
                 button_config_id,
                 button_id,
                 config_id,
                 action,
                 button_cid,
                 button_name,
                 reprog,
                 fn_key,
                 mouse_key,
                 gesture_support,
                 accessible
                 ):
        self.button_config_id = button_config_id
        self.button_id = button_id
        self.config_id = config_id
        self.action = action
        self.button_cid = button_cid



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

