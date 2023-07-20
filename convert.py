def main():
    print(get_keymate('BackSpace', 'en_US'))

def get_keymate(key, layout):

    keymates_en_us = {
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

    if layout == 'en_US' or None:
        return keymates_en_us.get(key, key.upper())

if __name__ == "__main__":
    main()