import sqlite3
import json

# Create SQLite connection and cursor
conn = sqlite3.connect('custom_objects.db')
cursor = conn.cursor()

# Create custom_objects table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS custom_objects (
        cid INTEGER PRIMARY KEY,
        action_type TEXT,
        data TEXT
    )
''')

# Create gestures table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gestures (
        gesture_id INTEGER PRIMARY KEY,
        custom_object_cid INTEGER,
        direction TEXT,
        mode TEXT,
        action_type TEXT,
        data TEXT,
        FOREIGN KEY (custom_object_cid) REFERENCES custom_objects (cid)
    )
''')

# Data to be saved
data = [
    {
        "cid": 0xc3,
        "action": {
            "type": "Keypress",
            "keys": ["KEY_LEFTALT", "KEY_GRAVE"]
        }
    },
    {
        "cid": 0xc4,
        "action": {
            "type": "Gestures",
            "gestures": [
                {
                    "direction": "Up",
                    "mode": "OnRelease",
                    "action": {
                        "type": "Keypress",
                        "keys": ["KEY_LEFTCTRL", "KEY_T"]
                    }
                },
                {
                    "direction": "Down",
                    "mode": "OnRelease",
                    "action": {
                        "type": "Keypress",
                        "keys": ["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_T"]
                    }
                },
                {
                    "direction": "Right",
                    "mode": "OnRelease",
                    "action": {
                        "type": "Keypress",
                        "keys": ["KEY_LEFTCTRL", "KEY_TAB"]
                    }
                },
                {
                    "direction": "Left",
                    "mode": "OnRelease",
                    "action": {
                        "type": "Keypress",
                        "keys": ["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_TAB"]
                    }
                },
                {
                    "direction": "None",
                    "mode": "OnRelease",
                    "action": {
                        "type": "Keypress",
                        "keys": ["KEY_LEFTCTRL", "KEY_W"]
                    }
                }
            ]
        }
    },
    {
        "cid": 0x53,
        "action": {
            "type": "Keypress",
            "keys": ["KEY_PAGEDOWN"]
        }
    },
    {
        "cid": 0x56,
        "action": {
            "type": "Keypress",
            "keys": ["KEY_PAGEUP"]
        }
    }
]

# Save data to the database
for item in data:
    cid = item["cid"]
    action_type = item["action"]["type"]
    action_data = json.dumps(item["action"])

    cursor.execute('INSERT INTO custom_objects (cid, action_type, data) VALUES (?, ?, ?)',
                   (cid, action_type, action_data))

    if action_type == "Gestures":
        custom_object_cid = cid
        gestures = item["action"]["gestures"]
        for gesture in gestures:
            direction = gesture["direction"]
            mode = gesture["mode"]
            gesture_action_type = gesture["action"]["type"]
            gesture_action_data = json.dumps(gesture["action"])

            cursor.execute('INSERT INTO gestures (custom_object_cid, direction, mode, action_type, data) VALUES (?, ?, ?, ?, ?)',
                           (custom_object_cid, direction, mode, gesture_action_type, gesture_action_data))

# Commit changes and close the connection
conn.commit()
conn.close()
