class Device:
    def __init__(self,
                device_id=None,
                device_name=None,
                config_file_device_name=None,
                product_ids=None,
                min_dpi=None,
                max_dpi=None,
                default_dpi=None,
                buttons=None,
                has_thumbwheel=None,
                smartshift_support=None,
                hires_scroll_support=None,
                number_of_sensors=None,
                thumbwheel_tap=None,
                thumbwheel_proxy=None,
                thumbwheel_touch=None,
                thumbwheel_timestamp=None,
                user_device_id=None,
                date_added=None,
                last_edited=None
                #  user_added_or_edited = None, TODO: THIS
                
                 ):
        self._device_id = device_id
        self._device_name = device_name
        self._config_file_device_name = config_file_device_name
        self._product_ids = product_ids
        self._min_dpi = min_dpi
        self._max_dpi = max_dpi
        self._default_dpi = default_dpi
        self._buttons = buttons
        self._has_thumbwheel = has_thumbwheel
        self._smartshift_support = smartshift_support
        self._hires_scroll_support = hires_scroll_support
        self._number_of_sensors = number_of_sensors
        self._thumbwheel_tap = thumbwheel_tap
        self._thumbwheel_proxy = thumbwheel_proxy
        self._thumbwheel_touch = thumbwheel_touch
        self._thumbwheel_timestamp = thumbwheel_timestamp
        self._user_device_id = user_device_id
        self._date_added = date_added
        self._last_edited = last_edited

    def get_device_id(self):
        return self._device_id

    def get_device_name(self):
        return self._device_name

    def get_config_file_device_name(self):
        return self._config_file_device_name

    def get_product_ids(self):
        return self._product_ids

    def get_min_dpi(self):
        return self._min_dpi

    def get_max_dpi(self):
        return self._max_dpi

    def get_default_dpi(self):
        return self._default_dpi

    def get_buttons(self):
        return self._buttons

    def get_has_thumbwheel(self):
        return self._has_thumbwheel

    def get_smartshift_support(self):
        return self._smartshift_support

    def get_hires_scroll_support(self):
        return self._hires_scroll_support

    def get_number_of_sensors(self):
        return self._number_of_sensors
    
    def get_smartshift_on(self):
        return self._smartshift_on

    def get_thumbwheel_tap(self):
        return self._thumbwheel_tap

    def get_thumbwheel_proxy(self):
        return self._thumbwheel_proxy
    
    def get_thumbwheel_touch(self):
        return self._thumbwheel_touch

    def get_thumbwheel_timestamp(self):
        return self._thumbwheel_timestamp



    def set_device_id(self, device_id):
        self._device_id = device_id

    def set_device_name(self, device_name):
        self._device_name = device_name

    def set_config_file_device_name(self, config_file_device_name):
        self._config_file_device_name = config_file_device_name

    def set_product_ids(self, product_ids):
        self._product_ids = product_ids

    def set_min_dpi(self, min_dpi):
        self._min_dpi = min_dpi

    def set_max_dpi(self, max_dpi):
        self._max_dpi = max_dpi

    def set_default_dpi(self, default_dpi):
        self._default_dpi = default_dpi

    def set_buttons(self, buttons):
        self._buttons = buttons

    def set_has_thumbwheel(self, has_thumbwheel):
        self._has_thumbwheel = has_thumbwheel

    def set_smartshift_support(self, smartshift_support):
        self._smartshift_support = smartshift_support

    def set_hires_scroll_support(self, hires_scroll_support):
        self._hires_scroll_support = hires_scroll_support

    def set_number_of_sensors(self, number_of_sensors):
        self._number_of_sensors = number_of_sensors

    def set_smartshift_on_db(self, smartshift_on):
        self._smartshift_on = smartshift_on

    def set_smartshift_on_toggle(self):
        self._smartshift_on = not self._smartshift_on



