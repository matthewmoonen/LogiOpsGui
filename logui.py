import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkListbox import *
import create_app_data
import execute_db_queries
import LogitechDeviceData
# from spinbox import IntSpinbox
from typing import Union, Callable


# primary_colour = "#1F538D"
# primary_colour = "#7FC4E7"
primary_colour = "#3A9EE9"
secondary_colour = "#363636"









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

        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'),
                                  width=width-(3.2*height), height=height-4, border_width=0)
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
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            pass

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
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
            value = int(self.entry.get()) - self.step_size
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

        def create_title_frame():
            title_frame = ctk.CTkFrame(master=self,
                                       fg_color="transparent")
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
                                        text_color=primary_colour,
                                        pady=30,
                                        anchor='s'
                                        )
            app_title.pack()

        create_title_frame()

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
         
        bottom_frame = ctk.CTkScrollableFrame(master=self,
                                              border_width=2,
                                                corner_radius=0,
                                                scrollbar_fg_color="#474747",
                                                scrollbar_button_color=primary_colour,
                                                # label_fg_color="red"
                                              )
        bottom_frame.pack(
            padx=20,
            # pady=(0, 20),
            fill="both",
            expand=True,
            )



        # for i in range(20):
        #     self.buttons_label = ctk.CTkLabel(
        #                                         master=bottom_frame,
        #                                         text=("Buttons:"),
        #                                         font=ctk.CTkFont(
        #                                                 family="Roboto",
        #                                                     # weight="bold",
        #                                                 size=42,
        #                                                 ),
        #                                                 # text_color="#1F538D",
        #                                 # pady=30,
        #                                 # anchor='s'
        #                                         )
        #     self.buttons_label.pack()



    def show(self):
        self.pack(fill="both", expand=True)

    def create_edit_page(self, device_dropdown_name):
        self.edit_page = EditPage(self.master, device_name=device_dropdown_name, main_page=self.show)
        self.edit_page.pack_forget()


    def show_edit_page(self):
        # self.create_and_update_device_dropdown()  # Corrected function name and using 'self'
        # self.button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))

        if self.edit_page:
            self.pack_forget()
            self.edit_page.pack(fill="both", expand=True)




