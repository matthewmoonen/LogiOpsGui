# Name
String

# Smartshift
* on - Bool
* threshold - int 1 - 255 or False
* torque - int - upper/lower limit unknown???

# Hiresscroll
* hires - bool
* invert - bool
* target - bool

# DPI 

If your mouse has multiple sensors, you may define separate DPIs for those sensors by using an array and placing the value in the sensor's index (e.g. sensor 0: 1000 dpi, sensor 1: 800 dpi -> dpi: [1000, 800])

* for now - int default value 1000. Try to put in array of len(1), see whether it works. 

# Buttons
* Each has an ID - string. E.g. '0xc3'
* Each has an action which can be:
    - None
    - Keypress
    - Gesture
* If keypress, 'keys' field required. This is an array of stings. e.g. ["KEY_LEFTCTRL", "KEY_T"]
* If gesture, need to create gesture object, which has 'direction' field that has 5 options:
    - gesture.up
    - gesture.down
    - gesture.left
    - gesture.right