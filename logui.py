import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkListbox import *
import create_app_data
import execute_db_queries
import DeviceData
from typing import Union, Callable
import main_page_elements
import edit_page_elements
import gui_variables






class IntSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 min_value: int = None,
                 max_value: int = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.command = command
        self.enabled = True  # TODO: Initial state is enabled

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-2, height=height-2,
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.default_value = 0 if min_value is None else min_value  # Set default value based on min_value

        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'),
                                  width=width-(2.8*height), height=height-4, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        
        self.entry.bind("<FocusOut>", self.on_focus_out)  # Bind the FocusOut event

        self.add_button = ctk.CTkButton(self, text="+", width=height-2.5, height=height-2.5,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, "0")

    def validate(self, new_text):
        return new_text.isdigit() or new_text == ""

    def on_focus_out(self, event):
        try:
            value = int(self.entry.get())
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
        except ValueError:
            value = self.default_value  # Use default_value if parsing fails
        
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try: 
            value = int(self.entry.get()) // self.step_size * self.step_size + self.step_size # Set new value to closest multiple of step size after the current value
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:

            def get_nearest_rounded_value(): # Set new value to closest multiple of step size after the current value
                previous_value = int(self.entry.get())
                return previous_value // self.step_size * self.step_size - self.step_size if previous_value % self.step_size == 0 else previous_value // self.step_size * self.step_size

            value = get_nearest_rounded_value()
            
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return 0

    def set(self, value: int):
        if self.min_value is not None and value < self.min_value:
            value = self.min_value
        if self.max_value is not None and value > self.max_value:
            value = self.max_value
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))

    def toggle_enable(self, new_enabled_state):
        self.enabled = new_enabled_state
        print(self.enabled)
        state = "normal" if self.enabled else "disabled"
        self.entry.configure(state=state)
        self.add_button.configure(state=state)
        self.subtract_button.configure(state=state)


class MainPage(ctk.CTkFrame):
    def __init__(self, 
                 master):
        super().__init__(master)

        self.edit_page = None
        self.selected_device = None


        main_page_elements.create_title_frame(self)

        top_frame = ctk.CTkFrame(master=self,
                                fg_color="transparent")
        top_frame.pack(
                        padx=(0, 10), 
                        pady=(0, 0),
                        fill="x",
        )

        top_frame.grid_columnconfigure((0), weight=1)

        def device_dropdown(new_device):
            self.selected_device = new_device  # Store the selected device name
            self.create_edit_page(self.selected_device)
            button_for_adding_devices.configure(state="normal", fg_color="#208637")
            button_for_adding_devices.configure(
                command=reset_button_after_click
                ) 

        def reset_button_after_click():
            create_and_update_device_dropdown()
            button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))
            self.show_edit_page()



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
        button_for_adding_devices.grid(
                                        padx=(20,20),
                                        row=0,
                                        column=2,
                                        )
        
        create_and_update_device_dropdown()
         
        devices_frame = ctk.CTkScrollableFrame(master=self,
                                              border_width=2,
                                                corner_radius=0,
                                                scrollbar_fg_color="#474747",
                                                scrollbar_button_color=gui_variables.primary_colour,
                                                # label_fg_color="red"
                                              )
        devices_frame.pack(
            padx=20,
            # pady=(0, 20),
            fill="both",
            expand=True,
            )


        user_devices_and_configs = execute_db_queries.get_user_devices_and_configs()
        for device in user_devices_and_configs:
            device_label = ctk.CTkLabel(master=devices_frame,
                                        text=device.device_name,
                                        font=ctk.CTkFont(
                                                family="Roboto",
                                                weight="bold",
                                                size=20,
                                                    ),
                                        )
            device_label.pack()


        


        bottom_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        bottom_frame.pack(
                        padx=(20, 20), 
                        pady=(0, 0),
                        fill="x",
        )








        save_devices_button = ctk.CTkButton(
            master=bottom_frame,
            height=40,
            width=120,
            text="Generate CFG",
            # text_color_disabled=("#9FA5AB"),
        )
        save_devices_button.grid(
            # row=0,
            # column=2,
            # padx=(20, 20),
            pady=30,
            sticky="e"
        )

        # thechosen = "TODO: update object to pass in"

        edit1 = ctk.CTkButton(
            master=bottom_frame,
            height=40,
            width=120,
            text="edit 1",
            command=lambda: self.edit_configuration("TODO: update object to pass in")
            # text_color_disabled=("#9FA5AB"),
        )
        edit1.grid(
            # row=0,
            # column=2,
            # padx=(20, 20),
            pady=30,
            sticky="e"
        )



        bottom_frame.grid_columnconfigure((0), weight=1)




    def edit_configuration(self, 
                           selected_config
                           ):
        print(selected_config)
        config_to_edit = execute_db_queries.get_object()
        self.edit_page = EditPage(self.master, configuration=config_to_edit, main_page=self.show)
        self.pack_forget()
        self.edit_page.pack(fill="both", expand=True)
        
    def show(self):
        self.pack(fill="both", expand=True)

    def create_edit_page(self, device_dropdown_name):
        self.edit_page = EditPage(self.master, 
                                  device_name=device_dropdown_name,
                                    main_page=self.show)
        self.edit_page.pack_forget()


    def show_edit_page(self):
        # self.create_and_update_device_dropdown()  # Corrected function name and using 'self'
        # self.button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))

        if self.edit_page:
            self.pack_forget()
            self.edit_page.pack(fill="both", expand=True)




class EditPage(ctk.CTkFrame):
    def __init__(self, master, main_page, configuration=None, #TODO: UPDATE NONETYPE
                 config_id=None, device_name=None # TODO: REMOVE THESE
                 ):
        super().__init__(master)


        self.master = master
        self.main_page = main_page
    

        edit_page_title = configuration.device_name
        edit_page_elements.create_name_device_label(self, edit_page_title)


        if configuration is not None:
            print("we've got a config!!!!")



        bottom_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        bottom_frame.pack()

        back_button = ctk.CTkButton(master=bottom_frame, 
                                            text="Cancel",
                                            command=self.go_back)
        back_button.pack(pady=20)



    def go_back(self):
        self.pack_forget()
        self.main_page()



def setup_gui(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1280x1280")
    root.resizable(True, True)
    root.title("LogiOpsGUI")

    main_page = MainPage(root)
    main_page.pack(fill="both", expand=True)

def main():

    root = ctk.CTk()
    
    create_app_data.configure_logging() # Configure logging for the application

    create_app_data.initialise_database() # Create DB, build required tables and triggers, add devices from DeviceData.py
    
    setup_gui(root) # Configure GUI settings and pack main page into window.
    
    root.mainloop()

if __name__ == "__main__":
    main()