class EditPage(ctk.CTkFrame):
    def __init__(self, master, main_page, config_id=None, device_name=None):
        super().__init__(master)
        # print(device_name)


        
        self.master = master
        self.main_page = main_page
        self.config_id = config_id
        self.tap_scroll_action = ctk.StringVar(value="None")



        self.back_button = ctk.CTkButton(self, text="Back to Page 1", command=self.go_back)
        self.back_button.pack(pady=5)
        


        if device_name is not None and config_id == None:
            device_attributes, device_thumbwheel = execute_db_queries.get_new_user_device_attributes(device_name)
        
        elif config_id is not None and device_name == None:
            device_attributes, device_thumbwheel = execute_db_queries.get_existing_device_config(config_id)

        else:
            print("there's an error")
            # TODO: configure the error handling.

    

        


        

        device_name_label = ctk.CTkLabel(master=self,
                                                text=device_attributes._device_name,
                                                font=ctk.CTkFont(
                                                family="Roboto",
                                                weight="bold",
                                                size=40,
                                                    ),
                                                text_color=primary_colour,
                                                pady=(20),

                                    # anchor='s'
                                              )
        device_name_label.pack()



        scroll_features_frame = ctk.CTkFrame(master=self,
                                       fg_color="transparent")
        scroll_features_frame.pack(
                                pady=(30,0),
                                fill="x"
            )

        if device_thumbwheel is not None:
            scrollwheel_frame_text = "Scrollwheels"
        else:
            scrollwheel_frame_text = "Scrollwheel"

        self.general_device_label = ctk.CTkLabel(
                                            master=scroll_features_frame,
                                            text=scrollwheel_frame_text,
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                    weight="bold",
                                                    size=22,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
        self.general_device_label.grid(row=0, column=0)



        if device_attributes._smartshift_support == True:


            self.smartshift_label = ctk.CTkLabel(
                                            master=scroll_features_frame,
                                            text=("SmartShift On"),
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                    # weight="bold",
                                                    size=20,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
            self.smartshift_label.grid(row=1, column=0)


            

            def checkbox_event():
                # TODO: update variable for smartshift 
                if smartshift_enabled_var.get() == "on":
                    is_smartshift_on = True
                else:
                    is_smartshift_on = False                
                print(is_smartshift_on)
                smartshift_threshold.toggle_enable(is_smartshift_on)
                smartshift_torque.toggle_enable(is_smartshift_on)

            
            smartshift_enabled_var = ctk.StringVar(value="on")
            smartshift_checkbox = ctk.CTkCheckBox(master=scroll_features_frame,
                                                    text="",
                                                    command=checkbox_event,
                                                    variable=smartshift_enabled_var,
                                                    onvalue="on",
                                                    offvalue="off",
                                                    checkbox_height=30,
                                                    checkbox_width=30,
                                                    corner_radius=0,
                                                    border_width=3,
                                     )
            smartshift_checkbox.grid(row=1, column=1)





            smartshift_threshold = IntSpinbox(self,
                                    width=150,
                                    step_size=1,
                                    min_value=1,
                                    max_value=255)
            
            smartshift_threshold.set(42) #TODO: Update
            smartshift_threshold.pack(padx=20, pady=20)

            # smartshift_threshold_spinbox = ctk.CTkButton(self, text="Toggle Enable/Disable", command=smartshift_threshold.toggle_enable)
            # smartshift_threshold_spinbox.pack()

            smartshift_torque = IntSpinbox(self,
                                    width=150,
                                    step_size=1,
                                    min_value=1,
                                    max_value=255)
            
            smartshift_torque.set(42) #TODO: Update
            smartshift_torque.pack(padx=20, pady=20)






            






        self.buttons_label = ctk.CTkLabel(
                                            master=self,
                                            text=("Buttons:"),
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                        # weight="bold",
                                                    size=22,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
        self.buttons_label.pack()

        reprogrammable_buttons_array = execute_db_queries.get_reprogrammable_buttons_array(device_attributes._device_id)

        for reprogrammable_button_object in reprogrammable_buttons_array:
            reprogrammable_button_label = ctk.CTkLabel(self, text=reprogrammable_button_object._button_name)
            reprogrammable_button_label.pack()
            # def combobox_callback(choice):
            #     print("combobox dropdown clicked:", choice)

            # combobox = ctk.CTkComboBox(self, values=["option 1", "option 2"],
                                       
            #                          command=combobox_callback)
            # combobox.set("option 2")
            # combobox.pack()
            def optionmenu_callback(choice):
                print("optionmenu dropdown clicked:", choice)

            optionmenu = ctk.CTkOptionMenu(self, values=["option 1", "option 2"],
                                                    command=optionmenu_callback)
            optionmenu.set("option 2")
            optionmenu.pack()

        if device_thumbwheel is not None:
            self.thumbwheel_label = ctk.CTkLabel(
                                                master=self,
                                                text=("Thumbwheel Controls:"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=22,
                                                        ),
                                                        # text_color="#1F538D",
                                        # pady=30,
                                        # anchor='s'
                                                )
            self.thumbwheel_label.pack()

            self.thumbwheel_invert_label = ctk.CTkLabel(self, text="Invert:")
            self.thumbwheel_invert_label.pack()
            
            
            self.thumbwheel_invert = ctk.CTkSwitch(master=self,
                                                   text="",
                                                    onvalue="on", 
                                                    offvalue="off",
                                                    border_width=3,
                                                    # width=200,
                                                    switch_width=40,
                                                    corner_radius=2,
                                                    switch_height=21,
                                                    border_color=("#181818"),
                                                    command=device_thumbwheel.set_invert()

                                                    )
            
            self.thumbwheel_invert.pack()

            self.thumbwheel_divert_label = ctk.CTkLabel(self, text="Divert:")
            self.thumbwheel_divert_label.pack()



            self.thumbwheel_divert = ctk.CTkSwitch(master=self,
                                                   text="",
                                                    onvalue="on", 
                                                    offvalue="off",
                                                    border_width=3,
                                                    # width=200,
                                                    switch_width=40,
                                                    corner_radius=2,
                                                    switch_height=21,
                                                    border_color=("black"),
                                                    command=device_thumbwheel.set_divert_toggle()

                                                    )
            
            self.thumbwheel_divert.pack()


            tap_options = ["None", "Keypress"]


            if device_thumbwheel._tap == True:

                def thumbwheel_tap_updated(new_action):
                    print(f"New tap action: {new_action}!")

                self.tap_label = ctk.CTkLabel(self, text=("Tap:"))
                self.tap_label.pack()

                self.tap_option_menu = ctk.CTkOptionMenu(master=self, 
                                                            variable=self.tap_scroll_action,
                                                            values=tap_options,
                                                            state="normal",
                                                            command=thumbwheel_tap_updated
                                                         )

                self.tap_option_menu.pack()


                # add_device_dropdown = ctk.CTkOptionMenu(master=top_frame,
                #                                     variable=selected_option_var,
                #                                     values=options,
                #                                     state="normal",
                #                                     width=400,
                #                                     height=36,
                #                                     command=device_dropdown)
                

            if device_thumbwheel._proxy == True:
                self.proxy_label = ctk.CTkLabel(self, text=("Proxy:"))
                self.proxy_label.pack()

            if device_thumbwheel._touch == True:
                self.touch_label = ctk.CTkLabel(self, text=("Touch:"))
                self.touch_label.pack()


    def go_back(self):
        self.pack_forget()
        self.main_page()



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

    # Configure logging for the application
    create_app_data.configure_logging()

    # Connect to the SQL database and build the required tables
    create_app_data.initialise_database()

    main_page = MainPage(root)
    main_page.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
