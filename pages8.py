import customtkinter as ctk
import tkinter as tk
from CTkListbox import *

import create_app_data
import execute_db_queries
import LogitechDeviceData


class MainPage(ctk.CTkFrame):

    def __init__(self,
                 master, 
            
                ):
        super().__init__(master)
        


class EditPage(ctk.CTkFrame):
    def __init__(self,
                 master, 
                 ):
        super().__init__(master)


def setup_gui():
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1000x800")
    root.resizable(False, False)
    root.title("LogiOpsGUI")
    return root

def main():
    
    root = setup_gui()

    root.mainloop()

if __name__ == "__main__":
    main()






    def show_edit_page():
        main_page.pack_forget()
        edit_page.pack(fill="both", expand=True)


    def show_main_page():
        edit_page.pack_forget()
        main_page.pack(fill="both", expand=True)

