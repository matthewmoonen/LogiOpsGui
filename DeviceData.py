import Classes


#   Accessible refers to whether the button is physically accessible on the mouse when in normal use.
#   For example, 0x00d7 is normally the control ID for the button to switch between host devices/computers, and theoretically has gesture support.
#   However it is usually located on the bottom of the mouse. 

# Creating instances of LogitechDevice for each device
logitech_devices = [ 

Classes.DeviceDatabase(
device_id = 1,
device_name = "MX Master 3S for Mac",
config_file_device_name = "MX Master 3S for Mac",
min_dpi = 200,
max_dpi = 8000,
default_dpi = 1000,
has_scrollwheel=True,
buttons = [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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


Classes.DeviceDatabase(
device_id = 2,
device_name = "MX Master 3S",
config_file_device_name = "MX Master 3S",

min_dpi = 200,
max_dpi = 8000,
default_dpi =              1000, 
has_scrollwheel=True,

buttons =      [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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


Classes.DeviceDatabase(
device_id = 3,
device_name = "MX Master 3 for Mac",
config_file_device_name = "MX Master 3 for Mac",

min_dpi =   200,
max_dpi =   4000,
default_dpi =         1000,
has_scrollwheel=True,

buttons =     [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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


Classes.DeviceDatabase(
device_id = 4,
device_name = "MX Master 3",
config_file_device_name = "Wireless Mouse MX Master 3",


min_dpi =  200, 
max_dpi = 4000,
default_dpi =           1000,
has_scrollwheel=True,

buttons =      [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 5,
device_name = "MX Master 2S",
config_file_device_name = "Wireless Mouse MX Master 2S",


min_dpi =  200, 
max_dpi =4000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =      [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 6,
device_name = "MX Master",
config_file_device_name = "Wireless Mouse MX Master",


min_dpi =  400,
max_dpi = 1600,
default_dpi = 1000,
has_scrollwheel=True,

buttons =     [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c3", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 7,
device_name = "MX Anywhere 3S",
config_file_device_name = "MX Anywhere 3S",


min_dpi =  200,
max_dpi = 8000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =         [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 8,
device_name = "MX Anywhere 3",
config_file_device_name = "MX Anywhere 3",

min_dpi =  200, 
max_dpi = 4000,
default_dpi = 1000,
has_scrollwheel=True,

buttons =       [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 9,
device_name = "MX Anywhere 2", 
config_file_device_name = "Wireless Mouse MX Anywhere 2",   


min_dpi =   400,
max_dpi = 1600, 
default_dpi = 1000,
has_scrollwheel=True,

buttons =      [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 10,
device_name = "MX Anywhere 2S",
config_file_device_name = "Wireless Mobile Mouse MX Anywhere 2S",

min_dpi =   200, max_dpi = 4000, default_dpi =1000,
has_scrollwheel=True,

buttons =       [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00c4", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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

Classes.DeviceDatabase(
device_id = 11,
device_name = "MX Vertical", 
config_file_device_name = "MX Vertical Advanced Ergonomic Mouse",


min_dpi =   400, max_dpi = 4000, default_dpi =1000,
has_scrollwheel=True,

buttons =    [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00fd", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
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

Classes.DeviceDatabase(
device_id = 12,
device_name = "MX Ergo", 
config_file_device_name = "MX Ergo Multi-Device Trackball",

min_dpi =   512, max_dpi = 2048, default_dpi = 1000,
has_scrollwheel=True,

buttons =    [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00ed", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True), # TODO: Get confirmation that this is correct for this button

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

Classes.DeviceDatabase(
device_id = 13,
device_name = "MX Ergo M575",
config_file_device_name = "ERGO M575 Trackball",


min_dpi =    400, max_dpi = 2000, default_dpi =1000,
has_scrollwheel=True,

buttons =    [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True), # TODO: are there any more buttons on this mouse?
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

Classes.DeviceDatabase(
device_id = 14,
device_name = "M720 Triathlon", 
config_file_device_name = "M720 Triathlon Multi-Device Mouse",

min_dpi =    200, max_dpi = 3200,default_dpi = 1000,
has_scrollwheel=True,

buttons =    [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0052", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d0", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False), # TODO: Check accessibility!
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

Classes.DeviceDatabase(
device_id = 15,
device_name = "M585/M590", 
config_file_device_name = "M585/M590 Multi-Device Mouse",

min_dpi =        1000, max_dpi = 2000,default_dpi = 1000, 
has_scrollwheel=True,

buttons =    [
Classes.ButtonProperties(button_cid="0x0050", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0051", reprogrammable=False, fn_key=False, mouse_key=True, gesture_support=False, accessible=True),
Classes.ButtonProperties(button_cid="0x0053", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x0056", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005b", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x005d", reprogrammable=True, fn_key=False, mouse_key=True, gesture_support=True, accessible=True),
Classes.ButtonProperties(button_cid="0x00d7", reprogrammable=True, fn_key=False, mouse_key=False, gesture_support=True, accessible=False),
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