class DeviceButton:
    def __init__(self, button_cid=None, reprogrammable=None, fn_key=None, mouse_key=None, gesture_support=None, accessible=None, button_id=None, button_name=None, button_action="Default", gesture_up=None, gesture_down=None, gesture_left=None, gesture_right=None, gesture_none=None):
        self._button_cid = button_cid
        self._reprogrammable = reprogrammable
        self._fn_key = fn_key
        self._mouse_key = mouse_key
        self._gesture_support = gesture_support
        self._accessible = accessible
        self._button_id = button_id
        self._button_name = button_name
        self._button_action = button_action
        self._gesture_up = gesture_up
        self._gesture_down = gesture_down
        self._gesture_left = gesture_left
        self._gesture_right = gesture_right
        self._gesture_none = gesture_none






        #   Accessible refers to whether the button is physically accessible on the mouse when in normal use.
        #   For example, 0x00d7 is normally the control ID for the button to switch between host devices/computers, and theoretically has gesture support.
        #   However it is usually located on the bottom of the mouse. 
        

    # Getters

    def get_button_id(self):
        return self._button_id

    def get_button_cid(self):
        return self._button_cid

    def get_reprogrammable(self):
        return self._reprogrammable

    def get_fn_key(self):
        return self._fn_key

    def get_mouse_key(self):
        return self._mouse_key

    def get_gesture_support(self):
        return self._gesture_support

    def get_accessible(self):
        return self._accessible
    
    def get_button_id(self):
        return self._button_id
    
    def get_button_name(self):
        return self._button_name

    # Setters
    def set_button_cid(self, button_cid):
        self._button_cid = button_cid

    def set_reprogrammable(self, reprogrammable):
        self._reprogrammable = reprogrammable

    def set_fn_key(self, fn_key):
        self._fn_key = fn_key

    def set_mouse_key(self, mouse_key):
        self._mouse_key = mouse_key

    def set_gesture_support(self, gesture_support):
        self._gesture_support = gesture_support

    def set_accessible(self, accessible):
        self._accessible = accessible

    def set_button_id(self, button_id):
        self._button_id = button_id

    def set_button_name(self, button_name):
        self._button_name = button_name


class DeviceThumbwheel:
    def __init__(self, 
                has_thumbwheel=None,
                tap=None,
                proxy=None, 
                proxy_keypresses=None,
                touch=None,
                timestamp=None,
                invert=False,
                divert=False):
        self._has_thumbwheel = has_thumbwheel
        self._tap = tap
        self._proxy = proxy
        self._proxy_keypresses = proxy_keypresses
        self._touch = touch
        self._timestamp = timestamp
        self._invert = invert
        self._divert = divert


    # Getters
    def get_has_thumbwheel(self):
        return self._has_thumbwheel

    def get_tap(self):
        return self._tap

    def get_proxy(self):
        return self._proxy
    
    def get_proxy_keypresses(self):
        return self._proxy_keypresses

    def get_touch(self):
        return self._touch

    def get_timestamp(self):
        return self._timestamp
    
    def get_invert(self):
        return self._invert
    
    def get_divert(self):
        return self._divert

    # Setters
    def set_has_thumbwheel(self, has_thumbwheel):
        self._has_thumbwheel = has_thumbwheel

    def set_tap(self, tap):
        self._tap = tap

    def set_proxy(self, proxy):
        self._proxy = proxy

    def set_proxy_keypresses(self, proxy_keypresses):
        self._proxy_keypresses = proxy_keypresses

    def set_touch(self, touch):
        self._touch = touch

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def set_invert(self):
        self._invert = not self._invert

    def set_divert_db(self, divert):
        self._divert = divert

    def set_divert_toggle(self):
        self._divert = not self._divert


