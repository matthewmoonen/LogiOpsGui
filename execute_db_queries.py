import logging
import sqlite3
import DeviceData
# import ConfigClasses
import re


def execute_queries(cursor, queries, placeholders=None, data=None):
    try:
        if placeholders and data:
            for query, args in zip(queries, zip(placeholders, data)):
                cursor.execute(query, args[1])
        else:
            for query in queries:
                cursor.execute(query)

    except sqlite3.Error as e:
        logging.error(e)


def create_db_connection():
    try:
        conn = sqlite3.connect('app_data/app_records.db')
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn, cursor
    except sqlite3.Error as e:
        logging.error(e)


def commit_changes_and_close(conn):
    conn.commit()
    conn.close()


def close_without_committing_changes(conn):
    conn.close()

def get_next_sequential_name(name_to_match, similar_names):
    if len(similar_names) == 0 or name_to_match not in similar_names:
        return name_to_match

    else:
        pattern = rf'{re.escape(name_to_match)}(?: \((\d+)\))?'
        numbers = []

        for similar_name in similar_names:
            match = re.match(pattern, similar_name)
            if match:
                number_str = match.group(1)
                if number_str:
                    number = int(number_str)
                    if number >= 2:
                        numbers.append(number)

        if len(numbers) == 0:
            return f"{name_to_match} (2)"

        numbers.sort()

        for i in range(1):
            if numbers[0] < 2:
                del numbers[0]
                if len(numbers) == 0:
                    return f"{name_to_match} (2)"

        new_highest_number = 2
            
        for i in numbers:
            if i == new_highest_number:
                new_highest_number += 1
                continue
            else:
                break

        return f"{name_to_match} ({new_highest_number})"

def new_empty_configuration(device_id, device_name):
    conn, cursor = create_db_connection()

    cursor.execute("""
                SELECT configuration_name
                FROM Configurations
                WHERE device_id = ? AND configuration_name LIKE ? || '%'
""", (device_id, device_name))
    
    similar_names = cursor.fetchall()
    
    similar_names_as_strings = [str(row[0]) for row in similar_names]
    # print(similar_names_as_strings)

    next_config_name = get_next_sequential_name(device_name, similar_names_as_strings)

    # print(f"next config name: {next_config_name}")

    cursor.execute("""
                SELECT smartshift_support, hires_scroll_support, has_thumbwheel
                FROM Devices
                WHERE device_id = ?
""", (device_id,))

    smartshift_support, hires_scroll_support, has_thumbwheel = cursor.fetchone()

    if bool(smartshift_support) == True:
        smartshift_on = 1
        smartshift_threshold = smartshift_torque = 10
    else:
        smartshift_on = smartshift_threshold = smartshift_torque = None


    if bool(hires_scroll_support) == True:
        hiresscroll_hires = hiresscroll_invert = hiresscroll_target = True

    else:
        hiresscroll_hires = hiresscroll_invert = hiresscroll_target = None

    if bool(has_thumbwheel) == True:
        thumbwheel_divert = thumbwheel_invert = True

    else:
        thumbwheel_divert = thumbwheel_invert = None

    cursor.execute("""
    INSERT INTO Configurations (
        device_id,
        configuration_name,
        last_modified,
        is_selected,
        smartshift_on,
        smartshift_threshold,
        smartshift_torque,
        hiresscroll_hires,
        hiresscroll_invert,
        hiresscroll_target,
        thumbwheel_divert,
        thumbwheel_invert
    ) VALUES (?, ?, NULL, 0, ?, ?, ?, ?, ?, ?, ?, ?)
""", (device_id, next_config_name, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert)) 

    newest_configuration_id = cursor.lastrowid

    commit_changes_and_close(conn)
    
    return newest_configuration_id


    # TODO: can't import the appropriate class from Classes.py as this would create a circular import, 
    # however I would prefer to use classes. Need to restructure to fix this.
    # Also, parts of this could be replaced with triggers on the DB - have a think about what is more simple.

