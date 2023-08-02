



class Device:
    def __init__(self, device_id, device_name, config_file_device_name, product_ids, min_dpi, max_dpi, default_dpi, buttons, thumbwheel, smartshift_support, hires_scroll_support, number_of_sensors):
        self.device_id = device_id
        self.device_name = device_name
        self.config_file_device_name = config_file_device_name
        self.product_ids = product_ids
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi
        self.default_dpi = default_dpi
        self.buttons = buttons
        self.thumbwheel = thumbwheel
        self.smartshift_support = smartshift_support
        self.hires_scroll_support = hires_scroll_support
        self.number_of_sensors = number_of_sensors



class DeviceButton:
    def __init__(self, button_cid, reprogrammable, fn_key, mouse_key, gesture_support, accessible):
        self.button_cid = button_cid
        self.reprogrammable = reprogrammable
        self.fn_key = fn_key
        self.mouse_key = mouse_key
        self.gesture_support = gesture_support
        self.accessible = accessible

class DeviceThumbwheel:
    def __init__(self, has_thumbwheel, tap, proxy, touch, timestamp):
        self.has_thumbwheel = has_thumbwheel
        self.tap = tap
        self.proxy = proxy
        self.touch = touch
        self.timestamp = timestamp





# Creating instances of LogitechDevice for each device
logitech_devices = [


    Device(
        1,
        "MX Master 3S for Mac",
        "MX Master 3S for Mac",
        ["910-006574"],
        200, 8000, 1000,
        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, False, True),
            DeviceButton("0x00c4", True, False, True, True, True),
            DeviceButton("0x00d7", True, False, False, True, False),
        ],

        DeviceThumbwheel(True, True, True, True, True),
        True,
        True,
        1
        ),


    Device(
        2,
        "MX Master 3S", #Device name
        "MX Master 3S", #Logiops config name
            [ #List of product IDs
                "910-006561", # Graphite
                "910-006562" # Pale Gray
            ],

            200, 8000, 1000, #Min, Max and default DPI

        [
            DeviceButton("0x0050", False, False, True, False, True),
            DeviceButton("0x0051", False, False, True, False, True),
            DeviceButton("0x0052", True, False, True, True, True),
            DeviceButton("0x0053", True, False, True, True, True),
            DeviceButton("0x0056", True, False, True, True, True),
            DeviceButton("0x00c3", True, False, True, False, True),
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
            DeviceButton("0x00c3", True, False, True, False, True),
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
            DeviceButton("0x00c3", True, False, True, False, True),
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
            DeviceButton("0x00c3", True, False, True, False, True),
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
            DeviceButton("0x00c3", True, False, True, False, True),
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