# Creating instances of LogitechDevice for each device
logitech_devices = [


    Device(
        1, # Device ID. This doesn't reference anything related to Logitech's naming/classification of devices. It's simply for use in this program.
        
        "MX Master 3S for Mac", # Device name in the GUI

        "MX Master 3S for Mac", # Device name in the config file
        
        [
            "910-006574" # List of product IDs that the device is sold under (colour variations etc).
                         # This doesn't have a purpose in the code yet, but is included for posterity.
            ],

        200, 8000, 1000, # Min, Max and default DPI
            
        [ 
            # Control IDs for each button on the device, and booleans that reference:
                    # Is the button reprogrammable?
                    # Is it a function key (keyboards)? 
                    # Is it a mouse button? 
                    # Does it support gestures?
                    # Is the button is accessible? (See note in DeviceButton class above)
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],

        # Information relating to the thumbwheel.
        # Not all devices have one, so in this case the first value in the tuple will be False, and the others None
        # Booleans/nonetypes reference:
                # Does the device have a thumbwheel
                # Does the thumbwheel register a tap as an input?
                # Does it register proximity? 
                # Does it register touch?
                # Timestamp - I have no idea what this is but it's included in the LogiOps debug output so I've included it here.
        DeviceThumbwheel(True, True, True, True, True),

        True, # Does the device support SmartShift (mostly newer devices)
        
        True, # Does the device support hi-res scrolling?
        
        1 # Number of sensors that the mouse has. 
        
        ),


    Device(
        2,
        "MX Master 3S",
        "MX Master 3S",
            [
                "910-006561", # Graphite
                "910-006562" # Pale Gray
            ],

            200, 8000, 1000, 

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],

        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),

    
    Device(
        3,
        "MX Master 3 for Mac",
        "MX Master 3 for Mac",
            [
                "910-005696",
            ],

            200, 4000, 1000,

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],
            
        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),


    Device(
        4,
        "MX Master 3",
        "Wireless Mouse MX Master 3",
            [
                "910-005620"
            ],

            200, 4000, 1000,

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],
            
        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),

    Device(
        5,
        "MX Master 2S",
        "Wireless Mouse MX Master 2S",
            [
                "910-005131"
            ],

            200, 4000, 1000,
            
        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],
            
        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),    

    Device(
        6,
        "MX Master",
        "Wireless Mouse MX Master",
            [
                "910-004337",
            ],
            
            400, 1600, 1000,
    
        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, True, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],
                
        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),    

    Device(
        7,
        "MX Anywhere 3S",
        "MX Anywhere 3S",
            [
                "910-006932", # Graphite
                "910-006933", # Pale Grey
                "910-006934" # Rose
            ],
            
            200, 8000, 1000,

            [
                DeviceButton("0x0050", False, False, True, False, True),
                DeviceButton("0x0051", False, False, True, False, True),
                DeviceButton("0x0052", True, False, True, True, True),
                DeviceButton("0x0053", True, False, True, True, True),
                DeviceButton("0x0056", True, False, True, True, True),
                DeviceButton("0x005b", True, False, True, True, True),
                DeviceButton("0x005d", True, False, True, True, True),
                DeviceButton("0x00c4", True, False, True, True, True),
                DeviceButton("0x00d7", True, False, False, True, False),
            ], 
        
        DeviceThumbwheel(False, None, None, None, None),
        True,
        True,
        1
        ),

    Device(
        8,
        "MX Anywhere 3",
        "MX Anywhere 3",
            [
                "910-005987"
            ],
            
            200, 4000, 1000,
        
            [
                DeviceButton("0x0050", False, False, True, False, True),
                DeviceButton("0x0051", False, False, True, False, True),
                DeviceButton("0x0052", True, False, True, True, True),
                DeviceButton("0x0053", True, False, True, True, True),
                DeviceButton("0x0056", True, False, True, True, True),
                DeviceButton("0x005b", True, False, True, True, True),
                DeviceButton("0x005d", True, False, True, True, True),
                DeviceButton("0x00c4", True, False, True, True, True),
                DeviceButton("0x00d7", True, False, False, True, False),
            ], 
            
        DeviceThumbwheel(False, None, None, None, None),
        True,
        True,
        1
        ),
    
    Device(
        9,
        "MX Anywhere 2", 
        "Wireless Mouse MX Anywhere 2",   
            [
                "910-004373"
            ],
           
            400, 1600, 1000,
            
            [
                DeviceButton("0x0050", False, False, True, False, True),
                DeviceButton("0x0051", False, False, True, False, True),
                DeviceButton("0x0052", True, False, True, True, True),
                DeviceButton("0x0053", True, False, True, True, True),
                DeviceButton("0x0056", True, False, True, True, True),
                DeviceButton("0x005b", True, False, True, True, True),
                DeviceButton("0x005d", True, False, True, True, True),
                DeviceButton("0x00c4", True, False, True, True, True),
                DeviceButton("0x00d7", True, False, False, True, False),
            ], 
                        
        DeviceThumbwheel(False, None, None, None, None),
        False,
        True,
        1
        ),
    
    Device(
        10,
        "MX Anywhere 2S",
        "Wireless Mobile Mouse MX Anywhere 2S",
            [
                "910-005132"
            ],
            
            200, 4000, 1000,
        
            [
                DeviceButton("0x0050", False, False, True, False, True),
                DeviceButton("0x0051", False, False, True, False, True),
                DeviceButton("0x0052", True, False, True, True, True),
                DeviceButton("0x0053", True, False, True, True, True),
                DeviceButton("0x0056", True, False, True, True, True),
                DeviceButton("0x005b", True, False, True, True, True),
                DeviceButton("0x005d", True, False, True, True, True),
                DeviceButton("0x00c4", True, False, True, True, True),
                DeviceButton("0x00d7", True, False, False, True, False),
            ], 
            
        DeviceThumbwheel(False, None, None, None, None),
        True,
        True,
        1
        ),
    
    Device(
        11,
        "MX Vertical", 
        "MX Vertical Advanced Ergonomic Mouse",
            [
                "910-005447"
            ],

            400, 4000, 1000,
        
            [
                DeviceButton("0x0050", False, False, True, False, True),
                DeviceButton("0x0051", False, False, True, False, True),
                DeviceButton("0x0052", True, False, True, True, True),
                DeviceButton("0x0053", True, False, True, True, True),
                DeviceButton("0x0056", True, False, True, True, True),
                DeviceButton("0x00fd", True, False, True, True, True),
            ],
            
        DeviceThumbwheel(False, None, None, None, None),
                False,
        True,
        1
        ),
    
    Device(
        12,
        "MX Ergo", 
        "MX Ergo Multi-Device Trackball",
        [
            "910-005177"
        ],
           
        512, 2048, 1000,

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x005b", True, False, True, True, True),
            DeviceButton("0x005d", True, False, True, True, True),
            DeviceButton("0x00ed", True, False, True, True, True), # TODO: Get confirmation that this is correct for this button

        ],
            
        DeviceThumbwheel(False, None, None, None, None),
                False,
        True,
        1
        ),
    
    Device(
        13,
        "MX Ergo M575",
        "ERGO M575 Trackball",

        [
            "910-005294"
        ],

           400, 2000, 1000,
           
        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True), # TODO: are there any more buttons on this mouse?
        ],
        
        DeviceThumbwheel(False, None, None, None, None),
                False,
        True,
        1
        ),
    
    Device(
        14,
        "M720 Triathlon", 
        "M720 Triathlon Multi-Device Mouse",
        [
            "910-004791"
        ],

            200, 3200, 1000,
            
        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x005b", True, False, True, True, True),
            DeviceButton("0x005d", True, False, True, True, True),
            DeviceButton("0x00d0", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False), # TODO: Check accessibility!
        ],
        
        DeviceThumbwheel(False, None, None, None, None),
        False,
        True,
        1
        ),
    
    Device(
        15,
        "M585/M590", 
        "M585/M590 Multi-Device Mouse",
        [
            "910-005012",
            "910-005197"
        ],

            1000, 2000, 1000, 

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x005b", True, False, True, True, True),
            DeviceButton("0x005d", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],
        
        DeviceThumbwheel(False, None, None, None, None),
        False,
        True,
        1
        ),

]

