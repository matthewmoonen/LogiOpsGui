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
import time
import threading
import Classes2




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

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand TODO: Fix repeats here
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


# class MainPageDevice(ctk.CTkFrame):
#     def __init__(self, parent, title, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.title = title
#         self.create_widgets()

#     def create_widgets():
#         label = ctk.CTkLabel




# class SplashScreen(ctk.CTkFrame):
#     def __init__(self, *args, **kwargs, ):
#         super().__init__(*args, **kwargs)


class MainPageRightPanel(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        pass




class MainPage(ctk.CTkFrame):
    def __init__(self, 
                 master):
        super().__init__(master)

        self.edit_page = None
        self.selected_device = None


        left_frame = ctk.CTkFrame(master=self, fg_color="#2B2B2B")
        left_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Set the weight of the row in the main frame


        app_title = ctk.CTkLabel(
            master=left_frame,
            text="LogiOpsGUI",
            font=ctk.CTkFont(
                # family="Roboto",
                # family="Source Code Pro",
                family="Noto Sans",
                # weight="bold",
                size=44),
            text_color=gui_variables.primary_colour,
            pady=20,
            # padx=40,
            corner_radius=0
            # anchor='s'
        )
        app_title.grid(row=0, column=0, columnspan=2, sticky="ew")



        def device_dropdown(new_device):
            self.selected_device = new_device
            button_for_adding_devices.configure(state="normal", fg_color="#198754")
            button_for_adding_devices.configure(
                command=add_device_button_clicked
                ) 

        def add_device_button_clicked():

            button_for_adding_devices.configure(state="disabled",
                                                #  fg_color=("#545B62"),
                                                fg_color=gui_variables.secondary_colour
                                                 )
            new_configuration_id = execute_db_queries.add_new_device(self.selected_device)
            self.edit_configuration(configuration_id=new_configuration_id, is_new_device=True, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame, create_and_update_device_dropdown=create_and_update_device_dropdown)

            for widget in devices_scrollable_frame.winfo_children():
                widget.destroy()
            create_devices_inner_frame()

            create_and_update_device_dropdown()



        def create_and_update_device_dropdown():

            options = execute_db_queries.get_unconfigured_devices()
            selected_option_var = ctk.StringVar(value='Select Device To Add')
            add_device_dropdown = ctk.CTkOptionMenu(master=left_frame,
                                                    variable=selected_option_var,
                                                    values=options,
                                                    state="normal",
                                                    width=230,
                                                    height=35,
                                                    corner_radius=4.5,
                                                    button_color=gui_variables.secondary_colour,
                                                    dropdown_fg_color="#212121",
                                                    dropdown_text_color="#D6D6D6",
                                                    dropdown_hover_color="#1F538D",
                                                    text_color="#D6D6D6",
                                                    font=ctk.CTkFont(
                                                        family="Noto Sans",
                                                        size=14,
                                                    ),
                                                    # corner_radius=2,
                                                    dropdown_font=ctk.CTkFont(
                                                            family="Noto Sans",
                                                                # weight="bold",
                                                            size=16,
                                                            ),
                                                    command=device_dropdown)
            add_device_dropdown.grid(row=1,
                                    column=0,
                                    pady=20,
                                    padx=(15,0),
                                    sticky="w",
                                    )



        button_for_adding_devices = ctk.CTkButton(master=left_frame,
                                        height=37,
                                        width=140,
                                        state="disabled",
                                        text="Add Device",
                                        text_color="white",
                                        text_color_disabled=("#9FA5AB"),
                                        # fg_color=("#545B62"),\
                                        fg_color=gui_variables.secondary_colour,
                                        hover_color=("#28A745"),
                                        font=ctk.CTkFont(
                                            size=14,
                                            # family="Open Sans",
                                            # family="Google Noto Sans Mono",
                                            # family="Space Mono",
                                            # family="Roboto",
                                            # family="Source Code Pro"
                                            family="Veranda"
                                            # weight="bold"
                                        )
                                        )
            
        button_for_adding_devices.grid(
                                        padx=15,
                                        row=1,
                                        column=1,
                                        sticky="w"
                                        )
        
        create_and_update_device_dropdown()
   

        user_devices_label = ctk.CTkLabel(
            master=left_frame,
            text="User Devices",
            font=ctk.CTkFont(
                family="Noto Sans",
                weight="bold",
                size=20
            )
        )

        user_devices_label.grid(row=2, column=0, columnspan=2, pady=(30,0))




    

        devices_frame = ctk.CTkFrame(master=self,
                                    corner_radius=0,
                                    )
        devices_frame.grid(row=0, column=1, sticky="nsew")
        devices_frame.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)  # Set the weight of the column in the main frame



        device_frames = {}
        self.current_device = None
        left_buttons = {}


        
        def create_device_frames(device):
            this_frame = ctk.CTkFrame(master=devices_frame, corner_radius=0, fg_color="transparent")
            frame_title = ctk.CTkLabel(master=this_frame, text=device.device_name)
            frame_title.pack()


            for i in device.config_ids:
                print(i)
            # print(device.config_ids)


            this_frame.pack_forget()
            device_frames[device.device_id] = this_frame


        def display_device_frame(device_id):
            if device_id == self.current_device:
                pass
            else:
                device_frames[self.current_device].pack_forget()
                left_buttons[device_id].configure(fg_color = "gray25")
                left_buttons[self.current_device].configure(fg_color = "transparent")
                device_frames[device_id].pack()
                self.current_device = device_id

        def create_left_buttons(device_name, device_id, index):
            device_button = ctk.CTkButton(
            master=left_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=device_name,
            command=lambda d=device_id: display_device_frame(d),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
    )
            left_buttons[device_id] = device_button
            device_button.grid(row=index + 3, column=0, columnspan=2, sticky="ew", padx=5)


        user_devices, user_configurations = Classes2.get_devices_and_configs()

        
        for i, (k, v) in enumerate(user_devices.items()):
            create_device_frames(v)
            create_left_buttons(device_name=v.device_name, device_id=v.device_id, index=i)

        if len(user_devices) > 0:
            current_device = list(device_frames.keys())[0]
            device_frames[current_device].pack()
            left_buttons[current_device].configure(fg_color = "gray25")
            self.current_device = current_device















        # def create_devices_inner_frame():


        #     # Calling destroy() and then rebuilding the CTkScrollableFrame creates various issues. This is an inner frame that can be manipulated more easily
        #     devices_inner_frame = ctk.CTkFrame(master=devices_scrollable_frame, fg_color="transparent")
        #     devices_inner_frame.pack(padx=0, pady=0, fill="both", expand=True)
        #     # self.devices_inner_frame = devices_inner_frame

        #     def refresh_devices_inner_frame():
        #         # Destroy the full frame of devices and configurations and then recursively call the function to recreate 
        #         devices_inner_frame.destroy()
        #         create_devices_inner_frame()
            

        #     def create_config_ui(device_id, configuration, device_configs_frame, grid_x_position):



        #         config_frame = ctk.CTkFrame(master=device_configs_frame, fg_color="transparent")
        #         config_frame.pack(fill="x", expand=True,)

        #         if grid_x_position == 1:
        #             select_configuration_label = ctk.CTkLabel(
        #                 master=config_frame,
        #                 text="Select Configuration:",
        #             )
        #             select_configuration_label.grid(row=0, column=0, sticky="w", padx=10)

        #         radio_button = ctk.CTkRadioButton(master=config_frame,
        #                                         text=f"{configuration.configuration_name}                     ",
        #                                         # text_color="#6C757D",
        #                                         text_color="#949A9F",
        #                                         font=   ctk.CTkFont(
        #                                                                 family="Noto Sans",
        #                                                                 # weight="bold",
        #                                                                 size=20,
        #                                                                 ),
        #                                         variable=selected_configurations[device_id],
        #                                         value=str(configuration.configuration_id),
        #                                         command=lambda c=configuration, d=device_id: select_configuration(c, d),
        #                                         # radiobutton_width=24.5,
        #                                         # radiobutton_height=24.5,
        #                                         radiobutton_width=21,
        #                                         radiobutton_height=21,
        #                                         # corner_radius=2.5,
        #                                         corner_radius=2.5,
        #                                         border_width_unchecked=6,
        #                                         border_width_checked=6,
        #                                         fg_color=gui_variables.primary_colour,
        #                                         # hover_color="#1B81A8"
        #                                         hover_color="#1F538D"
        #                                         )

        #         radio_button.grid(row=grid_x_position,
        #                           padx=(5,0),
        #                           column=0,
        #                           sticky="w")



        #         duplicate_configuration_button = ctk.CTkButton(
        #             master=config_frame,
        #             height=30,
        #             width=200,
        #             fg_color="transparent",
        #             # text_color="#198754",
        #             font=ctk.CTkFont(family="Noto Sans"),
        #             text_color="#6C757D",
        #             border_color="#6C757D",
        #             border_width=1,
        #             # hover_color="#113A1B",
        #             corner_radius=2,
        #             text=" Copy Configuration",
        #             # command=lambda: self.edit_configuration(configuration.configuration_id, devices_scrollable_frame, create_devices_inner_frame)
        #         )
        #         duplicate_configuration_button.grid(row=grid_x_position, column=1, sticky="e", padx=15)


        #         edit_configuration_button = ctk.CTkButton(
        #             master=config_frame,
        #             height=30,
        #             width=200,
        #             fg_color="transparent",
        #             # text_color="#198754",
        #             font=ctk.CTkFont(family="Noto Sans"),
        #             text_color="#6C757D",
        #             border_color="#6C757D",
        #             border_width=1,
        #             hover_color="#113A1B",
        #             corner_radius=2,
        #             text=" Edit Configuration",
        #             command=lambda: self.edit_configuration(configuration.configuration_id, devices_scrollable_frame, create_devices_inner_frame)
        #         )
        #         edit_configuration_button.grid(row=grid_x_position, column=2, sticky="e")

        #         delete_configuration_button = ctk.CTkButton(
        #             master=config_frame,
        #             height=30,
        #             width=190,
        #             text="Delete Configuration",
        #             fg_color="transparent",
        #             # border_color="red",
        #             font=ctk.CTkFont(family="Noto Sans"),
        #             text_color="#6C757D",
        #             border_color="#6C757D",
        #             hover_color="#450C0F",
        #             border_width=1,
        #             corner_radius=2,
        #             # border_spacing=5,
        #             command=lambda c=configuration.configuration_id, f=config_frame, s=configuration.is_selected: configuration_deletion_warning(c, f, s)
        #         )
        #         delete_configuration_button.grid(row=grid_x_position, column=3, padx="15", pady="5", sticky="e")
        #         config_frame.columnconfigure(1, weight=2)
        #         # config_frame.columnconfigure(2, weight=1)


        #     def select_configuration(configuration, device_id):
        #         selected_configurations[device_id] = configuration.configuration_id
        #         execute_db_queries.update_selected_configuration(configuration.configuration_id)

        #     def create_left_buttons(device_name, device_id, index):
        #         device_button = ctk.CTkButton(
        #         master=left_frame,
        #         corner_radius=0,
        #         height=40,
        #         border_spacing=10,
        #         text=device_name,
        #         fg_color="transparent",
        #         text_color=("gray10", "gray90"),
        #         hover_color=("gray70", "gray30"),
        #         anchor="w"
        # )
        #         device_button.grid(row=index + 3, column=0, columnspan=2, sticky="ew", padx=5)


        #     def create_device_ui(device, row=None):

        #         device_frame = ctk.CTkFrame(master=devices_inner_frame, fg_color="transparent")
        #         device_frame.pack(fill="both", expand=True)

        #         devicewide_actions_frame = ctk.CTkFrame(
        #             master=device_frame,
        #             fg_color="transparent"
        #         )
        #         devicewide_actions_frame.pack(
        #             fill="x", 
        #             expand=False)
                
        #         # device_label = ctk.CTkLabel(master=left_frame,
        #         #                             text=device.device_name,
        #         #                             font=ctk.CTkFont(
        #         #                                 family="Roboto",
        #         #                                 weight="bold",
        #         #                                 size=25,
                                                
        #         #                             ),
        #         #                             )
                
        #         # device_label.grid(row=0, column=0,
        #         #                   sticky="e",
        #         #                   pady=(15, 30)
        #         #                   )


        #         new_configuration_button = ctk.CTkButton(master=devicewide_actions_frame,
        #                                                  text="Add Device Configuration",
        #                                                  text_color="white",
        #                                                  fg_color="#198754",
        #                                                  height=40,
        #                                                  width=230,
        #                                                  hover_color="#28A745",
        #                                                  font=ctk.CTkFont(family="Noto Sans"),
        #                                                 #  corner_radius=3,
        #                                                 #  border_width=2,
        #                                                  command=lambda d=device.device_id, n=device.device_name: add_new_configuration(d, n))
        #         new_configuration_button.grid(row=0, column=1, sticky="e",
        #                                     #   padx=15
        #                                       )


        #         delete_device_button = ctk.CTkButton(master=devicewide_actions_frame,
        #                                              text="Delete Device",
        #                                             fg_color="#DC3545",
        #                                             height=40,
        #                                             width=150,
        #                                             hover_color="red",
        #                                             font=ctk.CTkFont(family="Noto Sans"),
        #                                             # border_width=2,
        #                                             command=lambda d=device.device_id, f=device_frame: device_deletion_warning(d, f)
        #                                              )
        #         delete_device_button.grid(row=0, column=2, sticky="e",
        #                                   padx=(25, 15))

        #         devicewide_actions_frame.columnconfigure((0), weight=1)

        #         devicewide_actions_frame.columnconfigure((1), weight=2)

        #         device_configs_frame = ctk.CTkFrame(master=device_frame, fg_color="transparent")
        #         device_configs_frame.pack(fill="x")

        #         for configuration in device.configurations:
        #             # Loop through once and find the selected configuration to store in the dictionary
        #             if configuration.is_selected == True:
        #                 selected_configurations[device.device_id] = ctk.StringVar()
        #                 selected_configurations[device.device_id].set(str(configuration.configuration_id))

        #         for row, configuration in enumerate(device.configurations):

        #             create_config_ui(device.device_id, configuration, device_configs_frame, row+1)

        #         return device_frame


        #     def add_new_configuration(device_id, device_name):
        #         newest_configuration_id = execute_db_queries.new_empty_configuration(device_id, device_name)
        #         self.edit_configuration(configuration_id = newest_configuration_id, is_new_config=True, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame)
        #         for widget in devices_scrollable_frame.winfo_children():
        #             widget.destroy()
        #         create_devices_inner_frame()



        #     def configuration_deletion_warning(configuration_id, config_frame, is_selected):
        #         msg = CTkMessagebox(title="Delete Device?",
        #                             message="Delete configuration?",
        #                             option_1="Delete",
        #                             option_2="Cancel",
        #                             width=600,
        #                             height=300,
        #                             fade_in_duration=200
        #                             )
        #         if msg.get() == "Delete":
        #             if is_selected == True:
        #                 execute_db_queries.delete_configuration(configuration_id)
        #                 devices_inner_frame.destroy()
        #                 create_devices_inner_frame()
        #             else:
        #                 config_frame.destroy()
        #                 execute_db_queries.delete_configuration(configuration_id)

        #     def device_deletion_warning(device_id, device_frame):
        #         msg = CTkMessagebox(title="Delete Device?",
        #                             message="Deleting device will also delete all its configurations.",
        #                             option_1="Delete",
        #                             option_2="Cancel",
        #                             width=600,
        #                             height=300,
        #                             fade_in_duration=200
        #                             )
        #         if msg.get() == "Delete":
        #             device_frame.destroy()
        #             execute_db_queries.delete_device(device_id)
        #             create_and_update_device_dropdown()


        #     user_devices_and_configs = Classes.get_main_page_user_devices()
        #     # user_devices_and_configs2 = Classes2.get_main_page_user_devices()
            


        #     for index, device in enumerate(user_devices_and_configs):

        #         create_left_buttons(device.device_name, device.device_id, index)

        #         create_device_ui(device)

        # create_devices_inner_frame()



















        # bottom_frame = ctk.CTkFrame(
        #     master=self,
        #     fg_color="transparent"
        # )
        # bottom_frame.pack(
        #                 padx=(20, 20), 
        #                 pady=(0, 0),
        #                 fill="x",
        # )


        # save_devices_button = ctk.CTkButton(
        #     master=bottom_frame,
        #     height=40,
        #     width=120,
        #     text="Generate CFG",
        #     # text_color_disabled=("#9FA5AB"),
        # )
        # save_devices_button.grid(
        #     # row=0,
        #     # column=2,
        #     # padx=(20, 20),
        #     pady=30,
        #     sticky="e"
        # )




        # bottom_frame.grid_columnconfigure((0), weight=1)


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





        left_frame_edit_page = ctk.CTkFrame(master=self, fg_color="#2B2B2B")
        left_frame_edit_page.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Set the weight of the row in the main frame


        device_name_label = ctk.CTkLabel(master=left_frame_edit_page,
                                                text=configuration.device_name, # TODO: create function to spread across two lines if device name is long. /n apears to work well for this
                                                font=ctk.CTkFont(
                                                family="Noto Sans",
                                                # weight="bold",
                                                size=36,
                                                    ),
                                                text_color=gui_variables.primary_colour,
                                                pady=(20),
                                                corner_radius=0
                                    # anchor='s'
                                                )
        device_name_label.grid(row=0, column=0, columnspan=2, sticky="ew")




        general_settings_button = ctk.CTkButton(
            master=left_frame_edit_page,
            corner_radius=0,
            height=40,
            width=400,
            border_spacing=10,
            text="General Settings",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        general_settings_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15)



        edit_page_scrollable_frame = ctk.CTkScrollableFrame(master=self,)
        # edit_page_scrollable_frame.pack(fill="both", expand=True)


        edit_page_scrollable_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)  



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




        general_settings_frame = ctk.CTkFrame(master=edit_page_scrollable_frame,
                                              fg_color="transparent")
        general_settings_frame.pack(fill="both", expand=True)

        general_settings_left_frame = ctk.CTkFrame(
            master=general_settings_frame,
            fg_color="transparent"
        )

        general_settings_left_frame.grid(row=0, column=0)

        general_settings_right_frame = ctk.CTkFrame(master=general_settings_frame,
                                                    fg_color="transparent"
                                                    )
                                                    
        general_settings_right_frame.grid(row=0, column=1)


        configuration_name_label = ctk.CTkLabel(master=general_settings_left_frame,
                                                text=" Configuration Name",
                                                font=ctk.CTkFont(
                                                    family="Noto Sans",
                                                    weight="bold",
                                                    size=14
                                                )
                                                )
        configuration_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(200, 0))

        configuration_name_textbox = ctk.CTkTextbox(master=general_settings_left_frame,
                                                    height=10,
                                                    width=400,
                                                    # text_color="red",
                                                    font=ctk.CTkFont(
                                                        family="Noto Sans",
                                                        
                                                        size=16
                                                    ),
                                                    corner_radius=1
                                                    )
        configuration_name_textbox.grid(row=1, column=0, padx=10)

        configuration_name_textbox.insert("0.0", configuration.configuration_name)

        configuration_name_textbox.bind("<Tab>", focus_next_widget)
        configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)




        dpi_spinbox = IntSpinbox(master=general_settings_right_frame,
                                            width=200,
                                            step_size=50,
                                            min_value=configuration.min_dpi,
                                            max_value=configuration.max_dpi
                                            )


        def create_dpi_widgets():

            dpi_label = ctk.CTkLabel(
                                    master=general_settings_right_frame,
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
            dpi_label.grid(row=0, column=1)

            
            dpi_spinbox.set(configuration.dpi) #TODO: Update
            dpi_spinbox.grid(row=1, column=1)

        create_dpi_widgets()


        if configuration.smartshift_support == True:

            smartshift_options_label = ctk.CTkLabel(
                                    master=general_settings_left_frame,
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
            smartshift_options_label.grid(row=3, column=0, padx=(10,0), pady=(30,0), sticky="w")

            smartshift_frame = ctk.CTkFrame(master=general_settings_left_frame)
            smartshift_frame.grid(row=4, column=0, sticky="ew")


            def smartshift_checkbox_toggled():
                configuration.smartshift_on = not(configuration.smartshift_on)

            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = ctk.CTkCheckBox(master=smartshift_frame, text="SmartShift On", command=smartshift_checkbox_toggled,
                                                variable=check_var, onvalue=True, offvalue=False)
            checkbox.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w", rowspan=2)

            
            smartshift_threshold_label = ctk.CTkLabel(
                                    master=smartshift_frame,
                                                                        text=("Threshold"),
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
            smartshift_threshold_spinbox.grid(row=1, column=1, sticky="w", padx=(0,10))



            smartshift_torque_label = ctk.CTkLabel(
                                    master=smartshift_frame,
                                                                        text=("Torque"),
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
                                    master=general_settings_right_frame,
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
            hiresscroll_options_label.grid(row=3, column=1, padx=(10,0), pady=(30,0), sticky="w")


            hiresscroll_frame = ctk.CTkFrame(master=general_settings_right_frame)
            hiresscroll_frame.grid(row=4, column=1, sticky="ew")


            def hiresscroll_hires_toggle():
                configuration.hiresscroll_hires = not(configuration.hiresscroll_hires)


            hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
            hirescroll_hires_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="HiRes Scroll On", command=hiresscroll_hires_toggle,
                                                variable=hiresscroll_hires_var, onvalue=True, offvalue=False)
            hirescroll_hires_checkbox.grid(row=0, column=0, rowspan=2)


            def hiresscroll_invert_toggle():
                configuration.hiresscroll_invert = not(configuration.hiresscroll_invert)


            hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
            hirescroll_invert_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll Invert", command=hiresscroll_invert_toggle,
                                                variable=hiresscroll_invert_var, onvalue=True, offvalue=False)
            hirescroll_invert_checkbox.grid(row=0, column=1, rowspan=2)


            def hiresscroll_target_toggle():
                configuration.hiresscroll_target = not(configuration.hiresscroll_target)

            hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
            hirescroll_target_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll target", command=hiresscroll_target_toggle,
                                                variable=hiresscroll_target_var, onvalue=True, offvalue=False)
            hirescroll_target_checkbox.grid(row=0, column=2, rowspan=2)



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
            scrollwheel_label.pack(pady=300)


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


        if configuration.thumbwheel_touch_support == True or configuration.thumbwheel_proxy_support == True or configuration.thumbwheel_tap_support == True:
            

            touch_tap_proxy_frame = ctk.CTkFrame(master=edit_page_scrollable_frame)
            touch_tap_proxy_frame.pack()

            title_array = []
            if configuration.thumbwheel_touch_support == True:
                title_array.append("Touch")
            if configuration.thumbwheel_tap_support == True:
                title_array.append("Tap")
            if configuration.thumbwheel_proxy_support == True:
                title_array.append("Proxy")

            title_string = "/".join(title_array)

            touch_tap_proxy_label = ctk.CTkLabel(master=touch_tap_proxy_frame, text=title_string, font=ctk.CTkFont(
                                                            family="Roboto",
                                                                # weight="bold",
                                                            size=18,
                                                            ),)
            touch_tap_proxy_label.pack()


            def touch_tap_proxy_actions_radio_buttons(ttt_object):


                selected_ttt_configuration = ctk.StringVar()


                ttt_label = ctk.CTkLabel(master=touch_tap_proxy_frame, text=f"{ttt_object.ttt_type}")            
                ttt_label.pack()


                ttt_radio_buttons_to_create = []

                if ttt_object.ttt_nopress is not None:
                    ttt_radio_buttons_to_create.append(["No Press", ttt_object.ttt_nopress])
                if ttt_object.ttt_toggle_smartshift is not None:
                    ttt_radio_buttons_to_create.append(["Toggle Smart Shift", ttt_object.ttt_toggle_smartshift])
                if ttt_object.ttt_toggle_hiresscroll is not None:
                    ttt_radio_buttons_to_create.append(["Toggle Hi Res Scroll", ttt_object.ttt_toggle_hiresscroll])

                for ttt_config in ttt_radio_buttons_to_create:
                    ttt_config_radio_button = ctk.CTkRadioButton(master=touch_tap_proxy_frame,
                                                    text=ttt_config[0],
                                                    value=str(ttt_config[1]),
                                                    variable=selected_ttt_configuration,
                                                    command=lambda b= ttt_config[1]: Classes.update_selected_ttt_id(b),
                                                    radiobutton_width=24.5,
                                                    radiobutton_height=24.5,
                                                    corner_radius=2.5,
                                                    border_width_unchecked=6,
                                                    border_width_checked=6,
                                                    hover_color=gui_variables.primary_colour
                                                    )

                    ttt_config_radio_button.pack()

                    if ttt_config[1] == ttt_object.selected_id:
                        selected_ttt_configuration.set(str(ttt_config[1]))



            if configuration.thumbwheel_touch_support == True:
                thumbwheel_touch_object = Classes.TouchTapProxy.create_ttt_object(configuration.configuration_id, "Touch")
                touch_tap_proxy_actions_radio_buttons(thumbwheel_touch_object)


            if configuration.thumbwheel_tap_support == True:
                thumbwheel_touch_object = Classes.TouchTapProxy.create_ttt_object(configuration.configuration_id, "Tap")
                touch_tap_proxy_actions_radio_buttons(thumbwheel_touch_object)

            if configuration.thumbwheel_proxy_support == True:
                thumbwheel_touch_object = Classes.TouchTapProxy.create_ttt_object(configuration.configuration_id, "Proxy")
                touch_tap_proxy_actions_radio_buttons(thumbwheel_touch_object)















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





            selected_button_configuration = ctk.StringVar()




            button_label = ctk.CTkLabel(master=buttons_frame,
                                        font=ctk.CTkFont(
                                            family="Noto Sans",
                                            size=18
                                        ),
                                         text=f"{button.button_name} ({button.button_cid})")            
            button_label.pack(padx=12, pady=(20, 5))


            radio_buttons_to_create = []

            if button.button_default is not None:
                radio_buttons_to_create.append(["Default", button.button_default])
            if button.button_nopress is not None:
                radio_buttons_to_create.append(["No Press", button.button_nopress])
            if button.button_togglesmartshift is not None:
                radio_buttons_to_create.append(["Toggle Smart Shift", button.button_togglesmartshift])
            if button.button_togglehiresscroll is not None:
                radio_buttons_to_create.append(["Toggle Hi Res Scroll", button.button_togglehiresscroll])
            if button.button_gestures is not None:
                radio_buttons_to_create.append(["Gestures", button.button_gestures])

            radio_buttons_frame = ctk.CTkFrame(master=buttons_frame)
            radio_buttons_frame.pack()

            grid_row = 0

            for button_config in radio_buttons_to_create:
                button_config_radio_button = ctk.CTkRadioButton(master=radio_buttons_frame,
                                                text=button_config[0],
                                                value=str(button_config[1]),
                                                variable=selected_button_configuration,
                                                command=lambda b= button_config[1]: Classes.update_selected_button_config_id(b),
                                                radiobutton_width=24.5,
                                                radiobutton_height=24.5,
                                                corner_radius=2.5,
                                                border_width_unchecked=6,
                                                border_width_checked=6,
                                                hover_color=gui_variables.primary_colour
                                                )

                button_config_radio_button.grid(column=0, row=grid_row, sticky="w")

                if button_config[1] == button.selected_button_config_id:
                    selected_button_configuration.set(str(button_config[1]))

                grid_row += 1


# if configuration.is_selected == True:
                        # selected_configurations[device.device_id] = ctk.StringVar()
                        # selected_configurations[device.device_id].set(str(configuration.configuration_id))


#                radio_button = ctk.CTkRadioButton(master=config_frame,
#                                                 text=f"{configuration.configuration_name}",
#                                                 variable=selected_configurations[device_id],
#                                                 value=str(configuration.configuration_id),
#                                                 command=lambda c=configuration, d=device_id: select_configuration(c, d),
#                                                 radiobutton_width=24.5,
#                                                 radiobutton_height=24.5,
#                                                 corner_radius=2.5,
#                                                 border_width_unchecked=6,
#                                                 border_width_checked=6,
#                                                 hover_color=gui_variables.primary_colour
#                                                 )




        bottom_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        bottom_frame.grid(row=1, column=1)



        back_button = ctk.CTkButton(master=bottom_frame, 
                                            text="Back",
                                            command=lambda: [self.go_back(), update_spinboxes_in_db(), update_config_file_name()])
        back_button.pack(pady=20)


        if is_new_device == True:

            cancel_button_new_device = ctk.CTkButton(master=bottom_frame,
                                      text="Cancel Adding Device",
                                      command=lambda d=configuration.device_id, s=devices_scrollable_frame, c=create_devices_inner_frame, u=create_and_update_device_dropdown: self.go_back_dont_save_new_device(d, s, c, u)
                                      )
            cancel_button_new_device.pack(pady=20)

        elif is_new_config == True:
            cancel_button_new_config = ctk.CTkButton(master=bottom_frame,
                                                     text="Cancel Adding Config",
                                                     command=lambda i=configuration.configuration_id, s=devices_scrollable_frame, c=create_devices_inner_frame: self.go_back_dont_save_new_config(i, s, c)
                                                     )
            cancel_button_new_config.pack(pady=20)


        def update_config_file_name():
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            configuration.configuration_name = config_name_stripped
            for widget in devices_scrollable_frame.winfo_children():
                widget.destroy()
            create_devices_inner_frame()


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











class SplashScreen(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        

        self.label = ctk.CTkLabel(self, text="LogiOpsGUI", font=ctk.CTkFont(family="Noto Sans", size=60), text_color=gui_variables.primary_colour)

        self.label.pack(pady=(300, 50))  

        self.after(500, self.move_label_upwards)

        # Run the loading logic after the SplashScreen has been initialized
        self.after(10, self.start_loading)

    def start_loading(self):
        # Setup main_page in a separate thread
        self.loading_thread = threading.Thread(target=self.prepare_main_page)
        self.loading_thread.start()
        
        # After 2 seconds, check if main_page is ready
        self.after(1200, self.check_main_page_ready)

    def prepare_main_page(self):
        self.main_page = MainPage(self.master)
        self.main_page.pack_forget()

    def check_main_page_ready(self):
        if not self.loading_thread.is_alive():
            self.destroy()
            self.main_page.pack(fill="both", expand=True)
        else:
            # Check again after a short delay if the loading_thread is done
            self.after(100, self.check_main_page_ready)

    def move_label_upwards(self, steps=90):
        initial_padding = 300
        final_padding = 50
        step_value = (initial_padding - final_padding) / steps
        current_step = 0

        def update_position():
            nonlocal current_step
            current_step += 1

            # Calculate new padding based on current step
            new_padding = initial_padding - (current_step * step_value)

            # Update label padding
            self.label.pack_configure(pady=(new_padding, 10))

            # If we haven't reached the desired position, schedule the next update
            if current_step < steps:
                self.after(10, update_position)

        # Start the updating process
        update_position()





def setup_gui(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1366x768+100+100")
    root.resizable(True, True)
    root.title("LogiOpsGUI")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    splash = SplashScreen(root)
    splash.pack(fill="both", expand=True)


def main():
    root = ctk.CTk()
    
    create_app_data.configure_logging()  # Configure logging for the application
    create_app_data.initialise_database()  # Create DB, build required tables and triggers, add devices from DeviceData.py

    setup_gui(root)  # Configure GUI settings and pack main page into window.

    root.mainloop()

if __name__ == "__main__":
    main()













# class SplashScreen(ctk.CTkFrame):
#     def __init__(self, 
#                  master):
#         super().__init__(master)
#         # self.master.geometry("1366x768+100+100")
#         self.master.attributes('-type', 'splash')

#         loading_label = ctk.CTkLabel(master=self, text="Loading")
#         loading_label.pack()


# def load_main_page():
#     main_page = m

# def setup_gui(root):
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("dark-blue")

#     root.geometry("1366x768+100+100")
#     root.resizable(True, True)
#     root.title("LogiOpsGUI")

#     ctk.DrawEngine.preferred_drawing_method = "circle_shapes"


#     splashscreen_page = SplashScreen(root)
#     splashscreen_page.pack(fill="both", expand=True)


#     main_page = MainPage(root)
#     # main_page.pack_forget()
#     main_page.pack(fill="both", expand=True)



# def main():

#     root = ctk.CTk()
    
#     create_app_data.configure_logging() # Configure logging for the application

#     create_app_data.initialise_database() # Create DB, build required tables and triggers, add devices from DeviceData.py
    
#     setup_gui(root) # Configure GUI settings and pack main page into window.
    
    
#     root.mainloop()



