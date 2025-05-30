import DeviceData
import logging
import os
import execute_db_queries
import sqlite3
import version

def configure_logging():

    if not os.path.exists("app_data"):
        os.mkdir("app_data")

    logging.basicConfig(
        filename='app_data/error_log.txt',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def initialise_database():
    
    database_path = 'app_data/app_records.db'

    if not os.path.exists(database_path):

        conn, cursor = execute_db_queries.create_db_connection()
        
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("create_tables.sql")) # Create database tables
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("create_triggers.sql")) # Create database triggers
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("insert_settings.sql")) # Create database triggers
        cursor.execute("""INSERT INTO UserSettings(key, value) VALUES ('version', ?)""", (version.__version__,))
        add_devices(cursor)

        conn.commit()
        conn.close()
    else:
        conn, cursor = execute_db_queries.create_db_connection()

        cursor.execute("""SELECT value FROM UserSettings WHERE key = 'version'""")
        latest_used_version = cursor.fetchone()[0]
        if latest_used_version == version.__version__:
            execute_db_queries.close_without_committing_changes(conn)
        else:
            cursor.execute("""INSERT INTO UserSettings (key, value) VALUES (?, 'previous version')""", (latest_used_version,))
            cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'version'""", (version.__version__,))
            execute_db_queries.commit_changes_and_close(conn)

def parse_sql_file_into_array(sql_file_path):
    with open (sql_file_path , "r") as sql_file:
        sql_contents = sql_file.read()

    queries = sql_contents.split("-- ### QUERY_SEPARATOR ###")  
    
    return_array = []

    for query in queries:
        formatted_query = query.strip()
        if formatted_query:  # Skip empty queries
            return_array.append(formatted_query)

    return return_array

def add_devices(cursor):
    try:
        for device in DeviceData.logitech_devices:



            cursor.execute("""
                            INSERT INTO Devices (
                                device_id,
                                device_name,
                                is_user_device,
                                config_file_device_name,
                                device_pids,
                                min_dpi,
                                max_dpi,
                                default_dpi,
                                has_thumbwheel,
                                thumbwheel_tap,
                                thumbwheel_proxy,
                                thumbwheel_touch,
                                thumbwheel_timestamp,
                                smartshift_support,
                                hires_scroll_support,
                                number_of_sensors,
                                has_scrollwheel


                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                            
                            device.device_id,
                            device.device_name,
                            0,
                            device.config_file_device_name,
                            str(device.device_pids),
                            device.min_dpi,
                            device.max_dpi,
                            device.default_dpi,
                            device.has_thumbwheel,
                            device.thumbwheel_tap_support,
                            device.thumbwheel_proxy_support,
                            device.thumbwheel_touch_support,
                            device.thumbwheel_timestamp_support,
                            device.smartshift_support, 
                            device.hires_scroll_support, 
                            device.number_of_sensors,
                            device.has_scrollwheel
                            ))
            
            for button in device.buttons:

                cursor.execute("""
                                INSERT INTO Buttons (
                                    device_id,
                                    button_cid,
                                    button_name,
                                    reprog,
                                    fn_key,
                                    mouse_key,
                                    gesture_support,
                                    accessible
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                
                                device.device_id,
                                button.button_cid,
                                button.button_name,
                                button.reprogrammable,
                                button.fn_key,
                                button.mouse_key,
                                button.gesture_support,
                                button.accessible
                                ))

    except sqlite3.Error as e:
        logging.error(e)




def main():
    conn, cursor = execute_db_queries.create_db_connection()
    add_devices(cursor)
    execute_db_queries.commit_changes_and_close(conn)

if __name__ == "__main__":
    main()