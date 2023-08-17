import customtkinter as ctk
import tkinter as tk
from CTkListbox import *

import create_app_data
import execute_db_queries
import LogitechDeviceData


class MainPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_edit_page, edit_page_instance
                #  device_name
                 ):
        super().__init__(master)
        # self.master = master
        self.edit_page_instance = edit_page_instance  # Store the EditPage instance

        title_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(
                            pady=(30,0),
                            fill="x"
        )

        app_title = ctk.CTkLabel(
                                    master=title_frame, 
                                    text="LogiOpsGUI",
                                    font=ctk.CTkFont(
                                                        family="Roboto",
                                                        weight="bold",
                                                        size=40,
                                                    ),
                                    text_color="#1F538D",
                                    pady=30,
                                    anchor='s'
                                    )
        
        app_title.pack()

        top_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        top_frame.pack(
                        padx=(0, 10), 
                       pady=(0, 0),
                       fill="x",
        )

        top_frame.grid_columnconfigure((0), weight=1)



        def create_and_update_device_dropdown():

            options = execute_db_queries.get_unconfigured_devices()
            selected_option_var = ctk.StringVar(value='Select Device To Add')
            add_device_dropdown = ctk.CTkOptionMenu(master=top_frame,
                                                    variable=selected_option_var,
                                                    values=options,
                                                    state="normal",
                                                    width=400,
                                                    height=36,
                                                    command=device_dropdown)
            add_device_dropdown.grid(row=0,
                                    column=1,
                                    # padx=20,
                                    pady=20,
                                    sticky="e",
                                    )


        button_for_adding_devices = ctk.CTkButton(master=top_frame,
                                        height=40,
                                        width=120,
                                        state="disabled",
                                        text="Add Device",
                                        text_color_disabled=("#9FA5AB"),
                                        fg_color=("#545B62"),
                                        hover_color=("#28A745"))
                                        # command=lambda: add_button_clicked('Select Device To Add'))
        button_for_adding_devices.grid(
                                        padx=(20,20),
                                        row=0,
                                        column=2,
                                        # sticky="w",
                                        )



        def device_dropdown(new_device):
            button_for_adding_devices.configure(state="normal")
            button_for_adding_devices.configure(fg_color="#208637")
            # create_edit_page(self.master, switch_to_edit_page, selected_device_name=new_device)
            self.edit_page_instance.device_name=new_device
            button_for_adding_devices.configure(command=lambda: add_button_clicked(new_device))  # Update button command with selected option
            # create_edit_page(new_device)
            


        def add_button_clicked(selected_option):
            button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))
            # current_datetime = int(time.time() * 1e9)
            # device_name(selected_option)
            switch_to_edit_page()
            create_and_update_device_dropdown()
            
            
            
            # print(f"logic for adding {selected_option} to the DB goes here")

        create_and_update_device_dropdown()



        # bottom_frame = ctk.CTkFrame(master=self)
        bottom_frame = ctk.CTkScrollableFrame(master=self)
        bottom_frame.pack(
            padx=20,
            # pady=(0, 20),
            fill="both",
            expand=True
            )
        

    

        # test1.grid(row=0, column=0, padx=20, pady=20)



class EditPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_main_page, device_name_label=None, device_attributes=None, device_id=None, device_name=None, config_file_device_name=None, product_ids=None, min_dpi=None, ):
        super().__init__(master)
        self.device_id = device_id
        self.master = master
        self.label = ctk.CTkLabel(self, text="Page 2: Input fields for New Entry Content")
        self.label.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back to Page 1", command=switch_to_main_page)
        self.back_button.pack(pady=5)
        

        self.device_name_label = device_name_label



        # self.device_name = device_name

        if device_name is not None:
            device_attributes, device_thumbwheel = execute_db_queries.get_new_user_device_attributes(device_name)
        
        if device_attributes is not None:
            print(device_attributes._device_name)
            self.device_name_label = ctk.CTkLabel(self, text=device_attributes._device_name)
            self.device_name_label.pack()
            # print(device_name)
        else:
            print("device attributes none")
            self.device_name_label = ctk.CTkLabel(self, text='label here')
            self.device_name_label.pack()


def setup_gui():
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1000x800")
    root.resizable(False, False)
    root.title("LogiOpsGUI")
    return root


def create_edit_page(master, switch_to_main_page, selected_device_name=None, selected_device_id=None):
    print("now creating the edit page")
    if selected_device_name is not None:
        edit_page = EditPage(master, switch_to_main_page, device_name=selected_device_name)
    elif selected_device_id is not None:
        edit_page = EditPage(master, switch_to_main_page, device_id=selected_device_id)
    else:
        edit_page = EditPage(master, switch_to_main_page)
    return edit_page



def create_main_page(master, switch_to_edit_page, edit_page):
    main_page = MainPage(master, switch_to_edit_page, edit_page)
    return main_page


def main():
    root = setup_gui()

    # Configure logging for the application
    create_app_data.configure_logging()

    # Connect to the SQL database and build the required tables
    create_app_data.initialise_database()



    def show_edit_page(selected_device=None):
        print(selected_device)
        main_page.pack_forget()
        # if selected_device is not None:
        edit_page.pack(fill="both", expand=True)


    def show_main_page():
        edit_page.pack_forget()
        main_page.pack(fill="both", expand=True)


    edit_page = create_edit_page(root, show_main_page)  # Create an instance of EditPage
    main_page = create_main_page(root, show_edit_page, edit_page)  # Pass the EditPage instance
    # ...


    # edit_page = create_edit_page(root, show_main_page)  # Pass the root and appropriate callback
    # main_page = create_main_page(root, show_edit_page)  # Pass the root and appropriate callback

    show_main_page()

    root.mainloop()

if __name__ == "__main__":
    main()