def delete_device(device_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
                UPDATE Devices
                SET is_user_device = 0
                WHERE device_id = ?
        """, (device_id,))
    commit_changes_and_close(conn)



def get_selected_config(device_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
                SELECT configuration_id
                FROM configurations
                WHERE is_selected = 1 AND device_id = ?
""", (device_id,))
    selected_config_id = cursor.fetchone()
    close_without_committing_changes(conn)
    return selected_config_id[0]


# def get_button_configs(config_id, button_id):
#     conn, cursor = create_db_connection()

#     cursor.execute("""
#                 SELECT button_config_id, action
#                 FROM ButtonConfigs
#                 WHERE button_id = ? AND configuration_id = ?
#                    """, (button_id, config_id))

#     button_configs = cursor.fetchall()
#     button_configs_array = []

#     for row in button_configs:
#         button_config = ConfigClasses.ButtonConfig(
#             config_id=config_id,
#             button_id=button_id,
#             button_config_id=row[0],
#             action=row[0]            
#         )
#         button_configs_array.append(button_config)

#     return button_configs_array


def get_user_device_objects():
    
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_id, device_name, is_activated
        FROM Devices
        WHERE is_user_device = 1
        ORDER BY date_added DESC
                   """)

    devices = cursor.fetchall()

    

# def get_user_devices_and_configs():
        
#     conn, cursor = create_db_connection()
#     cursor.execute("""
#         SELECT device_id, device_name, is_activated
#         FROM Devices
#         WHERE is_user_device = 1
#         ORDER BY date_added DESC
#     """)
#     devices = cursor.fetchall()

#     user_devices_objects = []
#     for device in devices:
#         device_id, device_name, is_activated = device

#         # Fetch UserConfigs for the current device
#         cursor.execute("""
#             SELECT configuration_id, configuration_name, is_selected
#             FROM Configurations
#             WHERE device_id = ?
#             ORDER BY is_selected DESC, last_modified DESC
#         """, (device_id,))
#         configs_data = cursor.fetchall()
        
#         configs = []
#         for config_data in configs_data:
#             config_id, configuration_name, is_selected = config_data
#             user_config = ConfigClasses.UserConfigs(device_id, config_id, configuration_name, is_selected)
#             configs.append(user_config)

#         user_device = ConfigClasses.UserDevices(device_id, device_name, is_activated, configs)
#         user_devices_objects.append(user_device)

#     close_without_committing_changes(conn)
#     return user_devices_objects

    # for user_device in user_devices_objects:
    #     print(
    #         f"Device ID: {user_device.device_id}, "
    #         f"Device Name: {user_device.device_name}, "
    #         f"Is Activated: {user_device.is_activated}"
    #     )
    #     print("Configs:")
    #     for config in user_device.configs:
    #         print(
    #             f"  Config ID: {config.config_id}, "
    #             f"Config Name: {config.configuration_name}, "
    #             f"Is Selected: {config.is_selected}"
    #         )



def update_selected_configuration(selected_configuration_id):
    # print(selected_configuration_id)

    conn, cursor = create_db_connection()

    cursor.execute("""
        UPDATE Configurations
        SET is_selected = 1
        WHERE configuration_id = ?
""", (selected_configuration_id,))

    commit_changes_and_close(conn)
    

def get_existing_device_config(config_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
            SELECT 
                   """)

    config = cursor.fetchone()
    return None
    # TODO: finish this

def get_reprogrammable_buttons_array(device_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
            SELECT button_id, button_cid, button_name, gesture_support
            FROM Buttons
            WHERE device_id = ? AND reprog = 1 AND accessible = 1
    """, (device_id,))

    reprogrammable_buttons_data = cursor.fetchall()

    reprogrammable_buttons_array = []

    for row in reprogrammable_buttons_data:
        
        button = DeviceData.InitialiseButtonsDatabase(
            button_id=row[0],
            button_cid=row[1],
            button_name=row[2],
            gesture_support=bool(row[3])
        )
        reprogrammable_buttons_array.append(button)

    close_without_committing_changes(conn)

    return reprogrammable_buttons_array


