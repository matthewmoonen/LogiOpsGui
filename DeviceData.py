

class Device:
    def __init__(
                self,
                device_id,
                device_name,
                config_file_device_name,
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
        self.device_id = device_id
        self.device_name = device_name
        self.config_file_device_name = config_file_device_name
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


class InitialiseDatabase(Device):
    def __init__(
                    self,
                    device_id,
                    device_name,
                    config_file_device_name,
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
                    buttons = [],
                    device_pids = None
    ):
        super().__init__(
            device_id,
            device_name,
            config_file_device_name,
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
        )
        self.buttons = buttons
        self.device_pids = device_pids


class EditPageDevice(Device):
    def __init__(
                self,
                device_id,
                device_name,
                config_file_device_name,
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
                is_user_device,
                date_added=None,
                is_activated=None,
                last_edited=None,
                configurations=None
    ):
        super().__init__(
            device_id,
            device_name,
            config_file_device_name,
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
        )
        self._is_user_device = is_user_device
        self._date_added = date_added
        self._is_activated = is_activated
        self._last_edited = last_edited
        self._configurations = configurations

    @property
    def is_user_device(self):
        if isinstance(self._is_user_device, bool):
            return self._is_user_device
        else:
            raise ValueError("is_user_device must be a bool")

    @property
    def date_added(self):
        return self._date_added
        
    @property
    def is_activated(self):
        return self._is_activated
    
    @property
    def last_edited(self):
        return self._last_edited
    
    @property
    def configurations(self):
        if isinstance(self._configurations, list) and len(self._configurations) >= 1: 
            return self._configurations
        else:
            raise ValueError("Configurations must be an array and cannot be empty")


class DeviceConfig:
    def __init__(self,
                 configuration_id,
                 configuration_name,
                 dpi,
                 date_added,
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
                 scroll_up_action,
                 scroll_down_action,
                 scroll_left_action,
                 scroll_right_action,
                 proxy_action,
                 tap_action,
                 touch_action):
        
        self.configuration_id = configuration_id
        self.configuration_name = configuration_name
        self.dpi = dpi
        self.date_added = date_added
        self.last_modified = last_modified
        self.is_selected = is_selected
        self.smartshift_on = smartshift_on
        self.smartshift_threshold = smartshift_threshold
        self.smartshift_torque = smartshift_torque
        self.hiresscroll_hires = hiresscroll_hires
        self.hiresscroll_invert = hiresscroll_invert
        self.hiresscroll_target = hiresscroll_target
        self.thumbwheel_divert = thumbwheel_divert
        self.thumbwheel_invert = thumbwheel_invert
        self.scroll_up_action = scroll_up_action
        self.scroll_down_action = scroll_down_action
        self.scroll_left_action = scroll_left_action
        self.scroll_right_action = scroll_right_action
        self.proxy_action = proxy_action
        self.tap_action = tap_action
        self.touch_action = touch_action




class MainPageDevice(Device):
    def __init__(
                self,
                device_id,
                device_name,
                config_file_device_name,
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
                is_user_device,
                date_added=None,
                is_activated=None,
                last_edited=None,
                configurations=None
    ):
        super().__init__(
            device_id,
            device_name,
            config_file_device_name,
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
        )
        self._is_user_device = is_user_device
        self._date_added = date_added
        self._is_activated = is_activated
        self._last_edited = last_edited
        self._configurations = configurations

    @property
    def is_user_device(self):
        if isinstance(self._is_user_device, bool):
            return self._is_user_device
        else:
            raise ValueError("is_user_device must be a bool")

    @property
    def date_added(self):
        return self._date_added
        
    @property
    def is_activated(self):
        return self._is_activated
    
    @property
    def last_edited(self):
        return self._last_edited
    
    @property
    def configurations(self):
        return self._configurations
        # if isinstance(self._configurations, list) and len(self._configurations) >= 1: 
        # else:
        #     raise ValueError("Configurations must be an array and cannot be empty")




class DeviceButton:
    def __init__(
                    self,
                    device_id, 
                    button_cid, 
                    button_name,
                    gesture_support, 
                    ):
        self.device_id = device_id
        self.button_cid = button_cid
        self.button_name = button_name
        self.gesture_support = gesture_support
 

# TODO: a better name for this class.
class InitialiseButtonsDatabase(DeviceButton):
    def __init__(
        self,
        button_cid, 
        gesture_support, 
        reprogrammable, 
        fn_key, 
        mouse_key, 
        accessible, 
        device_id=None,
        button_name=None,
        ):
        super().__init__(
            device_id,
            button_cid,
            button_name,
            gesture_support,
    )
        self.reprogrammable = reprogrammable
        self.fn_key = fn_key
        self.mouse_key = mouse_key
        self.accessible = accessible

class ButtonConfig(InitialiseButtonsDatabase):
    def __init__(
            self,
            device_id,
            button_cid,
            button_name,
            gesture_support,
            button_id,
            configuration_id,
            button_config_id,
            button_action,
    ):
       super().__init__(
           device_id,
           button_cid,
           button_name,
           gesture_support
       )
       self.button_id = button_id
       self.configuration_id = configuration_id
       self.button_config_id = button_config_id
       self.button_action = button_action




#   Accessible refers to whether the button is physically accessible on the mouse when in normal use.
#   For example, 0x00d7 is normally the control ID for the button to switch between host devices/computers, and theoretically has gesture support.
#   However it is usually located on the bottom of the mouse. 

# Creating instances of LogitechDevice for each device
logitech_devices = [ 

InitialiseDatabase(
device_id = 1,
device_name = "MX Master 3S for Mac",
config_file_device_name = "MX Master 3S for Mac",
min_dpi = 200,
max_dpi = 8000,
default_dpi = 1000,
has_scrollwheel=True,
buttons = [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],
has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support = True,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-006574"
],
),


InitialiseDatabase(
device_id = 2,
device_name = "MX Master 3S",
config_file_device_name = "MX Master 3S",

min_dpi = 200,
max_dpi = 8000,
default_dpi =              1000, 
has_scrollwheel=True,

buttons =      [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support= True,
hires_scroll_support =      True,
number_of_sensors = 1,
device_pids = [
"910-006561", # Graphite
"910-006562" # Pale Gray
],
),


InitialiseDatabase(
device_id = 3,
device_name = "MX Master 3 for Mac",
config_file_device_name = "MX Master 3 for Mac",

min_dpi =   200,
max_dpi =   4000,
default_dpi =         1000,
has_scrollwheel=True,

buttons =     [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support=   True,
hires_scroll_support =    True,
number_of_sensors = 1,

device_pids = [
"910-005696",
],


),


InitialiseDatabase(
device_id = 4,
device_name = "MX Master 3",
config_file_device_name = "Wireless Mouse MX Master 3",


min_dpi =  200, 
max_dpi = 4000,
default_dpi =           1000,
has_scrollwheel=True,

buttons =      [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support=        True,
hires_scroll_support =       True,
number_of_sensors = 1,
device_pids = [
"910-005620"
],


),

InitialiseDatabase(
device_id = 5,
device_name = "MX Master 2S",
config_file_device_name = "Wireless Mouse MX Master 2S",


min_dpi =  200, 
max_dpi =4000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =      [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support=       True,
hires_scroll_support =  True,
number_of_sensors = 1,

device_pids = [
"910-005131"
],

),    

InitialiseDatabase(
device_id = 6,
device_name = "MX Master",
config_file_device_name = "Wireless Mouse MX Master",


min_dpi =  400,
max_dpi = 1600,
default_dpi = 1000,
has_scrollwheel=True,

buttons =     [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = True,
thumbwheel_tap_support = True,
thumbwheel_proxy_support = True,
thumbwheel_touch_support = True,
thumbwheel_timestamp_support = True,
smartshift_support=      True,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-004337",
],


),    

InitialiseDatabase(
device_id = 7,
device_name = "MX Anywhere 3S",
config_file_device_name = "MX Anywhere 3S",


min_dpi =  200,
max_dpi = 8000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =         [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
], 

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=     True,
hires_scroll_support = True,
number_of_sensors = 1,


device_pids = [
"910-006932", # Graphite
"910-006933", # Pale Grey
"910-006934" # Rose
],
),

InitialiseDatabase(
device_id = 8,
device_name = "MX Anywhere 3",
config_file_device_name = "MX Anywhere 3",

min_dpi =  200, 
max_dpi = 4000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =       [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
], 

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=    True,
hires_scroll_support = True,
number_of_sensors = 1,

device_pids = [
"910-005987"
],


),

InitialiseDatabase(
device_id = 9,
device_name = "MX Anywhere 2", 
config_file_device_name = "Wireless Mouse MX Anywhere 2",   


min_dpi =   400,
max_dpi = 1600, 
default_dpi = 1000,
has_scrollwheel=True,

buttons =      [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
], 

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=    False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-004373"
],


),

InitialiseDatabase(
device_id = 10,
device_name = "MX Anywhere 2S",
config_file_device_name = "Wireless Mobile Mouse MX Anywhere 2S",

min_dpi =   200, max_dpi = 4000, default_dpi =1000,
has_scrollwheel=True,

buttons =       [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
], 

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=        True,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-005132"
],



),

InitialiseDatabase(
device_id = 11,
device_name = "MX Vertical", 
config_file_device_name = "MX Vertical Advanced Ergonomic Mouse",


min_dpi =   400, max_dpi = 4000, default_dpi =1000,
has_scrollwheel=True,

buttons =    [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00fd", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
],

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=             False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-005447"
],


),

InitialiseDatabase(
device_id = 12,
device_name = "MX Ergo", 
config_file_device_name = "MX Ergo Multi-Device Trackball",

min_dpi =   512, max_dpi = 2048, default_dpi = 1000,
has_scrollwheel=True,

buttons =    [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00ed", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True), # TODO: Get confirmation that this is correct for this button

],

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=           False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-005177"
],



),

InitialiseDatabase(
device_id = 13,
device_name = "MX Ergo M575",
config_file_device_name = "ERGO M575 Trackball",


min_dpi =    400, max_dpi = 2000, default_dpi =1000,
has_scrollwheel=True,

buttons =    [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True), # TODO: are there any more buttons on this mouse?
],

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=            False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-005294"
],



),

