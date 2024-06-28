import DeviceData
import logging
import os
import execute_db_queries
import sqlite3


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
    # TODO: Update this function with more complex logic to handle version control, new devices etc.
    
    database_path = 'app_data/app_records.db'

    if not os.path.exists(database_path):

        conn, cursor = execute_db_queries.create_db_connection()
        
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("create_tables.sql")) # Create database tables
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("create_triggers.sql")) # Create database triggers
        execute_db_queries.execute_queries(cursor, parse_sql_file_into_array("insert_settings.sql")) # Create database triggers
        add_devices(cursor)

        conn.commit()
        conn.close()


db_original_path = 'app_data/app_records.db'
db_copy_path = 'app_data/app_records_editing.db'

def copy_database():


    if not os.path.exists(db_copy_path):
        os.system(f'cp "{db_original_path}" "{db_copy_path}"')

def replace_database_with_copy():

    if os.path.exists(db_copy_path) and os.path.exists(db_original_path):
        os.system(f'mv "{db_copy_path}" "{db_original_path}"')


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



# TODO: Create a query for duplicating configs. 
    # - New ButtonConfigs will automatically propagate with default values, so need to create Python that forces copy of these
    # - New Gesture IDs will automatically propagate with default values, so as above
    # - Unique constraints prevent duplicate entries (good), so just need to get the values from the tables and duplicate them
    # OR COULD this be done somehow through triggers? Specify a way to denote a copy versus a new insertion, and then let 



def main():
    # copy_database()
    delete_database_copy()

if __name__ == "__main__":
    main()