def get_new_user_device_attributes(selected_device):
    conn, cursor = create_db_connection()

    try:

        cursor.execute("""
                SELECT device_id, min_dpi, max_dpi, default_dpi, has_thumbwheel, thumbwheel_tap, thumbwheel_proxy, thumbwheel_touch, smartshift_support, hires_scroll_support, number_of_sensors
                FROM Devices
                WHERE device_name = ?               
        """, (selected_device,))

        device = cursor.fetchone()


        if device:
            device_attributes = DeviceData.Device(
                device_name=selected_device,
                device_id=device[0],
                min_dpi=device[1],
                max_dpi=device[2],
                default_dpi=device[3],
                smartshift_support=bool(device[8]),
                hires_scroll_support=device[9],
                number_of_sensors=device[10]
            )
            
            if bool(device[4]) == False:
                device_thumbwheel = None
            
            else:
                device_thumbwheel = LogitechDeviceData.DeviceThumbwheel(
                        tap=bool(device[5]),
                        proxy=bool(device[6]),
                        touch=bool(device[7]),
                )
                

        else:
            device_attributes = None

        close_without_committing_changes(conn)

        return device_attributes, device_thumbwheel

    except sqlite3.Error as e:
        logging.error(e)




# def get_scroll_action_keypresses(config_id, scroll_action_id):
#     conn, cursor = create_db_connection()

#     cursor.execute("""
#         SELECT keypress_id, keypresses
#         FROM Keypresses
#         WHERE gesture_id = ? AND scroll_action_id = ?
#                    """, (config_id, scroll_action_id))

#     scroll_action_keypresses_data = cursor.fetchall()


#     scroll_action_keypresses_array = []

#     for row in scroll_action_keypresses_data:
        
#         keypress = ConfigClasses.Keypress(
#             keypress_id=row[0],
#             keypresses=row[1],
#             config_id=config_id,
#             scroll_action_id=scroll_action_id
#         )
#         scroll_action_keypresses_array.append(keypress)

#     close_without_committing_changes(conn)

#     return scroll_action_keypresses_array



def get_gesture_keypresses():
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT keypress_id, keypresses
        FROM Keypresses
        WHERE 
                   """)



def get_configured_devices():
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_name
        FROM Devices
        WHERE is_user_device = 1
    """)

    user_devices = cursor.fetchall()
    

    close_without_committing_changes(conn)
    return [row[0] for row in user_devices]


def add_new_device(new_device_name):

    conn, cursor = create_db_connection()

    cursor.execute("""
        UPDATE Devices
        SET is_user_device = 1
        WHERE device_name = ?
""", (new_device_name,))

    # print(new_device_name)

    cursor.execute("""
        SELECT Configurations.configuration_id
        FROM Configurations
        JOIN Devices ON Configurations.device_id = Devices.device_id
        WHERE Devices.device_name = ?;
""", (new_device_name,))
    
    new_configuration_id = cursor.fetchone()[0]

    commit_changes_and_close(conn)

    return new_configuration_id

def get_unconfigured_devices():
    
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_name, device_id
        FROM Devices
        WHERE is_user_device = 0
    """)

    non_user_devices = cursor.fetchall()
    
    close_without_committing_changes(conn)
    
    return [row[0] for row in non_user_devices]

def get_configured_devices_and_configs():

    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT 
                   """)
    


# TODO CREATE trigger to automatically propagate default_dpi to be current DPI on addition of new configuration.

def get_object():
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_id, device_name, min_dpi, max_dpi, has_scrollwheel, has_thumbwheel, thumbwheel_tap, thumbwheel_proxy, thumbwheel_touch, smartshift_support, hires_scroll_support, is_activated, date_added, is_activated, last_edited, default_dpi, config_file_device_name
                   FROM Devices
                   WHERE is_user_device = 1
                   ORDER BY date_added DESC