# TODO: Change this to a dictionary.
class Controls:
    def __init__(self, control_id, function):
        self.control_id = control_id
        self.function = function

cid_button_functions = [
    Controls('0x0050', 'Left Mouse Button'),
    Controls('0x0051', 'Right Mouse Button'),
    Controls('0x0052', 'Middle Mouse Button'),
    Controls('0x0053', 'Back Button'),
    Controls('0x0054', 'Back Button'),
    Controls('0x0056', 'Forward Button'),
    Controls('0x0057', 'Forward Button'),
    Controls('0x005b', 'Left Scroll'),
    Controls('0x005d', 'Right Scroll'),
    Controls('0x006e', 'Show Desktop'),
    Controls('0x006f', 'Lock Screen'),
    Controls('0x0090', 'Minimize'),
    Controls('0x0091', 'Maximize'),
    Controls('0x0095', 'Switch Screens'),
    Controls('0x00ba', 'Switch Apps'),
    Controls('0x00bb', 'Home'),
    Controls('0x00bc', 'Menu'),
    Controls('0x00bd', 'Back Button'),
    Controls('0x00be', 'Generic'),
    Controls('0x00bf', 'Print Screen'),
    Controls('0x00c0', 'Generic'),
    Controls('0x00c1', 'Generic'),
    Controls('0x00c2', 'Lock Screen'),
    Controls('0x00c3', 'Gesture Button'),
    Controls('0x00c4', 'Toggle SmartShift'),
    Controls('0x00c7', 'Decrease Brightness'),
    Controls('0x00c8', 'Increase Brightness'),
    Controls('0x00cc', 'Switch Apps'),
    Controls('0x00ce', 'Back Button'),
    Controls('0x00cf', 'Forward Button'),
    Controls('0x00d0', 'Switch Apps'),
    Controls('0x00d1', 'Generic'),
    Controls('0x00d2', 'Generic'),
    Controls('0x00d3', 'Generic'),
    Controls('0x00d4', 'Search'),
    Controls('0x00d5', 'Home'),
    Controls('0x00d6', 'Menu'),
    Controls('0x00d7', 'Switch Receivers'),
    Controls('0x00dd', 'Select Language'),
    Controls('0x00e0', 'Task View'),
    Controls('0x00e1', 'Action Center'),
    Controls('0x00e2', 'Decrease Backlight'),
    Controls('0x00e3', 'Increase Backlight'),
    Controls('0x00e4', 'Previous Track'),
    Controls('0x00e5', 'Play/Pause'),
    Controls('0x00e6', 'Next Track'),
    Controls('0x00e7', 'Mute'),
    Controls('0x00e8', 'Volume Down'),
    Controls('0x00e9', 'Volume Up'),
    Controls('0x00ea', 'App Menu'),
    Controls('0x00ed', 'Trackball Sensitivity'),
    Controls('0x00ef', 'F key'),
    Controls('0x00f0', 'F key'),
    Controls('0x00f1', 'F key'),
    Controls('0x00f2', 'F key'),
    Controls('0x00f3', 'F key'),
    Controls('0x00f4', 'F key'),
    Controls('0x00f5', 'F key'),
    Controls('0x00f6', 'F key'),
    Controls('0x00fd', 'Sensitivity Switch'),
    Controls('0x00fe', 'Home')
]


def get_button_function(control_id):
    for button in cid_button_functions:
        if button.control_id == control_id:
            return button.function
        

def main():
   pass

if __name__ == "__main__":
    main()