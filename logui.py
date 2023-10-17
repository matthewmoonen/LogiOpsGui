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
import Classes
from CTkMessagebox import CTkMessagebox
import inspect





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
            self.selected_device = new_device

            button_for_adding_devices.configure(state="normal", fg_color="#208637")
            button_for_adding_devices.configure(
                command=add_device_button_clicked
                ) 

        def add_device_button_clicked():

            button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))
            new_configuration_id = execute_db_queries.add_new_device(self.selected_device)
            self.edit_configuration(configuration_id=new_configuration_id, is_new_device=True, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame, create_and_update_device_dropdown=create_and_update_device_dropdown)

            for widget in devices_scrollable_frame.winfo_children():
                widget.destroy()
            create_devices_inner_frame()

            create_and_update_device_dropdown()


        def create_and_update_device_dropdown():

            options = execute_db_queries.get_unconfigured_devices()
            selected_option_var = ctk.StringVar(value='   Select Device To Add')
            add_device_dropdown = ctk.CTkOptionMenu(master=top_frame,
                                                    variable=selected_option_var,
                                                    values=options,
                                                    state="normal",
                                                    width=400,
                                                    height=40,
                                                    corner_radius=6.5,
                                                    dropdown_font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=20,
                                                            
                                                            ),
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
                                        hover_color=("#28A745")
                                        )
            
        button_for_adding_devices.grid(
                                        padx=(20,20),
                                        row=0,
                                        column=2,
                                        )
        
        create_and_update_device_dropdown()
   

        devices_scrollable_frame = ctk.CTkScrollableFrame(master=self,
                                              border_width=3,
                                              border_color=gui_variables.secondary_colour,
                                                corner_radius=0,
                                                scrollbar_fg_color=gui_variables.secondary_colour,
                                                scrollbar_button_color=gui_variables.primary_colour,
                                                # label_fg_color="red"
                                              )
        devices_scrollable_frame.pack(
            padx=0,
            # pady=(0, 20),
            fill="both",
            expand=True,
            )



        selected_configurations = {}



        def create_devices_inner_frame():


            # Calling destroy() and then rebuilding the CTkScrollableFrame creates various issues. This is an inner frame that can be manipulated more easily
            devices_inner_frame = ctk.CTkFrame(master=devices_scrollable_frame)
            devices_inner_frame.pack(padx=0, pady=0, fill="both", expand=True)
            # self.devices_inner_frame = devices_inner_frame

            def refresh_devices_inner_frame():
                # Destroy the full frame of devices and configurations and then recursively call the function to recreate 
                devices_inner_frame.destroy()
                create_devices_inner_frame()
            

            def create_config_ui(device_id, configuration, device_configs_frame, grid_x_position):

                config_frame = ctk.CTkFrame(master=device_configs_frame)
                config_frame.pack(fill="x", expand=True,)

                radio_button = ctk.CTkRadioButton(master=config_frame,
                                                text=f"{configuration.configuration_name}",
                                                variable=selected_configurations[device_id],
                                                value=str(configuration.configuration_id),
                                                command=lambda c=configuration, d=device_id: select_configuration(c, d),
                                                radiobutton_width=24.5,
                                                radiobutton_height=24.5,
                                                corner_radius=2.5,
                                                border_width_unchecked=6,
                                                border_width_checked=6,
                                                hover_color=gui_variables.primary_colour
                                                )

                radio_button.grid(row=grid_x_position, column=0, sticky="w")


                edit_configuration_button = ctk.CTkButton(
                    master=config_frame,
                    height=40,
                    width=120,
                    text="Edit Configuration",
                    command=lambda: self.edit_configuration(configuration.configuration_id, devices_scrollable_frame, create_devices_inner_frame)
                )
                edit_configuration_button.grid(row=grid_x_position, column=1, sticky="e")

                delete_configuration_button = ctk.CTkButton(
                    master=config_frame,
                    height=40,
                    width=120,
                    text="Delete Configuration",
                    command=lambda c=configuration.configuration_id, f=config_frame, s=configuration.is_selected: configuration_deletion_warning(c, f, s)
                )
                delete_configuration_button.grid(row=grid_x_position, column=2, sticky="e")

            def select_configuration(configuration, device_id):
                selected_configurations[device_id] = configuration.configuration_id
                execute_db_queries.update_selected_configuration(configuration.configuration_id)

            def create_device_ui(device, row=None):

                device_frame = ctk.CTkFrame(master=devices_inner_frame)
                device_frame.pack(fill="both", expand=True)

                device_label = ctk.CTkLabel(master=device_frame,
                                            text=device.device_name,
                                            font=ctk.CTkFont(
                                                family="Roboto",
                                                weight="bold",
                                                size=20,
                                                
                                            ),
                                            )
                
                device_label.pack()

                devicewide_actions_frame = ctk.CTkFrame(
                    master=device_frame,
                )
                devicewide_actions_frame.pack(
                    fill="x", 
                    expand=False)

                new_configuration_button = ctk.CTkButton(master=devicewide_actions_frame,
                                                         text="Add Configuration",
                                                         command=lambda d=device.device_id, n=device.device_name: add_new_configuration(d, n))
                new_configuration_button.grid(row=0, column=0)


                delete_device_button = ctk.CTkButton(master=devicewide_actions_frame,
                                                     text="Delete Device",
                                                    command=lambda d=device.device_id, f=device_frame: device_deletion_warning(d, f)
                                                     )
                delete_device_button.grid(row=0, column=1)

                device_configs_frame = ctk.CTkFrame(master=device_frame)
                device_configs_frame.pack(fill="x")

                for configuration in device.configurations:
                    # Loop through once and find the selected configuration to store in the dictionary
                    if configuration.is_selected == True:
                        selected_configurations[device.device_id] = ctk.StringVar()
                        selected_configurations[device.device_id].set(str(configuration.configuration_id))

                for row, configuration in enumerate(device.configurations):
                    # 
                    create_config_ui(device.device_id, configuration, device_configs_frame, row)

                return device_frame


            def add_new_configuration(device_id, device_name):
                newest_configuration_id = execute_db_queries.new_empty_configuration(device_id, device_name)
                self.edit_configuration(configuration_id = newest_configuration_id, is_new_config=True, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame)
                for widget in devices_scrollable_frame.winfo_children():
                    widget.destroy()
                create_devices_inner_frame()



            def configuration_deletion_warning(configuration_id, config_frame, is_selected):
                msg = CTkMessagebox(title="Delete Device?",
                                    message="Delete configuration?",
                                    option_1="Delete",
                                    option_2="Cancel",
                                    width=600,
                                    height=300,
                                    fade_in_duration=200
                                    )
                if msg.get() == "Delete":
                    if is_selected == True:
                        execute_db_queries.delete_configuration(configuration_id)
                        devices_inner_frame.destroy()
                        create_devices_inner_frame()
                    else:
                        config_frame.destroy()
                        execute_db_queries.delete_configuration(configuration_id)

            def device_deletion_warning(device_id, device_frame):
                msg = CTkMessagebox(title="Delete Device?",
                                    message="Deleting device will also delete all its configurations.",
                                    option_1="Delete",
                                    option_2="Cancel",
                                    width=600,
                                    height=300,
                                    fade_in_duration=200
                                    )
                if msg.get() == "Delete":
                    device_frame.destroy()
                    execute_db_queries.delete_device(device_id)
                    create_and_update_device_dropdown()


            user_devices_and_configs = Classes.get_main_page_user_devices()


            for device in user_devices_and_configs:

                create_device_ui(device)

        create_devices_inner_frame()

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


    def edit_configuration(self, 
                           configuration_id,
                            devices_scrollable_frame=None,
                            create_devices_inner_frame=None,
                            create_and_update_device_dropdown=None,
                            is_new_device=False,
                            is_new_config=False,
                           ):

        configuration = Classes.DeviceConfig.create_from_configuration_id(configuration_id)

        self.edit_page = EditPage(self.master, configuration=configuration, is_new_config=is_new_config, is_new_device=is_new_device, main_page=self, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame, create_and_update_device_dropdown=create_and_update_device_dropdown, show_main_page=self.show)
        
        self.pack_forget()
        
        self.edit_page.pack(fill="both", expand=True)
        
    def show(self):
        self.pack(fill="both", expand=True)

    def show_edit_page(self):
        if self.edit_page:
            self.pack_forget()
            self.edit_page.pack(fill="both", expand=True)



