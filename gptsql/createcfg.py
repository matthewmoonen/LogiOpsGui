import sqlite3
import configparser
import json

# Create SQLite connection and cursor
conn = sqlite3.connect('custom_objects.db')
cursor = conn.cursor()

# Retrieve data from the database
cursor.execute('SELECT * FROM custom_objects')
custom_objects_data = cursor.fetchall()

cursor.execute('SELECT * FROM gestures')
gestures_data = cursor.fetchall()

# Close the connection
conn.close()

# Create a ConfigParser object
config = configparser.ConfigParser()

# Process custom_objects data
for row in custom_objects_data:
    cid = hex(row[0])  # Convert CID to hexadecimal representation
    action_type = row[1]
    data = row[2]

    # Add custom object section to the config
    config[cid] = {
        'action': {  # Use "action" instead of "data"
            'type': action_type,
            'keys': json.loads(data)  # Load JSON data as Python object
        }
    }

# Process gestures data
for row in gestures_data:
    gesture_id = str(row[0])
    custom_object_cid = hex(row[1])  # Convert CID to hexadecimal representation
    direction = row[2]
    mode = row[3]
    action_type = row[4]
    data = row[5]

    # Add gesture as an option within the custom object section
    option_key = gesture_id
    option_value = {
        'direction': direction,
        'mode': mode,
        'action': {  # Use "action" instead of "data"
            'type': action_type,
            'keys': json.loads(data)  # Load JSON data as Python object
        }
    }
    config.set(custom_object_cid, option_key, json.dumps(option_value))  # Store option value as JSON string

# Write the config data to the file
with open('logidtest.cfg', 'w') as configfile:
    config.write(configfile)