InitialiseDatabase(
device_id = 14,
device_name = "M720 Triathlon", 
config_file_device_name = "M720 Triathlon Multi-Device Mouse",

min_dpi =    200, max_dpi = 3200,default_dpi = 1000,
has_scrollwheel=True,

buttons =    [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d0", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False), # TODO: Check accessibility!
],

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=     False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-004791"
],



),

InitialiseDatabase(
device_id = 15,
device_name = "M585/M590", 
config_file_device_name = "M585/M590 Multi-Device Mouse",

min_dpi =        1000, max_dpi = 2000,default_dpi = 1000, 
has_scrollwheel=True,

buttons =    [
InitialiseButtonsDatabase(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
InitialiseButtonsDatabase(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
],

has_thumbwheel = False,
thumbwheel_tap_support = None,
thumbwheel_proxy_support = None,
thumbwheel_touch_support = None,
thumbwheel_timestamp_support = None,
smartshift_support=     False,
hires_scroll_support = True,
number_of_sensors = 1,
device_pids = [
"910-005012",
"910-005197"
],


),

]


# TODO UPDATE THE ONE OR TWO EXCEPTIONS TO THE RULES HERE.
cid_button_functions = {
    "0x0050": "Left Mouse Button",
    "0x0051": "Right Mouse Button",
    "0x0052": "Middle Mouse Button",
    "0x0053": "Back Button",
    "0x0054": "Back Button",
    "0x0056": "Forward Button",
    "0x0057": "Forward Button",
    "0x005b": "Left Scroll",
    "0x005d": "Right Scroll",
    "0x006e": "Show Desktop",
    "0x006f": "Lock Screen",
    "0x0090": "Minimize",
    "0x0091": "Maximize",
    "0x0095": "Switch Screens",
    "0x00ba": "Switch Apps",
    "0x00bb": "Home",
    "0x00bc": "Menu",
    "0x00bd": "Back Button",
    "0x00be": "Generic",
    "0x00bf": "Print Screen",
    "0x00c0": "Generic",
    "0x00c1": "Generic",
    "0x00c2": "Lock Screen",
    "0x00c3": "Gesture Button",
    "0x00c4": "Toggle SmartShift",
    "0x00c7": "Decrease Brightness",
    "0x00c8": "Increase Brightness",
    "0x00cc": "Switch Apps",
    "0x00ce": "Back Button",
    "0x00cf": "Forward Button",
    "0x00d0": "Switch Apps",
    "0x00d1": "Generic",
    "0x00d2": "Generic",
    "0x00d3": "Generic",
    "0x00d4": "Search",
    "0x00d5": "Home",
    "0x00d6": "Menu",
    "0x00d7": "Switch Receivers",
    "0x00dd": "Select Language",
    "0x00e0": "Task View",
    "0x00e1": "Action Center",
    "0x00e2": "Decrease Backlight",
    "0x00e3": "Increase Backlight",
    "0x00e4": "Previous Track",
    "0x00e5": "Play/Pause",
    "0x00e6": "Next Track",
    "0x00e7": "Mute",
    "0x00e8": "Volume Down",
    "0x00e9": "Volume Up",
    "0x00ea": "App Menu",
    "0x00ed": "Trackball Sensitivity",
    "0x00ef": "F key",
    "0x00f0": "F key",
    "0x00f1": "F key",
    "0x00f2": "F key",
    "0x00f3": "F key",
    "0x00f4": "F key",
    "0x00f5": "F key",
    "0x00f6": "F key",
    "0x00fd": "Sensitivity Switch",
    "0x00fe": "Home"
}


def main():
    
    for logitech_device in logitech_devices:
        print(logitech_device)

        print("Device ID:", logitech_device.device_id)
        print("Device Name:", logitech_device.device_name)
        print("Config File Device Name:", logitech_device.config_file_device_name)
        print("Min DPI:", logitech_device.min_dpi)
        print("Max DPI:", logitech_device.max_dpi)
        print("Default DPI:", logitech_device.default_dpi)
        print("Has Scrollwheel:", logitech_device.has_scrollwheel)
        print("Smartshift Support:", logitech_device.smartshift_support)
        print("Hires Scroll Support:", logitech_device.hires_scroll_support)
        print("Has Thumbwheel:", logitech_device.has_thumbwheel)
        print("Thumbwheel Tap Support:", logitech_device.thumbwheel_tap_support)
        print("Thumbwheel Proxy Support:", logitech_device.thumbwheel_proxy_support)
        print("Thumbwheel Touch Support:", logitech_device.thumbwheel_touch_support)
        print("Thumbwheel Timestamp Support:", logitech_device.thumbwheel_timestamp_support)
        print("Number of Sensors:", logitech_device.number_of_sensors)
        print("Buttons:", logitech_device.buttons)
        print("Device PIDs:", logitech_device.device_pids)
    print(len(logitech_devices))

if __name__ == "__main__":
    main()