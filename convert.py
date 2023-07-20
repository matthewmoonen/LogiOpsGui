def main():
    print(get_keymate('at', 'en_US'))

def get_keymate(key, layout):

    keymates_en_us = {
        'asciitilde': 'grave',
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
        'underscore': 'minus',
        'plus': 'equal',
        'braceleft': 'bracketleft',
        'braceright': 'bracketright',
        'bar': 'backslash',
        'colon': 'semicolon',
        'quotedbl': 'apostrophe',
        'less': 'comma',
        'greater': 'period',
        'question': 'slash'
    }

    if layout == 'en_US':
        return keymates_en_us.get(key, key)

if __name__ == "__main__":
    main()