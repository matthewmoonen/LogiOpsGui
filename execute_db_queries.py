import logging
import sqlite3
import DeviceData
import LogitechDeviceData
import ConfigClasses

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
        return conn, cursor
    except sqlite3.Error as e:
        logging.error(e)


def commit_changes_and_close(conn):
    conn.commit()
    conn.close()


def close_without_committing_changes(conn):
    conn.close()


def get_button_configs(config_id, button_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
                SELECT button_config_id, action
                FROM ButtonConfigs
                WHERE button_id = ? AND configuration_id = ?
                   """, (button_id, config_id))

    button_configs = cursor.fetchall()
    button_configs_array = []

    for row in button_configs:
        button_config = ConfigClasses.ButtonConfig(
            config_id=config_id,
            button_id=button_id,
            button_config_id=row[0],
            action=row[0]            
        )
        button_configs_array.append(button_config)

    return button_configs_array


def get_user_devices_and_configs():
        
    conn, cursor = create_db_connection()
    cursor.execute("""
        SELECT Devices.device_id, Devices.device_name, UserDevices.is_activated
        FROM Devices
        JOIN UserDevices ON Devices.device_id = UserDevices.device_id
        ORDER BY UserDevices.date_added DESC
    """)
    devices = cursor.fetchall()

    user_devices_objects = []
    for device in devices:
        device_id, device_name, is_activated = device

        # Fetch UserConfigs for the current device
        cursor.execute("""
            SELECT configuration_id, configuration_name, is_selected
            FROM Configurations
            WHERE device_id = ?
            ORDER BY is_selected DESC, last_modified DESC
        """, (device_id,))
        configs_data = cursor.fetchall()
        
        configs = []
        for config_data in configs_data:
            config_id, config_name, is_selected = config_data
            user_config = ConfigClasses.UserConfigs(device_id, config_id, config_name, is_selected)
            configs.append(user_config)

        user_device = ConfigClasses.UserDevices(device_id, device_name, is_activated, configs)
        user_devices_objects.append(user_device)

    close_without_committing_changes(conn)
    return user_devices_objects

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
    #             f"Config Name: {config.config_name}, "
    #             f"Is Selected: {config.is_selected}"
    #         )

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
        
        button = DeviceData.DeviceButton(
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




def get_scroll_action_keypresses(config_id, scroll_action_id):
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT keypress_id, keypresses
        FROM Keypresses
        WHERE gesture_id = ? AND scroll_action_id = ?
                   """, (config_id, scroll_action_id))

    scroll_action_keypresses_data = cursor.fetchall()


    scroll_action_keypresses_array = []

    for row in scroll_action_keypresses_data:
        
        keypress = ConfigClasses.Keypress(
            keypress_id=row[0],
            keypresses=row[1],
            config_id=config_id,
            scroll_action_id=scroll_action_id
        )
        scroll_action_keypresses_array.append(keypress)

    close_without_committing_changes(conn)

    return scroll_action_keypresses_array



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

def main():

    get_user_devices_and_configs()
    # button_configs_array = get_button_configs(15, 115)
    # for i in button_configs_array:
    #     print(i.button_config_id)

    # reprogrammable_buttons_array = get_reprogrammable_buttons_array(15)
    # for i in reprogrammable_buttons_array:
    #     print(i._button_cid, i._button_id, i._button_name, i._gesture_support)

if __name__ == "__main__":
    main()