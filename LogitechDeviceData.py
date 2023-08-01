



class Device:
    def __init__(self, name, config_file_device_name, product_ids, min_dpi, max_dpi, default_dpi, buttons, thumbwheel, smartshift_support, hires_scroll_support, number_of_sensors):
        self.name = name
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
    def __init__(self, button_id, reprogrammable, fn_key, mouse_key, gesture_support, accessible):
        self.button_id = button_id
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




# def print_device_info(device):
#     print(f"Device Name: {device.name}")
#     print(f"Config File Device Name: {device.config_file_device_name}")
#     print(f"Config File Product IDs: {device.product_ids}")
#     print(f"Min DPI: {device.min_dpi}")
#     print(f"Max DPI: {device.max_dpi}")
#     print(f"Default DPI: {device.default_dpi}")
#     print(f"Has Thumbwheel: {device.has_thumbwheel}")
#     print("Buttons:")
#     for button in device.buttons:
#         print(f"  Button ID: {button.button_id}")
#         print(f"  Reprogrammable: {button.reprogrammable}")
#         print(f"  Function Key: {button.fn_key}")
#         print(f"  Mouse Key: {button.mouse_key}")
#         print(f"  Gesture Support: {button.gesture_support}")
#         print(f"  Accessible: {button.accessible}")
#         print()

# for device in logitech_devices:
#     print_device_info(device)