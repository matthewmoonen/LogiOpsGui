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
        # print('creating connection')
        conn = sqlite3.connect('app_data/app_records.db')
        
        cursor = conn.cursor()
        # conn.execute('PRAGMA journal_mode=WAL;')
        # cursor.execute('PRAGMA journal_mode;')
        result = cursor.fetchone()
        # print(f"Current journal mode: {result[0]}")
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn, cursor
    except sqlite3.Error as e:
        logging.error(e)
        

def commit_changes_and_close(conn):
    conn.commit()
    conn.close()


def close_without_committing_changes(conn):

    conn.close()

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



def get_user_device_objects():
    
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_id, device_name, is_activated
        FROM Devices
        WHERE is_user_device = 1
        ORDER BY date_added DESC
                   """)

    devices = cursor.fetchall()

    
    

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


def get_unconfigured_devices_dictionary():
    
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_name, device_id
        FROM Devices
        WHERE is_user_device = 0
    """)

    non_user_devices = cursor.fetchall()
    
    close_without_committing_changes(conn)
    
    unconfigured_devices = {}

    for i in non_user_devices:
        unconfigured_devices[i[1]] = i[0]

    return unconfigured_devices


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




    conn.close()

    return user_device_configurations


def get_scroll_actions():
    
    
    pass


def main():

    unconfigured_devices_dict = get_unconfigured_devices_dictionary()
    print(unconfigured_devices_dict)


if __name__ == "__main__":
    main()