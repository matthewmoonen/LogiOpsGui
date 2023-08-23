import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkListbox import *
import create_app_data
import execute_db_queries
import DeviceData
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
         
        devices_frame = ctk.CTkScrollableFrame(master=self,
                                              border_width=2,
                                                corner_radius=0,
                                                scrollbar_fg_color="#474747",
                                                scrollbar_button_color=primary_colour,
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


        bottom_frame.grid_columnconfigure((0), weight=1)






        
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



        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                MAIN SCROLLABLE FRAME FOR MAIN PAGE

        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """



        settings_scrollable_frame = ctk.CTkScrollableFrame(master=self,
                                              border_width=2,
                                                corner_radius=0,
                                                scrollbar_fg_color="#474747",
                                                scrollbar_button_color=primary_colour,
                                                # label_fg_color="red"
                                              )


        settings_scrollable_frame.pack(
                      padx=20,
            # pady=(0, 20),
            fill="both",
            expand=True,
        )






        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                GENERAL FEATURES HERE

        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """


        general_features_frame = ctk.CTkFrame(master=settings_scrollable_frame,
                                       fg_color="transparent"
                                       )
        general_features_frame.pack(
                                pady=(30,0),
                                fill="x"
            )


        config_name_label = ctk.CTkLabel(
                                        master=general_features_frame,
                                        text=("Configuration Name"),
                                        font=ctk.CTkFont(
                                                family="Roboto",
                                                # weight="bold",
                                                size=14,
                                                ),
                                                # text_color="#1F538D",
                                # pady=30,
                                # anchor='s'
                                        )
        config_name_label.grid(row=0, column=0)



        config_name_textbox = ctk.CTkTextbox(
            master=general_features_frame,
            height=30,
            width=500,
            font=ctk.CTkFont(
                                family="Roboto",
                                # weight="bold",
                                size=16,
                                ),
        )
        config_name_textbox.grid(row=1, column=0)

        config_name_var = config_name_textbox.get(0.0, "end")
        # TODO: Update event handling to save the name of the configuration.



        dpi_label = ctk.CTkLabel(
                                master=general_features_frame,
                                                                    text=("DPI"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=18,
                                                        ),
                                                        # text_color="#1F538D",
                                        # pady=30,
                                        # anchor='s'
        )
        dpi_label.grid(row=2, column=0)



        dpi_spinbox = IntSpinbox(master=general_features_frame,
                                width=200,
                                step_size=100,
                                min_value=400, #TODO: UPDATE
                                max_value=8000 # TODO: UPDATE
                                )
        
        dpi_spinbox.set(1000) #TODO: Update
        dpi_spinbox.grid(row=3, column=0)














        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                SCROLL FEATURES HERE

        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """




        scroll_features_frame = ctk.CTkFrame(master=settings_scrollable_frame,
                                    #    fg_color="transparent"
                                       )
        scroll_features_frame.pack(
                                pady=(30,0),
                                fill="x"
            )

        if device_thumbwheel is not None:
            scrollwheel_frame_text = "Vertical Scrollwheel"
        else:
            scrollwheel_frame_text = "Scrollwheel"

        scrollwheel_main_label = ctk.CTkLabel(
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
        # scrollwheel_main_label.grid(row=0, column=0)
        scrollwheel_main_label.pack()













        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                SMARTSHIFT FEATURES

        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """






        if device_attributes._smartshift_support == True:

            smartshift_frame = ctk.CTkFrame(master=scroll_features_frame,
                                            )
            smartshift_frame.pack()


            self.smartshift_label = ctk.CTkLabel(
                                            master=smartshift_frame,
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
            self.smartshift_label.grid(row=0, column=0)


            

            def checkbox_event():
                # TODO: update variable for smartshift 
                if smartshift_enabled_var.get() == "on":
                    is_smartshift_on = True
                else:
                    is_smartshift_on = False                
                # print(is_smartshift_on)
                smartshift_threshold.toggle_enable(is_smartshift_on)
                smartshift_torque.toggle_enable(is_smartshift_on)


            smartshift_enabled_var = ctk.StringVar(value="on")
            smartshift_checkbox = ctk.CTkCheckBox(master=smartshift_frame,
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




            self.smartshift_threshold_label = ctk.CTkLabel(
                                            master=smartshift_frame,
                                            text=("Threshold"),
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                    # weight="bold",
                                                    size=16,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
            self.smartshift_threshold_label.grid(row=1, column=2)



            smartshift_threshold = IntSpinbox(master=smartshift_frame,
                                    width=150,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255)
            
            smartshift_threshold.set(42) #TODO: Update
            smartshift_threshold.grid(row=2, column=2)

            # smartshift_threshold_spinbox = ctk.CTkButton(self, text="Toggle Enable/Disable", command=smartshift_threshold.toggle_enable)
            # smartshift_threshold_spinbox.pack()


            self.smartshift_torque_label = ctk.CTkLabel(
                                            master=smartshift_frame,
                                            text=("Torque"),
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                    # weight="bold",
                                                    size=18,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
            self.smartshift_torque_label.grid(row=2, column=3)


            smartshift_torque = IntSpinbox(master=smartshift_frame,
                                    width=150,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255)
            
            smartshift_torque.set(42) #TODO: Update
            smartshift_torque.grid(row=2, column=4)








        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                GENERAL SCROLL FEATURES SHARED BY MOST MICE
                
        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """





        common_scrollwheel_features_frame = ctk.CTkFrame(master=scroll_features_frame,
                                        )
        common_scrollwheel_features_frame.pack()

        





        hi_res_scroll_label = ctk.CTkLabel (
                                            master=common_scrollwheel_features_frame,
                                            text=("Hi-Res Scroll"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=18,
                                                        ),
        )
        hi_res_scroll_label.grid(row=2, column=0)
        
        self.hires_scroll_switch = ctk.CTkSwitch(
                                                master=common_scrollwheel_features_frame,
                                                text="",
                                                onvalue="on", 
                                                offvalue="off",
                                                border_width=3,
                                                # width=200,
                                                switch_width=40,
                                                corner_radius=2,
                                                switch_height=21,
                                                border_color=("#181818"),
                                                command=None #TODO: UPDATE

                                                )
        
        self.hires_scroll_switch.grid(row=2, column=1)





        scroll_invert_label = ctk.CTkLabel (
                                            master=common_scrollwheel_features_frame,
                                            text=("Invert Scroll"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=18,
                                                        ),
        )
        scroll_invert_label.grid(row=3, column=0)




        self.scroll_invert_switch = ctk.CTkSwitch(
                                                master=common_scrollwheel_features_frame,
                                                text="",
                                                onvalue="on", 
                                                offvalue="off",
                                                border_width=3,
                                                # width=200,
                                                switch_width=40,
                                                corner_radius=2,
                                                switch_height=21,
                                                border_color=("#181818"),
                                                command=None #TODO: UPDATE

                                                )
        
        self.scroll_invert_switch.grid(row=3, column=1)



        scroll_target_label = ctk.CTkLabel (
                                            master=common_scrollwheel_features_frame,
                                            text=("Target"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=18,
                                                        ),
        )
        scroll_target_label.grid(row=4, column=0)


        self.target_switch = ctk.CTkSwitch(
                                                master=common_scrollwheel_features_frame,
                                                text="",
                                                onvalue="on", 
                                                offvalue="off",
                                                border_width=3,
                                                # width=200,
                                                switch_width=40,
                                                corner_radius=2,
                                                switch_height=21,
                                                border_color=("#181818"),
                                                command=None #TODO: UPDATE

                                                )
        
        self.target_switch.grid(row=4, column=1)

        

        scroll_speed_title_label = ctk.CTkLabel (
                                            master=common_scrollwheel_features_frame,
                                            text=("Scroll Speed (Axis Multiplier)"),
                                                font=ctk.CTkFont(
                                                        family="Roboto",
                                                            # weight="bold",
                                                        size=18,
                                                        ),
        )
        scroll_speed_title_label.grid(row=5, column=0)




        scroll_up_equals_scroll_down = True # TODO: update logic for  this.

        def handle_equal_unequal_vertical_scroll_speed():
            print(up_down_scrollspeed_equal_var.get())
            if up_down_scrollspeed_equal_var.get() == "on":
                scroll_speed_up_slider.grid_forget()
                scroll_speed_up_value_label.grid_forget()
            else:
                scroll_speed_up_slider.grid(row=9, column=0)
                scroll_speed_up_value_label.grid(row=10, column=0)
  

        up_down_scrollspeed_equal_var = ctk.StringVar(value="on")
        smartshift_checkbox = ctk.CTkCheckBox(master=common_scrollwheel_features_frame,
                                                text="",
                                                command=handle_equal_unequal_vertical_scroll_speed,
                                                variable=up_down_scrollspeed_equal_var,
                                                onvalue="on",
                                                offvalue="off",
                                                checkbox_height=30,
                                                checkbox_width=30,
                                                corner_radius=0,
                                                border_width=3,
                                    )
        smartshift_checkbox.grid(row=6, column=0)



        scroll_speed_value = 20.0
        def slider_event(value):
            global scroll_speed_value  # Use the global keyword to modify the global variable
            scroll_speed_value = value
            scroll_speed_value_label.configure(text=scroll_speed_value)  # Update the label text

        # Create the GUI components
        scroll_speed_slider = ctk.CTkSlider(master=common_scrollwheel_features_frame,
                                            from_=0,
                                            to=100, 
                                            number_of_steps=1000,
                                            command=slider_event)
        scroll_speed_slider.set(scroll_speed_value)  # Set the initial value of the slider
        scroll_speed_slider.grid(row=7, column=0)

        scroll_speed_value_label = ctk.CTkLabel(
            master=common_scrollwheel_features_frame,
            text=str(scroll_speed_value),
            font=ctk.CTkFont(
                family="Roboto",
                size=18,
            ),
        )
        
        
        scroll_speed_value_label.grid(row=8, column=0)





        scroll_speed_up_value = 20.0
        def up_slider_event(value):
            global scroll_speed_up_value  # Use the global keyword to modify the global variable
            scroll_speed_up_value = value
            scroll_speed_up_value_label.configure(text=scroll_speed_up_value)  # Update the label text

        scroll_speed_up_slider = ctk.CTkSlider(master=common_scrollwheel_features_frame,
                                            from_=0,
                                            to=100, 
                                            number_of_steps=1000,
                                            command=up_slider_event)
        scroll_speed_up_slider.set(scroll_speed_up_value)  # Set the initial value of the slider
        scroll_speed_up_slider.grid(row=9, column=0)

        scroll_speed_up_value_label = ctk.CTkLabel(
            master=common_scrollwheel_features_frame,
            text=str(scroll_speed_up_value),
            font=ctk.CTkFont(
                family="Roboto",
                size=18,
            ),
        )
        scroll_speed_up_value_label.grid(row=10, column=0)



        
        # TODO: create class - see here https://chat.openai.com/share/8d6e30d1-cac0-4e08-a51f-935e04ae582d




        

        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                THUMBWHEEL(IF PRESENT)
                
        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """


        thumbwheel_frame = ctk.CTkFrame(master=scroll_features_frame,
                                        )
        thumbwheel_frame.pack()



        if device_thumbwheel is not None:



            self.thumbwheel_label = ctk.CTkLabel(
                                                master=thumbwheel_frame,
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
            self.thumbwheel_label.grid(row=0, column=0)

            self.thumbwheel_invert_label = ctk.CTkLabel(thumbwheel_frame, text="Invert:")
            self.thumbwheel_invert_label.grid(row=1, column=0)
            
            
            self.thumbwheel_invert = ctk.CTkSwitch(
                                                    master=thumbwheel_frame,
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
            
            self.thumbwheel_invert.grid(row=2, column=0)

            self.thumbwheel_divert_label = ctk.CTkLabel(master=thumbwheel_frame, text="Divert:")
            self.thumbwheel_divert_label.grid(row=1, column=1)



            self.thumbwheel_divert = ctk.CTkSwitch(
                                                    master=thumbwheel_frame,

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
            
            self.thumbwheel_divert.grid(row=2, column=1)


            tap_touch_proxy_options = ['Do Nothing', 'Keypress', 'Toggle SmartShift', 'Cycle DPI', 'Change Host']
            if device_attributes._smartshift_support != True:
                tap_touch_proxy_options.remove("Toggle SmartShift")



            if device_thumbwheel._tap == True:

                self.tap_label = ctk.CTkLabel(master=thumbwheel_frame, text=("Tap:"))
                self.tap_label.grid(row=3, column=0)

                thumbwheel_tap_tabview = ctk.CTkTabview(master=thumbwheel_frame,
                                                        height=0)
                thumbwheel_tap_tabview.grid(row=4, column=0)

                for i in tap_touch_proxy_options:
                    thumbwheel_tap_tabview.add(i)  

                thumbwheel_tap_tabview.set("Do Nothing")  # set currently visible tab TODO: update this to match DB value
                
                    

            if device_thumbwheel._proxy == True:
                proxy_label = ctk.CTkLabel(thumbwheel_frame, text=("Proxy:"))
                proxy_label.grid(row=5, column=0)

                thumbwheel_proxy_tabview = ctk.CTkTabview(master=thumbwheel_frame,
                                                          height=0)
                thumbwheel_proxy_tabview.grid(row=6, column=0)

                for i in tap_touch_proxy_options:
                    thumbwheel_proxy_tabview.add(i)  

                thumbwheel_proxy_tabview.set("Do Nothing")  # set currently visible tab TODO: update this to match DB value
                

            if device_thumbwheel._touch == True:

                touch_label = ctk.CTkLabel(thumbwheel_frame, text=("Touch:"))
                touch_label.grid(row=7, column=0)

                thumbwheel_touch_tabview = ctk.CTkTabview(master=thumbwheel_frame,
                                                          height=0)
                thumbwheel_touch_tabview.grid(row=8, column=0)

                for i in tap_touch_proxy_options:
                    thumbwheel_touch_tabview.add(i)  

                thumbwheel_touch_tabview.set("Do Nothing")  # set currently visible tab TODO: update this to match DB value
                


























            






        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        *******************************************************************************

                BUTTON CONFIGS HERE
                
        *******************************************************************************
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """





        reprogrammable_buttons_array = execute_db_queries.get_reprogrammable_buttons_array(device_attributes._device_id)

        self.buttons_label = ctk.CTkLabel(
                                            master=settings_scrollable_frame,
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


        buttons_frame = ctk.CTkFrame(master=settings_scrollable_frame,
                                       fg_color="transparent")
        buttons_frame.pack(
                                pady=(30,0),
                                fill="x"
            )





        for index, reprogrammable_button_object in enumerate(reprogrammable_buttons_array):
            reprogrammable_button_label = ctk.CTkLabel(master=buttons_frame, text=reprogrammable_button_object._button_name)
            
            
            def get_column(i):
                return 1 if i % 2 == 0 else 0
            row = index//2
            column = get_column(index)

            reprogrammable_button_label.grid(row=row, column=column)
            # def combobox_callback(choice):
            #     print("combobox dropdown clicked:", choice)

            # combobox = ctk.CTkComboBox(self, values=["option 1", "option 2"],
                                       
            #                          command=combobox_callback)
            # combobox.set("option 2")
            # combobox.pack()
            def optionmenu_callback(choice):
                print("optionmenu dropdown clicked:", choice)
                print(thumbwheel_touch_tabview.get())

            optionmenu = ctk.CTkOptionMenu(master=settings_scrollable_frame, values=["option 1", "option 2"],
                                                    command=optionmenu_callback)
            optionmenu.set("option 2")
            optionmenu.pack()



    
        bottom_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        bottom_frame.pack()

        self.back_button = ctk.CTkButton(master=bottom_frame, 
                                            text="Cancel",
                                            command=self.go_back)
        self.back_button.pack(pady=20)




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