class EditPage(ctk.CTkFrame):
    def __init__(self, master, show_main_page, main_page, configuration=None,
                 devices_scrollable_frame = None,
                 create_devices_inner_frame= None,
                 create_and_update_device_dropdown=None,
                is_new_device=False,
                is_new_config=False
                 ):
        super().__init__(master)


        self.master = master
        self.show_main_page = show_main_page



        device_name_label = ctk.CTkLabel(master=self,
                                                text=configuration.device_name,
                                                font=ctk.CTkFont(
                                                family="Roboto",
                                                weight="bold",
                                                size=40,
                                                    ),
                                                text_color=gui_variables.primary_colour,
                                                pady=(20),

                                    # anchor='s'
                                                )
        device_name_label.pack()

        edit_page_scrollable_frame = ctk.CTkScrollableFrame(master=self, )
        edit_page_scrollable_frame.pack(fill="both", expand=True)


        # def device_configuration_widgets():
        
        def focus_next_widget(event):
            # Make TAB key push focus to next widget rather than inserting tabs
            current_widget = event.widget
            next_widget = current_widget.tk_focusNext() 
            
            if next_widget:
                next_widget.focus_set()
            return "break"  # Prevent the tab from inserting a tab character


        def update_config_name_in_db(event):
            # Update the DB on focus out from the textbox

            if configuration_name_textbox.get("1.0", "end-1c").strip() == "": #Prevent empty configuration name being inserted
                configuration_name_textbox.insert("0.0", configuration.configuration_name)
            
            elif configuration_name_textbox.get("1.0", "end-1c").strip() == configuration.configuration_name:
                pass
            else:
                config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
                configuration.configuration_name = config_name_stripped
                configuration_name_textbox.delete("0.0", "end")
                configuration_name_textbox.insert("0.0", config_name_stripped)
                
                # TODO: make this target the desired widget more specifically. Now it's
                for widget in devices_scrollable_frame.winfo_children():
                    widget.destroy()
                create_devices_inner_frame()

        configuration_name_label = ctk.CTkLabel(master=edit_page_scrollable_frame,
                                                text="Configuration Name",
                                                )
        configuration_name_label.pack()

        configuration_name_textbox = ctk.CTkTextbox(master=edit_page_scrollable_frame,
                                                    height=10,
                                                    width=500,
                                                    corner_radius=1
                                                    )
        configuration_name_textbox.pack()

        configuration_name_textbox.insert("0.0", configuration.configuration_name)

        configuration_name_textbox.bind("<Tab>", focus_next_widget)
        configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)




        dpi_spinbox = IntSpinbox(master=edit_page_scrollable_frame,
                                            width=200,
                                            step_size=50,
                                            min_value=configuration.min_dpi,
                                            max_value=configuration.max_dpi
                                            )
        # device_configuration_widgets()

        def create_dpi_widgets():

            dpi_label = ctk.CTkLabel(
                                    master=edit_page_scrollable_frame,
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
            dpi_label.pack()

            
            dpi_spinbox.set(configuration.dpi) #TODO: Update
            dpi_spinbox.pack()

        create_dpi_widgets()


        if configuration.smartshift_support == True:

            smartshift_options_label = ctk.CTkLabel(
                                    master=edit_page_scrollable_frame,
                                                                        text=("SmartShift Options"),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=18,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            smartshift_options_label.pack()

            smartshift_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
            smartshift_frame.pack(fill="y")


            def smartshift_checkbox_toggled():
                configuration.smartshift_on = not(configuration.smartshift_on)

            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = ctk.CTkCheckBox(master=smartshift_frame, text="SmartShift On", command=smartshift_checkbox_toggled,
                                                variable=check_var, onvalue=True, offvalue=False)
            checkbox.grid(row=0, column=0)

            
            smartshift_threshold_label = ctk.CTkLabel(
                                    master=smartshift_frame,
                                                                        text=("SmartShift Threshold"),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=12,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            smartshift_threshold_label.grid(row=0, column=1)

            smartshift_threshold_spinbox = IntSpinbox(master=smartshift_frame,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    )
            
            smartshift_threshold_spinbox.set(configuration.smartshift_threshold) #TODO: Update
            smartshift_threshold_spinbox.grid(row=1, column=1)



            smartshift_torque_label = ctk.CTkLabel(
                                    master=smartshift_frame,
                                                                        text=("SmartShift Torque"),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=12,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            smartshift_torque_label.grid(row=0, column=2)

            smartshift_torque_spinbox = IntSpinbox(master=smartshift_frame,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    )
            
            smartshift_torque_spinbox.set(configuration.smartshift_torque) #TODO: Update
            smartshift_torque_spinbox.grid(row=1, column=2)

            # TODO: Smartshift threshold, smartshift torque


        if configuration.hires_scroll_support == True:

            hiresscroll_options_label = ctk.CTkLabel(
                                    master=edit_page_scrollable_frame,
                                                                        text=("HiRes Scroll Options"),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=18,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            hiresscroll_options_label.pack()


            hiresscroll_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
            hiresscroll_frame.pack()


            def hiresscroll_hires_toggle():
                configuration.hiresscroll_hires = not(configuration.hiresscroll_hires)


            hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
            hirescroll_hires_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="HiRes Scroll On", command=hiresscroll_hires_toggle,
                                                variable=hiresscroll_hires_var, onvalue=True, offvalue=False)
            hirescroll_hires_checkbox.grid(row=0, column=0)


            def hiresscroll_invert_toggle():
                configuration.hiresscroll_invert = not(configuration.hiresscroll_invert)


            hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
            hirescroll_invert_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll Invert", command=hiresscroll_invert_toggle,
                                                variable=hiresscroll_invert_var, onvalue=True, offvalue=False)
            hirescroll_invert_checkbox.grid(row=0, column=1)


            def hiresscroll_target_toggle():
                configuration.hiresscroll_target = not(configuration.hiresscroll_target)

            hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
            hirescroll_target_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll target", command=hiresscroll_target_toggle,
                                                variable=hiresscroll_target_var, onvalue=True, offvalue=False)
            hirescroll_target_checkbox.grid(row=0, column=2)



        if configuration.has_scrollwheel == True:
            
            scroll_properties = Classes.ScrollProperties.create_from_configuration_id(configuration.configuration_id)

            if configuration.has_thumbwheel == True:
                scrollwheel_label_text = "Vertical Scrollwheel"
            else:
                scrollwheel_label_text = "Scrollwheel"

            scrollwheel_label = ctk.CTkLabel(
                                    master=edit_page_scrollable_frame,
                                                                        text=(scrollwheel_label_text),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=18,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            scrollwheel_label.pack()


            vertical_scrollwheel_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
            vertical_scrollwheel_frame.pack()

            scrollwheel_up_threshold_label = ctk.CTkLabel(
                master= vertical_scrollwheel_frame,
                text = "Scrollwheel Up Threshold"
            )
            scrollwheel_up_threshold_label.grid(row=0, column=0)

            scrollwheel_up_spinbox = IntSpinbox(master=vertical_scrollwheel_frame,
                                    width=200,
                                    step_size=5,
                                    min_value=1,
                                    max_value=9999
                                    )
            
            scrollwheel_up_spinbox.set(scroll_properties.scroll_up_threshold)
            scrollwheel_up_spinbox.grid(row=1, column=0)

            scrollwheel_up_mode_label = ctk.CTkLabel(
                master=vertical_scrollwheel_frame,
                text = "Scrollwheel Up Mode"
            )
            scrollwheel_up_mode_label.grid(row=0,column=1)

            def update_scroll_up_mode(new_mode):
                scroll_properties.scroll_up_mode = new_mode

            scroll_up_mode_dropdown = ctk.CTkOptionMenu(master=vertical_scrollwheel_frame,
                                                    variable=ctk.StringVar(value=scroll_properties.scroll_up_mode),
                                                    values=["OnInterval", "OnThreshold"],
                                                    state="normal",
                                                    width=200,
                                                    height=36,
                                                    command=update_scroll_up_mode)
            scroll_up_mode_dropdown.grid(row=1, column=1)



            scrollwheel_down_threshold_label = ctk.CTkLabel(
                master=vertical_scrollwheel_frame,
                text = "Scrollwheel Down Threshold"
            )
            scrollwheel_down_threshold_label.grid(row=0, column=2)

            scrollwheel_down_spinbox = IntSpinbox(master=vertical_scrollwheel_frame,
                                    width=200,
                                    step_size=5,
                                    min_value=1,
                                    max_value=9999
                                    )
            
            scrollwheel_down_spinbox.set(scroll_properties.scroll_down_threshold)
            scrollwheel_down_spinbox.grid(row=1, column=2)

            scrollwheel_down_mode_label = ctk.CTkLabel(
                master=vertical_scrollwheel_frame,
                text = "Scrollwheel Down Mode"
            )
            scrollwheel_down_mode_label.grid(row=0, column=3)

            def update_scroll_down_mode(new_mode):
                scroll_properties.scroll_down_mode = new_mode

            scroll_down_mode_dropdown = ctk.CTkOptionMenu(master=vertical_scrollwheel_frame,
                                                    variable=ctk.StringVar(value=scroll_properties.scroll_down_mode),
                                                    values=["OnInterval", "OnThreshold"],
                                                    state="normal",
                                                    width=200,
                                                    height=36,
                                                    command=update_scroll_down_mode)
            scroll_down_mode_dropdown.grid(row=1, column=3)






        if configuration.has_thumbwheel == True:
            thumbwheel_label = ctk.CTkLabel(
                                    master=edit_page_scrollable_frame,
                                                                        text=("Thumbwheel"),
                                                    font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=18,
                                                            ),
                                                            # text_color="#1F538D",
                                            # pady=30,
                                            # anchor='s'
            )
            thumbwheel_label.pack()


            thumbwheel_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
            thumbwheel_frame.pack()

            
            def thumbwheel_divert_event():
                configuration.thumbwheel_divert = not(configuration.thumbwheel_divert)


            thumbwheel_divert_var = ctk.BooleanVar(value=configuration.thumbwheel_divert)
            thumbwheel_divert_checkbox = ctk.CTkCheckBox(master=thumbwheel_frame, text="Thumbwheel Divert", command=thumbwheel_divert_event,
                                                variable=thumbwheel_divert_var, onvalue=True, offvalue=False)
            thumbwheel_divert_checkbox.grid(row=0, column=0)


            def thumbwheel_invert_event():
                configuration.thumbwheel_invert = not(configuration.thumbwheel_invert)


            thumbwheel_invert_var = ctk.BooleanVar(value=configuration.thumbwheel_invert)
            thumbwheel_invert_checkbox = ctk.CTkCheckBox(master=thumbwheel_frame, text="Thumbwheel Invert", command=thumbwheel_invert_event,
                                                variable=thumbwheel_invert_var, onvalue=True, offvalue=False)
            thumbwheel_invert_checkbox.grid(row=0, column=1)



            thumbwheel_left_threshold_label = ctk.CTkLabel(
                master= thumbwheel_frame,
                text = "Thumbwheel Left Threshold"
            )
            thumbwheel_left_threshold_label.grid(row=1, column=0)

            thumbwheel_left_spinbox = IntSpinbox(master=thumbwheel_frame,
                                    width=200,
                                    step_size=5,
                                    min_value=1,
                                    max_value=9999
                                    )
            
            thumbwheel_left_spinbox.set(scroll_properties.scroll_left_threshold)
            thumbwheel_left_spinbox.grid(row=2, column=0)

            thumbwheel_left_mode_label = ctk.CTkLabel(
                master= thumbwheel_frame,
                text = "Thumbwheel Left Mode"
            )
            thumbwheel_left_mode_label.grid(row=1, column=1)

            def update_scroll_left_mode(new_mode):
                scroll_properties.scroll_left_mode = new_mode

            scroll_left_mode_dropdown = ctk.CTkOptionMenu(master=thumbwheel_frame,
                                                    variable=ctk.StringVar(value=scroll_properties.scroll_left_mode),
                                                    values=["OnInterval", "OnThreshold"],
                                                    state="normal",
                                                    width=200,
                                                    height=36,
                                                    command=update_scroll_left_mode)
            scroll_left_mode_dropdown.grid(row=2, column=1)














            thumbwheel_right_threshold_label = ctk.CTkLabel(
                master= thumbwheel_frame,
                text = "Thumbwheel Right Threshold"
            )
            thumbwheel_right_threshold_label.grid(row=1, column=2)

            thumbwheel_right_spinbox = IntSpinbox(master=thumbwheel_frame,
                                    width=200,
                                    step_size=5,
                                    min_value=1,
                                    max_value=9999
                                    )
            
            thumbwheel_right_spinbox.set(scroll_properties.scroll_right_threshold)
            thumbwheel_right_spinbox.grid(row=2, column=2)

            thumbwheel_right_mode_label = ctk.CTkLabel(
                master= thumbwheel_frame,
                text = "Thumbwheel Right Mode"
            )
            thumbwheel_right_mode_label.grid(row=1, column=3)

            def update_scroll_right_mode(new_mode):
                scroll_properties.scroll_right_mode = new_mode

            scroll_right_mode_dropdown = ctk.CTkOptionMenu(master=thumbwheel_frame,
                                                    variable=ctk.StringVar(value=scroll_properties.scroll_right_mode),
                                                    values=["OnInterval", "OnThreshold"],
                                                    state="normal",
                                                    width=200,
                                                    height=36,
                                                    command=update_scroll_right_mode)
            scroll_right_mode_dropdown.grid(row=2, column=3)






        buttons_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
        buttons_frame.pack()
        for button in configuration.buttons:
            button_label = ctk.CTkLabel(master=buttons_frame, text=f"{button.button_name} ({button.button_cid})")            
            button_label.pack()

        







        bottom_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        bottom_frame.pack()



        back_button = ctk.CTkButton(master=bottom_frame, 
                                            text="Back",
                                            command=lambda: [self.go_back(), update_spinboxes_in_db(), update_config_file_name_test()])
        back_button.pack(pady=20)


        if is_new_device == True:
            print(devices_scrollable_frame)
            cancel_button_new_device = ctk.CTkButton(master=bottom_frame,
                                      text="Cancel Adding Device",
                                      command=lambda d=configuration.device_id, s=devices_scrollable_frame, c=create_devices_inner_frame, u=create_and_update_device_dropdown: self.go_back_dont_save_new_device(d, s, c, u)
                                      )
            cancel_button_new_device.pack(pady=20)
            # print(configuration.device_id)
        elif is_new_config == True:
            # print(configuration.configuration_id)
            print(devices_scrollable_frame)
            cancel_button_new_config = ctk.CTkButton(master=bottom_frame,
                                                     text="Cancel Adding Config",
                                                     command=lambda i=configuration.configuration_id, s=devices_scrollable_frame, c=create_devices_inner_frame: self.go_back_dont_save_new_config(i, s, c)
                                                     )
            cancel_button_new_config.pack(pady=20)


        def update_config_file_name_test():
            print("test")
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            configuration.configuration_name = config_name_stripped
            for widget in devices_scrollable_frame.winfo_children():
                widget.destroy()
            create_devices_inner_frame()
            # print(configuration_name_textbox.get("1.0", "end-1c").strip())

        def update_spinboxes_in_db():
            configuration.dpi = dpi_spinbox.get()
            if configuration.smartshift_support == True:
                configuration.smartshift_threshold = smartshift_threshold_spinbox.get()
                configuration.smartshift_torque = smartshift_torque_spinbox.get()
            if configuration.has_scrollwheel == True:
                scroll_properties.scroll_up_threshold = scrollwheel_up_spinbox.get()
                scroll_properties.scroll_down_threshold = scrollwheel_down_spinbox.get()
            if configuration.has_thumbwheel == True:
                scroll_properties.scroll_left_threshold = thumbwheel_left_spinbox.get()
                scroll_properties.scroll_right_threshold = thumbwheel_right_spinbox.get()

    def go_back_dont_save_new_device(self, device_id, devices_scrollable_frame, create_devices_inner_frame, create_and_update_device_dropdown):
        execute_db_queries.delete_device(device_id)
        print(devices_scrollable_frame)
        for widget in devices_scrollable_frame.winfo_children():
            widget.destroy()
        create_devices_inner_frame()
        create_and_update_device_dropdown()
        self.pack_forget()
        self.show_main_page()
        
    def go_back_dont_save_new_config(self, configuration_id, devices_scrollable_frame, create_devices_inner_frame):

        execute_db_queries.delete_configuration(configuration_id)
        # TODO: this can be achieved more gracefully; the frame for the configuration can be passed in and removed, rather than refreshing the whole page
        for widget in devices_scrollable_frame.winfo_children():
            widget.destroy()
        create_devices_inner_frame()
        self.pack_forget()
        self.show_main_page()

    def go_back(self):
        self.pack_forget()
        self.show_main_page()



def setup_gui(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1280x1280")
    root.resizable(True, True)
    root.title("LogiOpsGUI")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

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
