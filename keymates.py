def get_keymates(key_input, layout=None):
    gui_keymates_en_us = {
            'GRAVE': '`',
            'SPACE': 'Space',
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
            'RIGHTMETA': 'Super',
            'ENTER': 'Enter',
            'UP': '↑',
            'DOWN': '↓',
            'LEFT': '←',
            'RIGHT': '→',
            'FN': 'Fn'
        }

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
            'Super_R': 'RIGHTMETA',
            'Escape': 'ESC',
            'XF86WakeUp': 'FN'
            }

    if layout == 'en_US' or layout == None:
        try:
            db_keymate = db_keymates_en_us[key_input]
        except KeyError:
            db_keymate = key_input.upper()
        try:
            gui_keymate = gui_keymates_en_us[db_keymate]
        except KeyError:
            gui_keymate = db_keymate
        return f"KEY_{db_keymate}", gui_keymate
