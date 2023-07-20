import tkinter as tk

selected_box = None


def on_keypress(event):
    if selected_box is not None:
        key = event.keysym
        keymate = get_keymate(key, 'en_US')
        box_text = box_text_map[selected_box] + " " + keymate

        print(keymate)
        update_box_text(selected_box, box_text)

def get_keymate(key, layout):

    keymates_en_us = {
        'asciitilde': 'KEY_GRAVE',
        'exclam': 'KEY_1',
        'at': 'KEY_2',
        'numbersign': 'KEY_3',
        'dollar': 'KEY_4',
        'percent': 'KEY_5',
        'asciicircum': 'KEY_6',
        'ampersand': 'KEY_7',
        'asterisk': 'KEY_8',
        'parenleft': 'KEY_9',
        'parenright': 'KEY_0',
        'underscore': 'KEY_MINUS',
        'plus': 'KEY_EQUAL',
        'braceleft': 'KEY_LEFTBRACE',
        'bracketleft': 'KEY_LEFTBRACE',
        'braceright': 'KEY_RIGHTBRACE',
        'bracketright': 'KEY_RIGHTBRACE',
        'bar': 'KEY_BACKSLASH',
        'colon': 'KEY_SEMICOLON',
        'quotedbl': 'KEY_APOSTROPHE',
        'less': 'KEY_COMMA',
        'greater': 'KEY_DOT',
        'period': 'KEY_DOT',
        'question': 'KEY_SLASH',
        'Prior': 'KEY_PAGEUP',
        'Next': 'KEY_PAGEDOWN',
        'Control_L': 'KEY_LEFTCTRL',
        'Control_R': 'KEY_RIGHTCTRL',
        'Shift_L': 'KEY_LEFTSHIFT',
        'Shift_R': 'KEY_RIGHTSHIFT',
        'Alt_L': 'KEY_LEFTALT',
        'Alt_R': 'KEY_RIGHTALT',
        'Return': 'KEY_ENTER',
        'Super_L': 'KEY_LEFTMETA',
        'Escape': 'KEY_ESC',
        'Caps_Lock': 'KEY_CAPSLOCK'
    }

    if layout == 'en_US' or None:
        return keymates_en_us.get(key, f'KEY_{key.upper()}')

def on_box_click(box_number):
    global selected_box
    selected_box = box_number
    print("Box {} selected".format(box_number))

def update_box_text(box_number, text):
    if box_number in box_buttons:
        box_buttons[box_number].configure(text=text)
        box_text_map[box_number] = text

def create_window():
    root = tk.Tk()
    root.geometry("500x400")
    root.title("Click and Keypress Logger")

    label = tk.Label(root, text="Click a box and press a key:")
    label.pack(pady=10)

    global box_buttons
    box_buttons = {}

    box_names = {
        1: "Wheel Button",
        2: "Top Button",
        3: "Thumb Wheel Left",
        4: "Thumb Wheel Right",
        5: "Forward Button",
        6: "Back Button",
        7: "Thumb Button"
    }

    global box_text_map
    box_text_map = {box_number: "" for box_number in range(1, 8)}

    for box_number, box_name in box_names.items():
        box_button = tk.Button(root, text=box_name, command=lambda num=box_number: on_box_click(num))
        box_button.pack(pady=5)
        box_buttons[box_number] = box_button

    root.bind("<Key>", on_keypress)
    root.mainloop()

create_window()
