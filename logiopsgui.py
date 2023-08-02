import customtkinter as ctk
import time
import sqlite3
import logging
from make_database import create_tables, create_db_triggers, add_devices
from LogitechDeviceData import Device, DeviceButton, logitech_devices 
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")



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





def configure_logging():

    if not os.path.exists("app_data"):
        os.mkdir("app_data")

    logging.basicConfig(
        filename='app_data/error_log.txt',  # Log file name
        level=logging.ERROR,       # Set the log level to ERROR
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def initialise_database():

    database_path = 'app_data/app_records.db'

    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        execute_queries(cursor, create_tables)
        execute_queries(cursor, create_db_triggers)
        add_devices(cursor)
        
        conn.commit()
        conn.close()




def main():


    # Configure logging for the application
    configure_logging()

    # Connect to the SQL database and build the required tables
    initialise_database()

    # Create the main application window
    root = ctk.CTk()
    root.title('LogiOpsGUI') 
    root.geometry('1000x800')
    root.resizable(True, True)




    root.mainloop()

if __name__ == "__main__":
    main()