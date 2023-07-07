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
    cid = str(row[0])
    action_type = row[1]
    data = row[2]

    # Add custom object section to the config
    config[cid] = {
        'type': action_type,
        'data': data
    }

# Process gestures data
for row in gestures_data:
    gesture_id = str(row[0])
    custom_object_cid = str(row[1])
    direction = row[2]
    mode = row[3]
    action_type = row[4]
    data = row[5]

    # Create a nested subsection data as a string
    gesture_data = {
        'direction': direction,
        'mode': mode,
        'type': action_type,
        'data': data
    }
    gesture_data_str = json.dumps(gesture_data)

    # Add the nested subsection data as a string within the main section
    config.set(custom_object_cid, gesture_id, gesture_data_str)

# Write the config data to the file
with open('logidtest.cfg', 'w') as configfile:
    config.write(configfile)
