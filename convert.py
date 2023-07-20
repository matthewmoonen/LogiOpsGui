def main():
    print(get_keymate('BackSpace', 'en_US'))

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
        'Escape': 'KEY_ESC'
    }

    if layout == 'en_US' or None:
        return keymates_en_us.get(key, f'KEY_{key.upper()}')

if __name__ == "__main__":
    main()