""")


    sql_query_results = cursor.fetchall()

    user_devices = []
    for result in sql_query_results:
        # print(result[14])
        user_device = DeviceData.EditPageDevice(
            device_id=result[0], device_name=result[1], min_dpi=result[2], max_dpi=result[3], has_scrollwheel=result[4], has_thumbwheel=result[5],
            thumbwheel_tap_support=result[6], thumbwheel_proxy_support=result[7], thumbwheel_touch_support=result[8], smartshift_support=result[9],
            hires_scroll_support=result[10], is_activated=result[11], date_added=result[12], last_edited=result[13],
            configurations=["todo:", "finish this"], config_file_device_name=result[16], default_dpi=result[15], thumbwheel_timestamp_support=False, number_of_sensors=1, is_user_device=True
        )
        
        user_devices.append(user_device)


    conn.close()


    return user_devices[0]




def delete_configuration(configuration_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
                   DELETE FROM Configurations
                   WHERE configuration_id = ?
                    """, (configuration_id,))



    commit_changes_and_close(conn)



def get_configurations(device_id):
    conn, cursor = create_db_connection()

    # TODO: Update selection order.

    cursor.execute("""
        SELECT configuration_id, configuration_name, date_added, last_modified, is_selected, dpi, smartshift_on, smartshift_threshold, smartshift_torque, hiresscroll_hires, hiresscroll_invert, hiresscroll_target, thumbwheel_divert, thumbwheel_invert, scroll_up_action, scroll_down_action, scroll_left_action, scroll_right_action, proxy_action, tap_action, touch_action
        FROM Configurations
        WHERE device_id = ?
        ORDER BY is_selected DESC
    """, (device_id,))



    sql_query_results = cursor.fetchall()

    user_device_configurations = []
    for result in sql_query_results:
        user_config = DeviceData.DeviceConfig(
    configuration_id=result[0],
    configuration_name=result[1],
    date_added=result[2],
    last_modified=result[3],
    is_selected=bool(result[4]),
    dpi=result[5],
    #TODO Update getter and setter methods to handle these better.
    smartshift_on=bool(result[6]) if result[6] is not None else result[6],
    smartshift_threshold=result[7],
    smartshift_torque= result[8],
    hiresscroll_hires = bool(result[9]) if result[9] is not None else result[9],
    hiresscroll_invert = bool(result[10]) if result[10] is not None else result[10],
    hiresscroll_target = bool(result[11]) if result[11] is not None else result[11],
    thumbwheel_divert = bool(result[12]) if result[12] is not None else result[12],
    thumbwheel_invert = result[13],
    scroll_up_action = result[14],
    scroll_down_action = result[15],
    scroll_left_action = result[16],
    scroll_right_action = result[17],
    proxy_action = result[18],
    tap_action = result[19],
    touch_action = result[20],


)
    user_device_configurations.append(user_config)


    
    print("Config ID:", user_config.configuration_id)
    print("Config Name:", user_config.configuration_name)
    print("DPI:", user_config.dpi)
    print("Date Added:", user_config.date_added)
    print("Last Modified:", user_config.last_modified)
    print("Is Selected:", user_config.is_selected)
    print("Smartshift On:", user_config.smartshift_on)
    print("Smartshift Threshold:", user_config.smartshift_threshold)
    print("Hiresscroll Hires:", user_config.hiresscroll_hires)
    print("Hiresscroll Invert:", user_config.hiresscroll_invert)
    print("Hiresscroll Target:", user_config.hiresscroll_target)
    print("Thumbwheel Divert:", user_config.thumbwheel_divert)
    print("Thumbwheel Invert:", user_config.thumbwheel_invert)
    print("Scroll Up Action:", user_config.scroll_up_action)
    print("Scroll Down Action:", user_config.scroll_down_action)
    print("Scroll Left Action:", user_config.scroll_left_action)
    print("Scroll Right Action:", user_config.scroll_right_action)
    print("Proxy Action:", user_config.proxy_action)
    print("Tap Action:", user_config.tap_action)
    print("Touch Action:", user_config.touch_action)


    conn.close()

    return user_device_configurations


def get_scroll_actions():
    
    
    pass


def main():
    get_configurations(14)
    # get_object()
    # get_user_devices_and_configs()
    # button_configs_array = get_button_configs(15, 115)
    # for i in button_configs_array:
    #     print(i.button_configuration_id)

    # reprogrammable_buttons_array = get_reprogrammable_buttons_array(15)
    # for i in reprogrammable_buttons_array:
    #     print(i._button_cid, i._button_id, i._button_name, i._gesture_support)

if __name__ == "__main__":
    main()