import logging
import sqlite3


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
    conn = sqlite3.connect('app_data/app_records.db')
    cursor = conn.cursor()
    return conn, cursor

def commit_changes(conn):
        conn.commit()
        conn.close()



def get_configured_devices():
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_name
        FROM Devices
        WHERE is_user_device = 1
    """)

    user_devices = cursor.fetchall()
    user_devices_list = [row[0] for row in user_devices]

    print(user_devices_list)

def get_unconfigured_devices():
    
    conn, cursor = create_db_connection()

    cursor.execute("""
        SELECT device_name, device_id
        FROM Devices
        WHERE is_user_device = 0
    """)

    non_user_devices = cursor.fetchall()
    
    commit_changes(conn)
    # print(non_user_devices)
    return [row[0] for row in non_user_devices]

    