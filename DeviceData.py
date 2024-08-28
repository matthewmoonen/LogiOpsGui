import Classes


#   Accessible refers to whether the button is physically accessible on the mouse when in normal use.
#   For example, 0x00d7 is normally the control ID for the button to switch between host devices/computers, and theoretically has gesture support.
#   However it is usually located on the bottom of the mouse. 

# Creating instances of LogitechDevice for each device
logitech_devices = [ 

Classes.DeviceDatabase(
device_id = 1900,
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
device_id = 1800,
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
device_id = 1700,
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
device_id = 1600,
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
device_id = 1500,
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
device_id = 1400,
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
device_id = 1300,
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
device_id = 1200,
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
device_id = 1100,
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
device_id = 1000,
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
device_id = 900,
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
device_id = 800,
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
device_id = 700,
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
device_id = 600,
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
device_id = 500,
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



def main():
    pass

if __name__ == "__main__":
    main()