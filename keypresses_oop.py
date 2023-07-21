import tkinter as tk

class ClickAndKeypressLogger:
    def __init__(self):
        self.selected_box = None
        self.box_buttons = {}
        self.box_text_map = {box_number: "" for box_number in range(1, 8)}

    @staticmethod
    def get_gui_keymate(key, layout):
        gui_keymates_en_us = {
            'GRAVE': '`',
            'MINUS': '-',
            'EQUAL': '=',
            'BACKSPACE': 'Backspace',
            'LEFTBRACE': '[',
            'RIGHTBRACE': ']',
            'BACKSLASH': '\\',
            'TAB': 'Tab',
            'CAPS_LOCK': 'CapsLock',
            'LEFTSHIFT': 'Shift',
            'RIGHTSHIFT': 'Shift',
            'LEFTCTRL': 'Ctrl',
            'RIGHTCTRL': 'Ctrl',
            'LEFTALT': 'Alt',
            'RIGHTALT': 'Alt',
            'APOSTROPHE': "'",
            'SEMICOLON': ';',
            'SLASH': '/',
            'DOT': '.',
            'COMMA': ',',
            'PAGEUP': 'PgUp',
            'PAGEDOWN': 'PgDn',
            'HOME': 'Home',
            'END': 'End',
            'DELETE': 'Delete',
            'ESC': 'Esc',
            'LEFTMETA': 'Super',
            'ENTER': 'Enter',
            'UP': '↑',
            'DOWN': '↓',
            'LEFT': '←',
            'RIGHT': '→'
        }

        if layout == 'en_US' or layout == None:
            return gui_keymates_en_us.get(key, key)
    @staticmethod
    def get_db_keymate(key, layout):
        db_keymates_en_us = {
            'asciitilde': 'GRAVE',
            'exclam': '1',
            'at': '2',
            'numbersign': '3',
            'dollar': '4',
            'percent': '5',
            'asciicircum': '6',
            'ampersand': '7',
            'asterisk': '8',
            'parenleft': '9',
            'parenright': '0',
            'underscore': 'MINUS',
            'plus': 'EQUAL',
            'braceleft': 'LEFTBRACE',
            'bracketleft': 'LEFTBRACE',
            'braceright': 'RIGHTBRACE',
            'bracketright': 'RIGHTBRACE',
            'bar': 'BACKSLASH',
            'colon': 'SEMICOLON',
            'quotedbl': 'APOSTROPHE',
            'less': 'COMMA',
            'greater': 'DOT',
            'period': 'DOT',
            'question': 'SLASH',
            'Prior': 'PAGEUP',
            'Next': 'PAGEDOWN',
            'Control_L': 'LEFTCTRL',
            'Control_R': 'RIGHTCTRL',
            'Shift_L': 'LEFTSHIFT',
            'Shift_R': 'RIGHTSHIFT',
            'Alt_L': 'LEFTALT',
            'Alt_R': 'RIGHTALT',
            'Return': 'ENTER',
            'Super_L': 'LEFTMETA',
            'Escape': 'ESC'
            }

        if layout == 'en_US' or layout == None:
            return db_keymates_en_us.get(key, key.upper())

    def on_keypress(self, event):
        if self.selected_box is not None:
            key = event.keysym
            keymate = ClickAndKeypressLogger.get_db_keymate(key, 'en_US')
            box_text = self.box_text_map[self.selected_box] + " " + keymate

            print(keymate)
            keymategui = ClickAndKeypressLogger.get_gui_keymate(keymate, 'en_US')
            print(keymategui)
            self.update_box_text(self.selected_box, box_text)

    def on_box_click(self, box_number):
        self.selected_box = box_number
        print("Box {} selected".format(box_number))

    def update_box_text(self, box_number, text):
        if box_number in self.box_buttons:
            self.box_buttons[box_number].configure(text=text)
            self.box_text_map[box_number] = text

    def create_window(self):
        root = tk.Tk()
        root.geometry("500x400")
        root.title("Click and Keypress Logger")

        label = tk.Label(root, text="Click a box and press a key:")
        label.pack(pady=10)

        box_names = {
            1: "Wheel Button",
            2: "Top Button",
            3: "Thumb Wheel Left",
            4: "Thumb Wheel Right",
            5: "Forward Button",
            6: "Back Button",
            7: "Thumb Button"
        }

        for box_number, box_name in box_names.items():
            box_button = tk.Button(root, text=box_name, command=lambda num=box_number: self.on_box_click(num))
            box_button.pack(pady=5)
            self.box_buttons[box_number] = box_button

        root.bind("<Key>", self.on_keypress)
        root.mainloop()

if __name__ == "__main__":
    logger = ClickAndKeypressLogger()
    logger.create_window()
