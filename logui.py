import customtkinter as ctk
import logging
import create_app_data
import execute_db_queries
import Classes
from CTkMessagebox import CTkMessagebox
import threading
import keymates
import json
import FileBrowserWindow
import create_cfg
import ast
import needs_super
import alleventcodes
import psutil
import os
import socket
import time
import gui_variables
from PIL import Image

import BackendData
from GraphicalControlElements import svg_to_image, MatthewsRadioButton, FloatSpinbox, IntSpinbox





class DeviceDropdown(ctk.CTkFrame):
    def __init__(self, master, front_page, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        self.master = master
        self.front_page = front_page
        self.add_device_button = ctk.CTkButton(master=self, height=37, width=140, state="disabled", text="Add Device", text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=("#28A745"), font=ctk.CTkFont(size=14, family="Veranda"))
        self.add_device_button.grid(row=0, column=1)
        self.setup_option_menu()

    def setup_option_menu(self):
        # Create the new option menu first
        self.options = [i.device_name for i in self.front_page.device_data.non_user_devices.values()]
        self.selected_option_var = ctk.StringVar(value=' Select New Device')
        new_option_menu = ctk.CTkOptionMenu(master=self, variable=self.selected_option_var, values=self.options, state="normal", width=350, height=35, corner_radius=0, dropdown_fg_color="#212121", dropdown_text_color="#D6D6D6", dropdown_hover_color="#1F538D", text_color="#D6D6D6", font=("Noto Sans", 14), dropdown_font=("Noto Sans", 16), command=self.device_dropdown_option_chosen)
        new_option_menu.grid(row=0, column=0)

        # Destroy the old option menu if it exists
        if hasattr(self, 'option_menu'):
            self.option_menu.destroy()

        # Set the new option menu as the current one
        self.option_menu = new_option_menu

    def add_device_button_clicked(self):
        self.front_page.pack_forget()
        selected_device = self.selected_option_var.get()
        self.front_page.make_a_splash(text=selected_device)

        self.front_page.device_added(selected_device)
        
        self.front_page.take_a_splash()
        def update_front_page():
            self.add_device_button.configure(state="disabled", fg_color=gui_variables.secondary_colour)
            self.setup_option_menu()
        self.after(10, update_front_page())

    def device_dropdown_option_chosen(self, new_device):
        self.selected_device = new_device
        self.add_device_button.configure(state="normal", fg_color=gui_variables.standard_green1)
        self.add_device_button.configure(command=self.add_device_button_clicked) 



class NewDeviceSplash1(ctk.CTkFrame):
    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)

        self.title_label = ctk.CTkLabel(master=self, text=text, font=ctk.CTkFont(family="Roboto", size=60), text_color="#242424")

        self.colours_array = [  '#242424', '#2C2C2C', '#353535', '#3D3D3D',
                                '#454545', '#4D4D4D', '#565656', '#5E5E5E',
                                '#666666', '#6E6E6E', '#777777', '#7F7F7F']

        self.fade_in_index = 0
        self.fade_in()

    def fade_in(self):
        self.title_label.pack(expand=True)
        self.change_colour()

    def change_colour(self):
        if self.fade_in_index < len(self.colours_array):
            current_colour = self.colours_array[self.fade_in_index]
            self.title_label.configure(text_color=current_colour)
            self.fade_in_index += 1
            self.after(5, self.change_colour) 

class NewDeviceSplash(ctk.CTkFrame):
    def __init__(self, master, text, text_color="#4D4D4D", *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        
        label = ctk.CTkLabel(master=self, text=text, font=ctk.CTkFont(family="Roboto", size=60), text_color=text_color)
        label.pack(expand=True)
        

class ConfigurationFrame:
    def __init__(self, master_frame, device_frame, config, front_page, select_configuration):
        
        self.device_frame = device_frame
        self.front_page = front_page
        self.master_frame = master_frame

        self.config = config

        self.select_configuration = select_configuration
        self.config_row_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent")
        self.config_row_frame.pack(side="bottom")

        self.radio_button = MatthewsRadioButton(master=self.config_row_frame, width=600, text=config.configuration_name, command=lambda c=self.config.configuration_id: select_configuration(c))
        self.radio_button.grid(row=0, column=0)

        if self.config.user_device_object.selected_config == self.config.configuration_id:
            self.radio_button.set_clicked()

        self.edit_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", border_width=1, hover_color="#113A1B", corner_radius=2, text=" Edit", command=lambda c=self.config.configuration_id, d=self.config.device_id: self.edit_configuration(configuration_id=c, device_id=d))
        self.edit_configuration_button.grid(row=0, column=2, sticky="e")

        delete_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=2, command=lambda: self.configuration_deletion_warning())
        delete_configuration_button.grid(row=0, column=3, padx="15", pady="5", sticky="e")
        
        self.config_row_frame.columnconfigure(1, weight=2)
        self.master_frame.columnconfigure(2, weight=1)

    def edit_configuration(self, configuration_id, device_id):
        self.edit_configuration_button.configure(state='disabled')
        self.front_page.edit_configuration(configuration_id=configuration_id, device_id=device_id, radio_button=self.radio_button)
        self.edit_configuration_button.configure(state='normal')


    def configuration_deletion_warning(self):
        msg = CTkMessagebox(title="Delete Configuration?", message="Delete configuration?", option_1="Delete", option_2="Cancel", width=600, height=300, fade_in_duration=200)
        if msg.get() == "Delete":

            if len(self.front_page.device_data.user_devices[self.config.device_id].configurations) == 1:
                self.front_page.device_deleted(self.config.device_id)

            else:
                self.config_row_frame.destroy()
                self.config.user_device_object.delete_configuration(configuration_id=self.config.configuration_id)
                try:
                    self.front_page.edit_windows[(self.config.device_id, self.config.configuration_id)].destroy()
                    del self.front_page.edit_windows[(self.config.device_id, self.config.configuration_id)] 
                except KeyError:
                    print("key error in configuration frame")
            
                if self.radio_button.is_selected == True:
                    self.device_frame.configuration_frames[self.config.user_device_object.selected_config].radio_button.set_clicked()



class DeviceFrame(ctk.CTkFrame):
    def __init__(self, master, controller, user_device):
        super().__init__(master, fg_color="transparent")

        self.configuration_frames = {}
        self.controller = controller
        self.front_page = self.controller.front_page

        self.user_device = user_device
        self.configurations = user_device.configurations

        self.frame_title = ctk.CTkLabel(master=self, text=user_device.device_name, font=ctk.CTkFont(family="Roboto", size=60), text_color="gray50")
        self.frame_title.pack(fill="x", expand=False, pady=20)

        self.device_options_frame = ctk.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.device_options_frame.pack(fill="x", expand=False)

        self.new_configuration_button = ctk.CTkButton(master=self.device_options_frame, text="Add Device Configuration", fg_color=gui_variables.standard_green1, height=55, width=300, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), command=lambda: self.add_new_configuration())
        self.new_configuration_button.grid(row=0, column=1, sticky="e")

        self.delete_device_button = ctk.CTkButton(master=self.device_options_frame, text="Delete Device", fg_color=gui_variables.standard_red4, hover_color=gui_variables.standard_red6,height=55, width=200, font=ctk.CTkFont(family="Helvetica Neue", size=16), command=lambda d=user_device.device_id: self.device_deletion_warning(d))
        self.delete_device_button.grid(row=0, column=2, sticky="e", padx=(25, 15))
        self.device_options_frame.columnconfigure((0), weight=1)
        self.device_options_frame.columnconfigure((1), weight=2)
        configurations_label = gui_variables.EditPageLabel1(master=self, text="Configurations:")
        configurations_label.pack(anchor="w", pady=(20, 10), padx=10)
        self.radio_button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.radio_button_frame.pack(fill="x", expand=False)
        self.create_configuration_frames()

    def add_new_configuration(self):
        self.front_page.pack_forget()
        self.front_page.make_a_splash(text=self.user_device.device_name)
        newest_configuration_id = self.user_device.add_new_configuration()
        radio_button = self.create_configuration_frame(newest_configuration_id, return_button=True)
        self.front_page.edit_configuration(configuration_id=newest_configuration_id, radio_button=radio_button, device_id=self.user_device.device_id)
        self.configuration_frames[self.user_device.selected_config].radio_button.another_button_clicked()
        radio_button.radio_button_clicked()
        self.front_page.take_a_splash()

    def select_configuration(self, configuration_id):
        try:
            self.configuration_frames[self.user_device.selected_config].radio_button.another_button_clicked()
            self.user_device.selected_config = configuration_id
        except KeyError as e:
            pass

    def create_configuration_frame(self, configuration_id, return_button=False):

        self.configuration_frames[configuration_id] = ConfigurationFrame(master_frame=self.radio_button_frame,device_frame=self,front_page=self.front_page,config=self.configurations[configuration_id], select_configuration=self.select_configuration)
        if return_button == True:
            return self.configuration_frames[configuration_id].radio_button

    def create_configuration_frames(self):
        for i in self.user_device.configurations.keys():
            self.create_configuration_frame(i)

    def device_deletion_warning(self, device_id):
        msg = CTkMessagebox(title="Delete Device?",message="Deleting device will also delete all its configurations.",option_1="Delete",option_2="Cancel",width=600,height=300,fade_in_duration=200)
        if msg.get() == "Delete":
            self.front_page.device_deleted(device_id)
            print(self.front_page.device_data.user_devices)

class DeviceFrameController(dict):
    def __init__(self, master, front_page):
        super().__init__()
        self.front_page = front_page
        self.current_frame = None
        self.master = master
        self.create_frames()

        if len(self.front_page.device_data.user_devices) > 0:
            self.pack_a_frame(frame_to_pack=next(iter(self.keys())))
        else:
            self.pack_a_frame()

    def create_single_frame(self, id_to_create):

        self[id_to_create] = DeviceFrame(master=self.master, controller=self, user_device=self.front_page.device_data.user_devices[id_to_create])

    def create_frames(self):
        self.placeholder_device_frame = ctk.CTkFrame(master=self.master, corner_radius=0, fg_color="transparent")
        placeholder_device_frame_text = ctk.CTkLabel(master=self.placeholder_device_frame, text="Add your first device from the dropdown", font=ctk.CTkFont(size=16), text_color="gray50")
        placeholder_device_frame_text.pack(padx=20)
        if len(self.front_page.device_data.user_devices) == 0:
            self.placeholder_device_frame.pack()
        for i in self.front_page.device_data.user_devices.keys():
            self.create_single_frame(id_to_create=i)

        self[None] = self.placeholder_device_frame

    def pack_a_frame(self, frame_to_pack=None, device_has_been_deleted=False):
        if self.current_frame is not None and not device_has_been_deleted:
            self.current_frame.pack_forget()
        self.current_frame = self[frame_to_pack]
        self.current_frame.pack()

    def add_new_device_frame(self, new_device_id):
        self.create_single_frame(new_device_id)
        self.pack_a_frame(new_device_id)


class LeftButtons(ctk.CTkFrame):
    def __init__(self, master, front_page, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.front_page = front_page
        self.button_dict = {}
        self.currently_selected_device = None
        self.setup_left_buttons()

    def create_button(self, device):
        self.button_dict[device.device_id] = ctk.CTkButton(master=self, corner_radius=0, height=40, border_spacing=10, text=device.device_name, font=ctk.CTkFont(family="Noto Sans",size=18 ), command=lambda d=device.device_id: self.on_button_click(d), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.button_dict[device.device_id].pack(side="bottom", fill="both", expand=True)

    def add_device(self, device):
        self.create_button(device)
        self.on_button_click(device.device_id)

    def setup_left_buttons(self):
        for i in reversed(self.front_page.device_data.user_devices.values()):
            self.create_button(i)
        if len(self.button_dict) > 0:
            self.on_button_click(device_id=list(self.button_dict.keys())[-1])

    def on_button_click(self, device_id):
        if device_id != self.currently_selected_device:
            self.front_page.device_frame_dict.pack_a_frame(frame_to_pack=device_id)

            if self.currently_selected_device is not None:
                self.button_dict[self.currently_selected_device].configure(fg_color="transparent")

            self.currently_selected_device = device_id
            self.button_dict[device_id].configure(fg_color="gray25")

    def remove_device_button(self, device_id):
        if device_id in self.button_dict:
            # self.currently_selected_device = None
            self.button_dict[device_id].destroy()
            del self.button_dict[device_id]

            self.currently_selected_device = None
            if len(self.button_dict) > 0:
                self.on_button_click(next(reversed(self.button_dict)))
            else:
                self.front_page.device_frame_dict.pack_a_frame()

class FrontPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.device_data = BackendData.Devices.get_all_devices()
        self.edit_windows = {}

        left_frame = ctk.CTkFrame(master=self, fg_color=gui_variables.bg_grey7)
        left_frame.grid(row=0, column=0, sticky="nsew")

        app_title_image = ctk.CTkImage(light_image=Image.open(os.path.join("images/logo.png")), size=(392, 132))
        app_title = ctk.CTkLabel(master=left_frame, image=app_title_image, text='')
        app_title.pack(padx=(0, 7), pady=(40,40))

        def handle_file_selection(selected_path, selected_filename):
            self.cfg_location, self.cfg_filename = create_cfg.set_cfg_location(selected_path, selected_filename)
            self.show_cfg_location.configure(text=f"{self.cfg_location}/{self.cfg_filename}")

        def on_create_cfg_button_click():            
            cfg_message = create_cfg.generate_in_user_chosen_directory()
            CTkMessagebox(title="Error", message=cfg_message, option_1="OK", width=600, height=300, fade_in_duration=200)

        ignored_devices_label = gui_variables.MainPageLabel1(master=left_frame, text="Ignored Devices",)
        cfg_file_label = ctk.CTkLabel(master=left_frame, text="Logid Configuration", font=ctk.CTkFont(family="Noto Sans", weight="bold", size=20),)
        self.cfg_location, self.cfg_filename = create_cfg.get_cfg_location()
        self.show_cfg_location = ctk.CTkLabel(master=left_frame, text=f"{self.cfg_location}/{self.cfg_filename}" if self.cfg_location != "default" else "etc/logid.cfg")
        create_cfg_button = ctk.CTkButton(master=left_frame, text="Create CFG", command=on_create_cfg_button_click)
        set_logid_path_button = ctk.CTkButton(master=left_frame,text="Edit CFG Location",command=lambda: FileBrowserWindow.BrowserWindow(self, permitted_formats="cfg", current_path=self.cfg_location, current_filename=self.cfg_filename, on_select=handle_file_selection))
        restart_logid_button = ctk.CTkButton(master=left_frame, text="Restart Logid")

        right_frame = ctk.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=2)

        self.grid_columnconfigure(1, weight=1)  # Set the weight of the column in the main frame
        self.grid_rowconfigure(1, weight=1)

        self.device_dropdown = DeviceDropdown(master=left_frame, front_page=self,)
        self.device_dropdown.pack()

        user_devices_label = gui_variables.MainPageLabel1(master=left_frame, text="User Devices",)
        user_devices_label.pack(padx=(0,0), pady=(50,0))
        self.device_frame_dict = DeviceFrameController(master=right_frame, front_page=self,)
        self.left_buttons = LeftButtons(master=left_frame, front_page=self, fg_color="transparent")
        self.left_buttons.pack(anchor="w", fill="x")
        ignored_devices_label.pack()
        cfg_file_label.pack()
        self.show_cfg_location.pack()
        create_cfg_button.pack()
        set_logid_path_button.pack()
        restart_logid_button.pack()

        bottom_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        bottom_frame.grid(row=1, column=0, sticky="ew",columnspan=2)

        def create_settings_window():
            settings_window = ctk.CTkToplevel(master)
            settings_window.title = "Settings"
            settings_window.geometry("800x800")

            def set_widget_scaling(value):
                ctk.set_widget_scaling(value)
                conn, cursor = execute_db_queries.create_db_connection()
                cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'widget_scaling'""",(value,))
                execute_db_queries.commit_changes_and_close(conn)

            def set_window_scaling(value):
                ctk.set_window_scaling(value)
                conn, cursor = execute_db_queries.create_db_connection()
                cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'window_scaling'""",(value,))
                execute_db_queries.commit_changes_and_close(conn)

            window_scaling, widget_scaling, geometry = get_geometry_and_window_and_widget_scaling()

            widget_scaling_label = ctk.CTkLabel(master=settings_window, text="Widget Scaling")
            widget_scaling_label.pack()
            widget_scaling_button = FloatSpinbox(master=settings_window, value=widget_scaling, width=200, step_size=0.05, decimal_places=2, min_value=-1000, max_value=1000, command=lambda: set_widget_scaling(widget_scaling_button.get()))
            widget_scaling_button.pack()
            
            window_scaling_label = ctk.CTkLabel(master=settings_window, text="Window Scaling")
            window_scaling_label.pack()
            window_scaling_button = FloatSpinbox(master=settings_window, value=window_scaling, width=200, step_size=0.05, decimal_places=2, min_value=-1000, max_value=1000, command=lambda: set_window_scaling(window_scaling_button.get()))
            
            window_scaling_button.pack()

            current_dimensions = f"{int(master.winfo_width()/window_scaling_button.get())}x{int(master.winfo_height()/window_scaling_button.get())}"
            current_dimensions_label = ctk.CTkLabel(master=settings_window, text=f"Current Dimensions: {current_dimensions}")
            current_dimensions_label.pack()
            startup_dimensions_label = ctk.CTkLabel(master=settings_window, text=f"Dimensions on Startup: {geometry}")
            startup_dimensions_label.pack()

            manually_update_label = ctk.CTkLabel(master=settings_window, text="Manually Update Dimensions")
            manually_update_label.pack()

            def manually_update():
                
                new_geometry = f"{width_button.get()}x{height_button.get()}"
                conn, cursor = execute_db_queries.create_db_connection()
                cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'geometry'""", (new_geometry,))
                execute_db_queries.commit_changes_and_close(conn)
                master.geometry(new_geometry)
                current_dimensions_label.configure(text=f"Current Dimensions: {new_geometry}")
                startup_dimensions_label.configure(text=f"Startup Dimensions: {new_geometry}")

            width_button = IntSpinbox(master=settings_window, value=int(master.winfo_width()/window_scaling_button.get()), width=200, step_size=10, min_value=100, max_value=7680)
            width_button.pack()
            height_button = IntSpinbox(master=settings_window, value=int(master.winfo_height()/window_scaling_button.get()), width=200, step_size=10, min_value=100, max_value=4320)
            height_button.pack()
            manually_update_button = ctk.CTkButton(master=settings_window, text="Set Dimensions", command=manually_update)
            manually_update_button.pack()

        settings_window_button = ctk.CTkButton(master=bottom_frame, height=40, width=120, text="App Settings", command=create_settings_window)
        settings_window_button.grid(pady=30, sticky="w")

        bottom_frame.grid_columnconfigure((0), weight=1)

        self.grid_columnconfigure(0, weight=0)  # Do not expand left_frame column
        self.grid_columnconfigure(1, weight=1)  # Allow right_frame column to expand
        self.grid_rowconfigure(0, weight=1)     # Allow right_frame row to expand
        self.grid_rowconfigure(1, weight=0)     # Keep bottom_frame from expanding vertically

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Customize close button behavior

        self.stop_event = threading.Event()
        def start_window_creation():
            self.stop_event.clear()  # Ensure the event is clear before starting
            self.thread = threading.Thread(target=self.create_windows)
            self.thread.start()

        start_window_creation()

    def on_close(self):
        if not self.stop_event.is_set():
            self.master.destroy()
            os._exit(0)
        else:
            self.master.destroy()
        
    def device_added(self, new_device_name): 
        new_device = self.device_data.add_new_user_device_given_name(new_device_name=new_device_name)
        new_device_id = new_device.device_id
        new_configuration_id, new_configuration = next(iter(new_device.configurations.items()))

        self.device_frame_dict.add_new_device_frame(new_device_id)
        self.left_buttons.add_device(new_device)

        radio_button = self.device_frame_dict[new_device_id].configuration_frames[new_configuration_id].radio_button
        radio_button.radio_button_clicked()

        self.edit_configuration(configuration_id=new_configuration_id, configuration_object=new_configuration, device_id=new_device_id, radio_button=radio_button)

    def make_a_splash(self, text="LogiOpsGUI"):
        self.splash = NewDeviceSplash(master=self.master, text=text, text_color="#3D3D3D")
        self.splash.pack(fill="both", expand=True)

    def take_a_splash(self):
        self.splash.destroy()


    def device_deleted(self, deleted_device_id):
# TODO: delete?
        self.left_buttons.remove_device_button(deleted_device_id)

        self.device_frame_dict[deleted_device_id].destroy()
        del self.device_frame_dict[deleted_device_id]
        
        self.device_data.delete_user_device(self.device_data.user_devices[deleted_device_id])
        self.device_dropdown.setup_option_menu()

        to_delete = []
        for i in self.edit_windows.keys():
            if i[0] == deleted_device_id:
                self.edit_windows[i].destroy()
                to_delete.append(i)
        for j in to_delete:
            del self.edit_windows[j]


    def configuration_added(self, device_id, newest_configuration_id):
        self.pack_forget()
        radio_button = self.device_frame_dict[device_id].configuration_frames[newest_configuration_id].radio_button
        radio_button.radio_button_clicked()
        
        self.edit_configuration(configuration_id=newest_configuration_id, device_id=device_id, radio_button=radio_button)

    def create_windows(self):
        print("start")
        for i in [k for k in self.device_data.user_devices.values()]:
            for j in [l for l in i.configurations.keys()]:
                try:
                    if (i.device_id, j) not in self.edit_windows.keys():
                        if i.device_id in self.device_frame_dict:
                            try:
                                radio_button = self.device_frame_dict[i.device_id].configuration_frames[j].radio_button
                                self.edit_configuration(configuration_id=j, device_id=i.device_id, radio_button=radio_button, add_to_dictionary=True)
                            except KeyError as e:
                                print(f"KeyError accessing radio_button: {e}")
                        else:
                            print(f"Error: device_id {i.device_id} not found in device_frame_dict.")
                    else:
                        print("already there")
                except Exception as e:
                    print(f"Exception occurred: {e}")

        self.stop_event.set()
        print("windows created")
        print(SystemMemory.get_memory_usage_mb())

    def edit_configuration(self, configuration_id, radio_button, device_id, configuration_object=None, add_to_dictionary=False ):
        if configuration_object == None:
            configuration_object = self.device_data.user_devices[device_id].configurations[configuration_id]
        if (device_id,configuration_id) in self.edit_windows.keys():
            self.pack_forget()
            self.edit_windows[(device_id,configuration_id)].show()
        else:
            edit_page = EditConfigFrame(self.master, front_page=self, configuration=configuration_object, radio_button=radio_button,)            
            self.edit_windows[(device_id,configuration_id)] = edit_page
            if add_to_dictionary == False:
                self.pack_forget()
                edit_page.show()
    def show(self):
        self.pack(fill="both", expand=True)
        self.master.unbind_all("<Button-4>")
        self.master.unbind_all("<Button-5>")

class EditConfigFrame(ctk.CTkFrame):
    def __init__(self, master, radio_button, front_page, configuration=None, add_action_frame=None):
        super().__init__(master, fg_color="transparent")

        self.master = master
        self.configuration = configuration
        self.main_page_radio_button = radio_button
        self.add_action_frame = add_action_frame
        self.front_page = front_page

        """Create the page's frames. Add title to page."""
        self.left_frame_edit_page = ctk.CTkFrame(master=self, fg_color=gui_variables.bg_grey7)
        self.left_frame_edit_page.grid(row=0, column=0, 
                                    #    rowspan=2,
                                         sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Set the weight of the row in the main frame

        self.edit_page_left_buttons_frame = ctk.CTkFrame(master=self.left_frame_edit_page, fg_color="transparent")
        self.edit_page_left_buttons_frame.grid(row=10, column=0, columnspan=2, sticky="ew", padx=0)

        self.edit_page_scrollable_frame = ctk.CTkFrame(master=self,)
        self.edit_page_scrollable_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)  

        device_name_label = ctk.CTkLabel(master=self.left_frame_edit_page, text=configuration.device_name, font=ctk.CTkFont( family="Noto Sans", size=30 if len(configuration.device_name) < 15 else 20, ), text_color=gui_variables.primary_colour, pady=(20), corner_radius=0 )
        device_name_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        back_button = ctk.CTkButton(master=self.left_frame_edit_page, text="Back",command=lambda: [self.go_back(),update_spinboxes_in_db(), update_config_file_name()])
        back_button.grid(row=2, column=0)

        self.left_buttons_dictionary = {}
        self.currently_selected_menu = None

        self.frames = {}

        def create_left_buttons(button_text, button_reference):
            created_button = ctk.CTkButton(master=self.edit_page_left_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=button_text, font=ctk.CTkFont(family="Noto Sans",size=18 ), command=lambda c=button_reference: self.left_button_clicked(c), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            created_button.pack(fill="x", expand=True)
            self.left_buttons_dictionary[button_reference] = created_button
            if len(self.left_buttons_dictionary) == 1:
                self.left_button_clicked(button_reference)

        if self.configuration.has_scrollwheel == True:
            self.frames["Scrollwheel"] = VerticalScrollwheelFrame(master=self.edit_page_scrollable_frame, root=self.master, configuration=self.configuration, )
            self.frames["Scrollwheel"].pack()

            if configuration.has_thumbwheel == True:
                create_left_buttons(button_reference="Scrollwheel", button_text="Scrollwheels")
            else:
                create_left_buttons(button_reference="Scrollwheel", button_text="Scrollwheel")

        for button in self.configuration.buttons:
            create_left_buttons(button_text=button.button_name, button_reference=button.button_cid)
            self.frames[button.button_cid] = ButtonConfigFrame(edit_config_frame_master = self.master,edit_config_frame_instance=self, master_frame=self.edit_page_scrollable_frame, configuration=self.configuration, button=button,)

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
                configuration_name_textbox.insert("end", configuration.configuration_name, "center")
            elif configuration_name_textbox.get("1.0", "end-1c").strip() == configuration.configuration_name:
                pass
            else:
                config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
                configuration.configuration_name = config_name_stripped
                configuration_name_textbox.delete("0.0", "end")
                configuration_name_textbox.insert("end", config_name_stripped, "center")
                # # TODO: make this target the desired widget more specifically. Now it's
                # for widget in devices_scrollable_frame.winfo_children():
                #     widget.destroy()
                # create_devices_inner_frame()
                self.main_page_radio_button.update_text(config_name_stripped)



        configuration_name_label = gui_variables.EditPageLabel1(master=self.left_frame_edit_page,text="Configuration Name")

        configuration_name_label.grid(row=3, column=0, columnspan=5, sticky="ew", padx=(0,0), pady=(20, 5))

        configuration_name_textbox = ctk.CTkTextbox(master=self.left_frame_edit_page, height=30, width=250,
                                                    activate_scrollbars=False,
                                                    fg_color=gui_variables.bg_grey6,
                                                    text_color=gui_variables.grey_standard2,
                                                     font=ctk.CTkFont(     family="Noto Sans",          size=15 ), corner_radius=1, 
                                                     
                                                     )


        configuration_name_textbox.grid(row=4, column=0, columnspan=5, padx=5, pady=(0,20), sticky="ew")
        configuration_name_textbox.tag_config("center", justify="center")
        configuration_name_textbox.insert("end", configuration.configuration_name, "center")

        configuration_name_textbox.bind("<Tab>", focus_next_widget)
        configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)

        dpi_spinbox = IntSpinbox(master=self.left_frame_edit_page, 
                                 db_query=self.configuration.update_dpi,
                                 width=250, step_size=50, min_value=configuration.min_dpi, max_value=configuration.max_dpi, value=configuration.dpi)

        def create_dpi_widgets():
            dpi_label = gui_variables.EditPageLabel1(master=self.left_frame_edit_page, text=("DPI"),)
            dpi_label.grid(row=5, column=0, columnspan=5, sticky="ew")        
            dpi_spinbox.grid(row=6, column=0, padx=(5, 5), pady=(0, 20), columnspan=5, )

        create_dpi_widgets()

        def update_config_file_name():
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            if len(config_name_stripped) > 0:
                configuration.configuration_name = config_name_stripped
                self.main_page_radio_button.update_text(config_name_stripped)

        def update_spinboxes_in_db():

            configuration.dpi = dpi_spinbox.get()
            if configuration.has_scrollwheel == True:
                pass
                # self.scroll_properties.scroll_up_threshold = self.frames["Scrollwheel"].scrollwheel_up_spinbox.get()
                # self.scroll_properties.scroll_down_threshold = self.frames["Scrollwheel"].scrollwheel_down_spinbox.get()
            if configuration.has_thumbwheel == True:
                pass
                # self.scroll_properties.scroll_left_threshold = self.frames["Thumbwheel"].thumbwheel_left_spinbox.get()
                # self.scroll_properties.scroll_right_threshold = self.frames["Thumbwheel"].thumbwheel_right_spinbox.get()



    def left_button_clicked(self, clicked_menu_item):
        if clicked_menu_item != self.currently_selected_menu:
            if self.currently_selected_menu is not None:
                self.left_buttons_dictionary[self.currently_selected_menu].configure(fg_color = "transparent")
            self.activate_left_button(menu_to_activate=clicked_menu_item)


    def activate_left_button(self, menu_to_activate):
        try:
            self.frames[menu_to_activate].pack()
            self.frames[self.currently_selected_menu].pack_forget()
        except KeyError:
            pass
        finally:
            self.currently_selected_menu = menu_to_activate
            self.left_buttons_dictionary[self.currently_selected_menu].configure(fg_color = "gray25")
            if self.add_action_frame is not None:
                self.add_action_frame.destroy()
                self.add_action_frame = None

    def go_back(self): 
        if self not in self.front_page.edit_windows.values():

            try:
                self.front_page.edit_windows[(self.configuration.device_id,self.configuration.configuration_id)].destroy()
                del self.front_page.edit_windows[(self.configuration.device_id, self.configuration.configuration_id)]

            except KeyError as e:
                print(e)
                logging.error(f"EditConfigFrame.go_back KeyError: {e}")
            self.front_page.edit_windows[(self.configuration.device_id,self.configuration.configuration_id)] = self
        if self.add_action_frame is not None:
            self.add_action_frame.destroy()
            self.add_action_frame = None
            self.frames[self.currently_selected_menu].pack()
        self.pack_forget()
        self.front_page.show()

    def show(self):
        self.pack(fill="both", expand=True)

    def on_mousewheel_linux(self, event):
        
        if event.num == 4:
            self.edit_page_scrollable_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.edit_page_scrollable_frame._parent_canvas.yview_scroll(1, "units")

class KeypressManual(ctk.CTkToplevel):
    def __init__(self, master, db_keypress_array, click_box):
        super().__init__(master)

        # Create a scrollable frame to hold the buttons
        self.button_container_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.button_container_frame.pack(fill='both', expand='true')
        self.button_frame = ctk.CTkScrollableFrame(self.button_container_frame)
        self.pack_button_frame()
        
        self.not_found_label = ctk.CTkLabel(master=self.button_frame, text="Not found")
        
        # Create a frame for the text box
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.pack(fill='x', padx=10, pady=10)

        # Create a text box for input
        self.search_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Search input event codes")
        self.search_entry.pack(fill='x', pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_buttons)
    
        self.button_names = [i for i in alleventcodes.all_events]

        self.buttons = []

        # Create buttons
        self.create_buttons()

    def pack_button_frame(self):
        self.button_frame.pack(fill='both', expand=True, padx=10, pady=10)


    def create_buttons(self):
        # Clear existing buttons
        for button in self.buttons:
            button.pack_forget()
        
        self.buttons = []
        
        # Create new buttons
        for name in self.button_names:
            button = ctk.CTkButton(self.button_frame, text=name, command=lambda n=name: self.on_button_click(n))
            button.pack(pady=5)
            self.buttons.append(button)

    def button_click(self, button):
        print(button)

    def filter_buttons(self, event):
        search_text = self.search_entry.get().lower()
        
        # Filter button names
        filtered_names = [name for name in self.button_names if search_text in name.lower()]
        
        # Update button frame
        for button in self.buttons:
            if button.cget("text") in filtered_names:
                button.pack_forget()
                button.pack(pady=5)

            else:
                button.pack_forget()
        if len(filtered_names) == 0:
            self.not_found_label.pack()
        else:
            self.not_found_label.pack_forget()
        self.button_frame.pack_forget()
        self.pack_button_frame()
        self.button_frame._parent_canvas.yview_moveto(0)
    def on_button_click(self, button_text):
        print(f"Button clicked: {button_text}")



class AddKeypressFrame(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back, root):
        super().__init__(master, fg_color="transparent")
        self.root=root
        self.settings_object = settings_object
        self.action_selection_frame=action_selection_frame
        self.go_back=go_back

        placeholder = ctk.CTkLabel(master=self, text="placeholder keypress")
        placeholder.pack()


        self.click_box = ctk.CTkButton(master=self, border_spacing=80)

        self.initialise_clickbox()
        self.click_box.pack(pady=50, padx=50, fill="both", expand=True)
        self.root.wm_attributes('-type', 'dialog')

    def initialise_clickbox(self):
        self.click_box.configure(text="\nCLICK HERE \n to enter keyboard shortcut\n                                                                                    ",
                                       command=self.activate_key_listener,
                                       fg_color="transparent",
                                       hover=False,
                                       border_width=10,
                                       border_color="#363636",
                                       font=ctk.CTkFont(size=14, family="Veranda"),
                                       border_spacing=80
                                       )
        if hasattr(self, "reset_button"):
            self.reset_button.destroy()
            self.save_button.destroy()
        if hasattr(self, "db_keypress_array"):
            del self.db_keypress_array
            del self.gui_keypress_array

    def activate_key_listener(self):
        self.root.bind("<KeyPress>", self.handle_key_press)
        self.root.bind("<KeyRelease>", self.handle_key_release)
        self.stop_recording_button = ctk.CTkButton(self, text="Click here to stop recording",
                                            command=self.deactivate_key_listener,
                                            )
        self.stop_recording_button.pack()
        self.click_box.configure(border_spacing=97 , text="                                                                              \nStart typing...\n", command=None, border_color="#198754",)
        self.click_box.focus_set()



    def stop_listening(self):
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")

    def deactivate_key_listener(self):
        self.stop_listening()
        self.stop_recording_button.destroy()

        if not hasattr(self, "db_keypress_array"):
            self.initialise_clickbox()
        elif hasattr(self, "reset_button") and bool(self.reset_button.winfo_exists()):
            pass
        else:
            self.click_box.configure(border_color="#DC3545")
            self.reset_button = ctk.CTkButton(self, text="Reset", command=self.initialise_clickbox)
            self.reset_button.pack()
            self.save_button = ctk.CTkButton(self, text="Save new keypress shortcut", command=self.save_button_clicked)
            self.save_button.pack()

    def save_button_clicked(self):

        new_keypress_object = self.settings_object.add_new_keypress_action(keypresses=json.dumps(self.db_keypress_array))
        new_button = self.action_selection_frame.create_keypress_button(new_keypress_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()

    def pack_forget(self, *args, **kwargs):
        if hasattr(self, 'stop_recording_button'):
            self.deactivate_key_listener()
        else:
            print("no button")
        super().pack_forget(*args, **kwargs)

    def handle_key_press(self, event):

        db_keymate, gui_keymate = keymates.get_keymates(event.keysym)
        if not hasattr(self, "db_keypress_array"):
            self.db_keypress_array = [db_keymate]            
            self.gui_keypress_array = [gui_keymate]
            self.click_box.configure(text=f"                                                                              \n{gui_keymate}\n")
            
        # elif db_keymate not in self.db_keypress_array:
        else:
            self.click_box.configure(text=f"{self.click_box._text[:-1]} {gui_keymate}\n")
            self.db_keypress_array.append(db_keymate)
            self.gui_keypress_array.append(gui_keymate)
        if event.keysym == "Super_L":
            self.root.after(150, lambda: self.root.focus_force())  # Try to force focus back after a short delay
        return "break"


    def handle_key_release(self, event):
        if event.keysym == "Super_L":
            self.root.after(150, lambda: self.root.focus_force())  # Try to force focus back after key is released




class KeyPressFrame(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

    

        self.click_box = ctk.CTkButton(master=self, border_spacing=80)

        self.initialise_clickbox()
        self.click_box.pack(pady=50, padx=50, fill="both", expand=True)
        self.app_root.wm_attributes('-type', 'dialog')

        self.enter_manually_button = ctk.CTkButton(master=self, text="Enter Array Manually", command=self.enter_manually)
        # self.enter_manually_button.pack()


    def enter_manually(self):
        
            
        asdf = KeypressManual(master=self, db_keypress_array=self.db_keypress_array if hasattr(self, "db_keypress_array") else [], click_box=self.click_box)




    def initialise_clickbox(self):
        self.click_box.configure(text="\nCLICK HERE \n to enter keyboard shortcut\n                                                                                    ",
                                       command=self.activate_key_listener,
                                       fg_color="transparent",
                                       hover=False,
                                       border_width=10,
                                       border_color="#363636",
                                       font=ctk.CTkFont(size=14, family="Veranda"),
                                       border_spacing=80
                                       )
        if hasattr(self, "reset_button"):
            self.reset_button.destroy()
            self.save_button.destroy()
        if hasattr(self, "db_keypress_array"):
            del self.db_keypress_array
            del self.gui_keypress_array

    def activate_key_listener(self):
        self.app_root.bind("<KeyPress>", self.handle_key_press)
        self.app_root.bind("<KeyRelease>", self.handle_key_release)
        self.stop_recording_button = ctk.CTkButton(self, text="Click here to stop recording",
                                            command=self.deactivate_key_listener,
                                            )
        self.stop_recording_button.pack()
        self.click_box.configure(border_spacing=97 , text="                                                                              \nStart typing...\n", command=None, border_color="#198754",)
        self.click_box.focus_set()



    def stop_listening(self):
        self.app_root.unbind("<KeyPress>")
        self.app_root.unbind("<KeyRelease>")

    def deactivate_key_listener(self):
        self.stop_listening()
        self.stop_recording_button.destroy()

        if not hasattr(self, "db_keypress_array"):
            self.initialise_clickbox()
        elif hasattr(self, "reset_button") and bool(self.reset_button.winfo_exists()):
            pass
        else:
            self.click_box.configure(border_color="#DC3545")
            self.reset_button = ctk.CTkButton(self, text="Reset", command=self.initialise_clickbox)
            self.reset_button.pack()
            self.save_button = ctk.CTkButton(self, text="Save new keypress shortcut", command=self.save_button_clicked)
            self.save_button.pack()

    def save_button_clicked(self):
        new_primary_key = self.settings_object.add_new_keypress_action(keypresses=json.dumps(self.db_keypress_array))

        if not isinstance(self.added_from, GestureRadioFrame):
            self.origin_frame.create_keypress_radio_button_row(i=new_primary_key)
            self.origin_frame.keypress_radio_buttons_frame.grid(row=3, column=0)
        else:
            self.added_from.create_keypress_radio_button_row(i=new_primary_key)
            self.added_from.keypress_radio_buttons_frame.grid(row=3, column=0)

        self.go_back_function()

    def pack_forget(self, *args, **kwargs):
        if hasattr(self, 'stop_recording_button'):
            self.deactivate_key_listener()
        else:
            print("no button")
        super().pack_forget(*args, **kwargs)

    def handle_key_press(self, event):

        db_keymate, gui_keymate = keymates.get_keymates(event.keysym)
        if not hasattr(self, "db_keypress_array"):
            self.db_keypress_array = [db_keymate]            
            self.gui_keypress_array = [gui_keymate]
            self.click_box.configure(text=f"                                                                              \n{gui_keymate}\n")
            
        # elif db_keymate not in self.db_keypress_array:
        else:
            self.click_box.configure(text=f"{self.click_box._text[:-1]} {gui_keymate}\n")
            self.db_keypress_array.append(db_keymate)
            self.gui_keypress_array.append(gui_keymate)
        if event.keysym == "Super_L":
            self.app_root.after(150, lambda: self.app_root.focus_force())  # Try to force focus back after a short delay
        return "break"


    def handle_key_release(self, event):
        if event.keysym == "Super_L":
            self.app_root.after(150, lambda: self.app_root.focus_force())  # Try to force focus back after key is released



class AddAxisFrame(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        label=ctk.CTkLabel(master=self, text="Axis")
        label.pack()

        
        rel_list = ["REL_X", "REL_Y", "REL_Z", "REL_RX", "REL_RY", "REL_RZ", "REL_HWHEEL", "REL_DIAL", "REL_WHEEL", "REL_MISC", "REL_RESERVED", "REL_WHEEL_HI_RES", "REL_HWHEEL_HI_RES", "REL_MAX", "REL_CNT"]

        def enable_save_button(selected_option):
            self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)


        axis_dropdown_variable = ctk.StringVar(value="Select Axis")
        axis_dropdown = ctk.CTkOptionMenu(master=self,
                                          variable=axis_dropdown_variable,
                                          values=rel_list,
                                          state="normal",
                                          width=200,
                                          height=36,
                                          command=enable_save_button
                                          )
        axis_dropdown.pack()



        multiplier_floatspinbox = FloatSpinbox(master=self,

                                value=1,
                                width=200,
                                step_size=0.1,
                                min_value=-9999,
                                max_value=9999
                                        )
        multiplier_floatspinbox.pack()
        


        self.save_button = ctk.CTkButton(master=self, 
                                        text="Save New Action", 
                                        command=lambda: self.add_new_axis(axis_dropdown_variable.get(), 
                                                                        multiplier_floatspinbox.get()), 
                                        text_color="white", 
                                        text_color_disabled=("#9FA5AB"), 
                                        fg_color=gui_variables.standard_green1, 
                                        font=ctk.CTkFont(size=14, family="Veranda"),
                                        state="disabled")
                                        
        self.save_button.pack()



    def add_new_axis(self, axis_to_add, axis_multiplier):
        
        new_primary_key = self.settings_object.add_new_axis(axis=axis_to_add, axis_multiplier=axis_multiplier)

        if isinstance(self.added_from, GestureRadioFrame):
            self.added_from.create_axes_radio_button_row(gesture_id=new_primary_key)
            self.added_from.axis_radio_buttons_frame.grid(row=7, column=0)
        else:
            self.origin_frame.create_axes_radio_button_row(button_config_id=new_primary_key)
            self.origin_frame.axis_radio_buttons_frame.grid(row=7, column=0)
        self.go_back_function()

class CycleDPIRemoveButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_not_hover = svg_to_image(path="images/delete_from_array_button.svg", output_height=22, output_width=22)
        self.button_hover = svg_to_image(path="images/delete_from_array_button_highlighted.svg", output_height=22, output_width=22)


        self.bind('<Enter>', lambda event: self.button_enter(event))
        self.bind('<Leave>', lambda event: self.button_leave(event))

    def button_enter(self, event):
        self.configure(image=self.button_hover)

    def button_leave(self, event):
        self.configure(image=self.button_not_hover)





class AddCycleDPI1(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back):
        super().__init__(master, fg_color="transparent")
        self.settings_object = settings_object
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back

        label=ctk.CTkLabel(master=self, text="CycleDPI")
        label.pack()



        self.spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=200,
                                step_size=100,
                                min_value=self.settings_object.config_object.min_dpi,
                                max_value=self.settings_object.config_object.max_dpi
                                )
        self.spinbox.pack()            

        self.add_to_array_button = ctk.CTkButton(master=self, text="Add value to array", command=self.add_value_to_array, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        self.add_to_array_button.pack(padx=100, pady=100)

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", state="disabled", command=self.save_button_clicked, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack()


        

        self.array_frame_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.array_frame_container.pack(
            # fill="x", expand="false"
            )

        array_left_bracket = ctk.CTkLabel(master=self.array_frame_container,text="dpis = [", font=ctk.CTkFont(size=28), text_color="gray50")
        array_right_bracket = ctk.CTkLabel(master=self.array_frame_container, text="]",font=ctk.CTkFont(size=28), text_color="gray50")

        array_left_bracket.pack(side="left", 
                                anchor=
                                "center",
                                # "w",
                                  padx=(0, 10))
        array_right_bracket.pack(side="right",
                                  anchor="center",
                                #   "e"
                                  )

        self.array_frame = ctk.CTkFrame(master=self.array_frame_container, fg_color="transparent")
        self.array_frame.pack(pady=30)
        self.array_frame_packer = ctk.CTkFrame(master=self.array_frame, fg_color="transparent")
        self.array_frame_packer.pack(side="left")
        packer_label = ctk.CTkLabel(master=self.array_frame_packer, text="    ", font=ctk.CTkFont(size=22))
        packer_label.pack(side="left")

        self.array_dict = {}


    def save_button_clicked(self):

        new_cycledpi_object = self.settings_object.add_new_cycledpi_action(str([i for i in self.array_dict.keys()]))
        new_button = self.action_selection_frame.create_cycledpi_button(new_cycledpi_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()

    def add_to_array_frame(self, value):
        if len(self.array_dict) == 0:
            self.array_frame_packer.pack_forget()
        if len(self.array_dict) == 1:

            self.save_button.configure(state="enabled")

        value_frame = ctk.CTkFrame(master=self.array_frame, fg_color="transparent")

        label = ctk.CTkLabel(master=value_frame, text=value, font=ctk.CTkFont(size=20),)
        label.pack(side="left")

        remove_button = CycleDPIRemoveButton(master=value_frame, text="", image=svg_to_image(path="images/delete_from_array_button.svg", output_height=22, output_width=22), command=lambda: self.delete_from_array(value), height=12,width=12, fg_color="transparent", hover=False)
        remove_button.pack()

        self.array_dict[value] = value_frame
        self.array_dict = dict(sorted(self.array_dict.items()))
        for i in self.array_dict.keys():
            if i >= value:
                self.array_dict[i].pack_forget()
                self.array_dict[i].pack(side="left")


    def delete_from_array(self, value):
        if len(self.array_dict) == 2:
            self.save_button.configure(state="disabled")
        self.array_dict[value].destroy()
        del self.array_dict[value]

    def add_value_to_array(self):
        value_to_add = self.spinbox.get()
        if value_to_add > self.settings_object.config_object.max_dpi:
            self.spinbox.set(self.settings_object.config_object.max_dpi)
            value_to_add = self.settings_object.config_object.max_dpi
        elif value_to_add < self.settings_object.config_object.min_dpi:
            self.spinbox.set(self.settings_object.config_object.min_dpi)
            value_to_add = self.settings_object.config_object.min_dpi
        if value_to_add not in self.array_dict.keys():
            self.add_to_array_frame(value=value_to_add)




class AddCycleDPI(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, min_dpi, max_dpi, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from
        self.max_dpi = max_dpi
        self.min_dpi = min_dpi

        label=ctk.CTkLabel(master=self, text="CycleDPI")
        label.pack()



        self.spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=200,
                                step_size=100,
                                min_value=self.min_dpi,
                                max_value=self.max_dpi
                                )
        self.spinbox.pack()            

        self.add_to_array_button = ctk.CTkButton(master=self, text="Add value to array", command=self.add_value_to_array, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        self.add_to_array_button.pack(padx=100, pady=100)

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", state="disabled", command=self.add_new_cycledpi, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack()


        

        self.array_frame_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.array_frame_container.pack(fill="both", expand="true")

        array_left_bracket = ctk.CTkLabel(master=self.array_frame_container,text="dpis = [", font=ctk.CTkFont(size=50), text_color="gray50")
        array_right_bracket = ctk.CTkLabel(master=self.array_frame_container, text="]",font=ctk.CTkFont(size=50), text_color="gray50")

        array_left_bracket.pack(side="left", anchor="w", padx=(0, 10))
        array_right_bracket.pack(side="right", anchor="e")

        self.array_frame = ctk.CTkFrame(master=self.array_frame_container, fg_color="transparent")
        self.array_frame.pack(pady=30)
        self.array_frame_packer = ctk.CTkFrame(master=self.array_frame, fg_color="transparent")
        self.array_frame_packer.pack(side="left")
        packer_label = ctk.CTkLabel(master=self.array_frame_packer, text=" ", font=ctk.CTkFont(size=30))
        packer_label.pack(side="left")

        self.array_dict = {}

    def add_to_array_frame(self, value):
        if len(self.array_dict) == 0:
            self.array_frame_packer.pack_forget()
        if len(self.array_dict) == 1:

            self.save_button.configure(state="enabled")

        value_frame = ctk.CTkFrame(master=self.array_frame, fg_color="transparent")

        label = ctk.CTkLabel(master=value_frame, text=value, font=ctk.CTkFont(size=30),)
        label.pack(side="left")

        remove_button = CycleDPIRemoveButton(master=value_frame, text="", image=svg_to_image(path="images/delete_from_array_button.svg", output_height=34, output_width=34), command=lambda: self.delete_from_array(value), height=12,width=12, fg_color="transparent", hover=False)
        remove_button.pack()

        self.array_dict[value] = value_frame
        self.array_dict = dict(sorted(self.array_dict.items()))
        for i in self.array_dict.keys():
            if i >= value:
                self.array_dict[i].pack_forget()
                self.array_dict[i].pack(side="left")


    def delete_from_array(self, value):
        if len(self.array_dict) == 2:
            self.save_button.configure(state="disabled")
        self.array_dict[value].destroy()
        del self.array_dict[value]

    def add_value_to_array(self):
        value_to_add = self.spinbox.get()
        if value_to_add > self.max_dpi:
            self.spinbox.set(self.max_dpi)
            value_to_add = self.max_dpi
        elif value_to_add < self.min_dpi:
            self.spinbox.set(self.min_dpi)
            value_to_add = self.min_dpi
        if value_to_add not in self.array_dict.keys():
            self.add_to_array_frame(value=value_to_add)

    def add_new_cycledpi(self):
        new_primary_key = self.settings_object.add_new_cycledpi(str([i for i in self.array_dict.keys()]))

        if isinstance(self.added_from, GestureRadioFrame):
            self.added_from.create_cycledpi_radio_button_row(gesture_id=new_primary_key)
            self.added_from.cycledpi_radio_buttons_frame.grid(row=6, column=0)
        else:
            self.origin_frame.create_cycledpi_radio_button_row(button_config_id=new_primary_key)
            self.origin_frame.cycledpi_radio_buttons_frame.grid(row=6, column=0)
        self.go_back_function()




class AddChangeDPI(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from=added_from

        label=ctk.CTkLabel(master=self, text="ChangeDPI")
        label.pack()

        self.spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=200,
                                step_size=100,
                                min_value=-8000,
                                max_value=8000
                                )
        self.spinbox.pack()            

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", command=self.add_new_changedpi, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack()


    def add_new_changedpi(self):
        new_primary_key = self.settings_object.add_new_changedpi(self.spinbox.get())

        if not isinstance(self.added_from, GestureRadioFrame):
            self.origin_frame.create_changedpi_radio_button_row(button_config_id=new_primary_key)
            self.origin_frame.changedpi_radio_buttons_frame.grid(row=5, column=0)
        else:
            self.added_from.create_changedpi_radio_button_row(gesture_id=new_primary_key)
            self.added_from.changedpi_radio_buttons_frame.grid(row=5, column=0)
        
        self.go_back_function()


class AddChangeHost(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        label=ctk.CTkLabel(master=self, text="Host to Toggle")
        label.pack(padx=(300), pady=(30, 15))

        def enable_save_button(x):
            self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)
            self.save_button.configure(command=self.add_new_changehost)

        self.menu_var = ctk.StringVar(value="Select Host")
        self.menu = ctk.CTkOptionMenu(master=self,
                                 variable=self.menu_var,
                                 values=["1", "2", "3", "Previous", "Next"],
                                 state="normal",
                                 width=200,
                                 height=36,
                                 command=enable_save_button
                                 )
        self.menu.pack()

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", command=self.add_new_changehost, state="disabled", text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=gui_variables.standard_green3, font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack(side="bottom", padx=(600, 0))

    def add_new_changehost(self):
        new_primary_key = self.settings_object.add_new_changehost(host=self.menu_var.get())

        if not isinstance(self.added_from, GestureRadioFrame):
            self.origin_frame.changehost_radio_buttons_frame.grid(row=4, column=0)
            self.origin_frame.create_changehost_radio_button_row(button_config_id=new_primary_key)
        else:
            self.added_from.changehost_radio_buttons_frame.grid(row=4, column=0)
            self.added_from.create_changehost_radio_button_row(gesture_id=new_primary_key)
            

        self.go_back_function()

        # new_primary_key = self.settings_object.add_new_keypress_action(keypresses=str(self.db_keypress_array))

        # if not isinstance(self.added_from, GestureRadioFrame):
        #     self.origin_frame.create_keypress_radio_button_row(i=new_primary_key)
        #     self.origin_frame.keypress_radio_buttons_frame.grid(row=2, column=0)
        # else:
        #     self.added_from.create_keypress_radio_button_row(i=new_primary_key)
        #     self.added_from.keypress_radio_buttons_frame.grid(row=2, column=0)

        # self.go_back_function()

class ScrollFrame(ctk.CTkFrame):
    def __init__(self, master, root, scroll_settings):
        super().__init__(master, fg_color="black")

        self.selected_action_id = scroll_settings.actions.selected_action_id
        
        title = ctk.CTkLabel(master=self, text=f"Scroll {scroll_settings.scroll_direction}")
        title.pack()

        selected_mode_var = ctk.StringVar(value=scroll_settings.mode)
        scroll_mode_dropdown = ctk.CTkOptionMenu(master=self, variable=ctk.StringVar(value=scroll_settings.mode), values=["OnInterval", "OnThreshold"], state="normal", width=200, height=36, command=lambda new_mode = selected_mode_var: scroll_settings.save_new_mode(new_mode))
        scroll_mode_dropdown.pack()

        scrollwheel_threshold_spinbox = IntSpinbox(master=self, width=200, step_size=5, min_value=1, max_value=9999, db_query=scroll_settings.update_threshold)
        scrollwheel_threshold_spinbox.set(scroll_settings.threshold)
        scrollwheel_threshold_spinbox.pack()

        action_selection_frame = ActionSelectionFrame(master=self, root=root, actions=scroll_settings.actions, pack_order=scroll_settings.actions.get_added_order())
        new_action_frame_button = ctk.CTkButton(master=self, text="Add New Action", command=lambda: (self.pack_forget(), NewActionFrame(master=master, root=root, action_selection_frame=action_selection_frame, origin_frame=self, settings_object=scroll_settings.actions)))
        new_action_frame_button.pack()

        action_selection_frame.pack(fill="both", expand=True)


class AddAxisFrame1(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back):
        super().__init__(master, fg_color="transparent")
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back
        self.settings_object = settings_object

        # Create and pack the label
        label = ctk.CTkLabel(master=self, text="Axis")
        label.pack()

        # List of available axes
        rel_list = [
            "REL_WHEEL (Scroll Up/Down)", "REL_WHEEL_HI_RES (Hi-res Scroll Up/Down)",
            "REL_HWHEEL (Scroll Left/Right)", "REL_HWHEEL_HI_RES (Hi-res Scroll Left/Right)",
            "REL_X (x-axis Movement)", "REL_Y (y-axis Movement)", "REL_Z (z-axis Movement)",
            "REL_RX (Rotational x-axis Movement)", "REL_RY (Rotational y-axis Movement)",
            "REL_RZ (Rotational z-axis Movement)", "REL_DIAL (Dial Movement)",
            "REL_MISC (Miscellaneous Relative Movement)", "REL_RESERVED (Typically Unused)",
            "REL_MAX (Maximum Relative Axis Value.)", "REL_CNT (Total Relative Axes Count)"
        ]

        # Dropdown variable and axis dropdown menu
        axis_dropdown_variable = ctk.StringVar(value="Select Axis")
        axis_dropdown = ctk.CTkOptionMenu(
            master=self,
            variable=axis_dropdown_variable,
            values=rel_list,
            state="normal",
            width=200,
            height=36,
            command=self.enable_save_button
        )
        axis_dropdown.pack()

        # Multiplier spinbox
        multiplier_floatspinbox = FloatSpinbox(
            master=self,
            value=1,
            width=200,
            step_size=0.1,
            min_value=-9999,
            max_value=9999
        )
        multiplier_floatspinbox.pack()

        # Save button (initially disabled)
        self.save_button = ctk.CTkButton(
            master=self,
            text="Save New Action",
            command=lambda: self.save_button_clicked(
                axis_dropdown_variable.get().split(" (")[0],
                multiplier_floatspinbox.get()
            ), 
            text_color="white",
            text_color_disabled="#9FA5AB",
            fg_color=gui_variables.standard_green1,
            font=ctk.CTkFont(size=14, family="Veranda"),
            state="disabled"
        )
        self.save_button.pack()

    def enable_save_button(self, selected_menu):
        # Enable the save button when an axis is selected
        self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)

    def save_button_clicked(self, axis_button, axis_multiplier):
        new_axis_object = self.settings_object.add_new_axis_action(axis_button,axis_multiplier)
        new_button = self.action_selection_frame.create_axis_button(new_axis_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()
        
        self.go_back()












class AddChangeHost1(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back):
        super().__init__(master, fg_color="transparent")
        self.settings_object=settings_object
        self.action_selection_frame=action_selection_frame
        self.go_back=go_back

        label=ctk.CTkLabel(master=self, text="Host to Toggle")
        label.pack(padx=(300), pady=(30, 15))

        def enable_save_button(x):
            self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)
            

        self.menu_var = ctk.StringVar(value="Select Host")
        self.menu = ctk.CTkOptionMenu(master=self,
                                 variable=self.menu_var,
                                 values=["1", "2", "3", "Previous", "Next"],
                                 state="normal",
                                 width=200,
                                 height=36,
                                 command=enable_save_button
                                 )
        self.menu.pack()

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", state="disabled", text_color="white", command=lambda: self.save_button_clicked(), text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=gui_variables.standard_green3, font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack(side="bottom", padx=(600, 0))

    def save_button_clicked(self):
        chosen_option = self.menu_var.get()
        host_change = "prev" if chosen_option == "Previous" else "next" if chosen_option=="Next" else chosen_option
        new_changehost_object = self.settings_object.add_new_changehost_action(host_change=host_change)

        new_button = self.action_selection_frame.create_changehost_button(new_changehost_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()



class AddChangeDPI1(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back):
        super().__init__(master, fg_color="transparent")
        self.settings_object = settings_object
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back

        label=ctk.CTkLabel(master=self, text="ChangeDPI")
        label.pack()

        spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=200,
                                step_size=100,
                                min_value=-settings_object.config_object.max_dpi,
                                max_value=settings_object.config_object.max_dpi
                                )
        spinbox.pack()            

        

        save_button = ctk.CTkButton(master=self, text="Save New Action", command=lambda: self.save_button_clicked(spinbox.get()), text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        save_button.pack()

    def save_button_clicked(self, dpi_change):      
        new_changedpi_object = self.settings_object.add_new_changedpi_action(dpi_change)
        
        new_button = self.action_selection_frame.create_changedpi_button(new_changedpi_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()






        # new_primary_key = self.settings_object.add_new_changedpi(self.spinbox.get())

        # if not isinstance(self.added_from, GestureRadioFrame):
        #     self.origin_frame.create_changedpi_radio_button_row(button_config_id=new_primary_key)
        #     self.origin_frame.changedpi_radio_buttons_frame.grid(row=5, column=0)
        # else:
        #     self.added_from.create_changedpi_radio_button_row(gesture_id=new_primary_key)
        #     self.added_from.changedpi_radio_buttons_frame.grid(row=5, column=0)
        
        # self.go_back_function()




class NewActionFrame(ctk.CTkFrame):
    def __init__(self, master, root, origin_frame, action_selection_frame, settings_object):
        super().__init__(master, corner_radius=0, fg_color='transparent')
        self.origin_frame=origin_frame        


        title=ctk.CTkLabel(master=self, text="Create New Action", font=ctk.CTkFont(size=40))
        title.pack()



        dark_colour = "#181818"
        segment_button_colour = gui_variables.blue_standard1

        options_frame = ctk.CTkFrame(master=self, fg_color=dark_colour)

        options = {}
        options["Keypress"] = AddKeypressFrame(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, root=root)
        options["Axis"] = AddAxisFrame1(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back)
        options["CycleDPI"] = AddCycleDPI1(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back)
        options["ChangeHost"] = AddChangeHost1(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back)
        options["ChangeDPI"] = AddChangeDPI1(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back)
        
        self.selected_option = "ChangeDPI"
        button_dict = {}
        segmented_frame = ctk.CTkFrame(master=self, fg_color=dark_colour)
        segmented_frame.pack()

        def button_callback(new_selected_button):
            if new_selected_button != self.selected_option:
                options[self.selected_option].pack_forget()
                options[new_selected_button].pack(fill="both", expand=True)
                button_dict[self.selected_option].configure(fg_color="transparent", hover=True, text_color=segment_button_colour)
                button_dict[new_selected_button].configure(fg_color=segment_button_colour, hover=False, text_color="black")
                self.selected_option = new_selected_button

        for i in ["Keypress", "Axis", "CycleDPI", "ChangeHost", "ChangeDPI"]:
            button_dict[i] = ctk.CTkButton(master=segmented_frame, text=i, command= lambda i=i: button_callback(i), text_color=segment_button_colour, width=180, height=40, fg_color='transparent', border_width=1, border_color=segment_button_colour, corner_radius=0)
            button_dict[i].pack(side="left")
        button_callback("Keypress")

        options_frame.pack(fill="both", expand=True)

        go_back_button = ctk.CTkButton(master=self, text="Cancel", command=lambda: self.go_back())
        go_back_button.pack(anchor="se")

        self.pack(fill="both", expand=True)

    def go_back(self):
        self.destroy()
        self.origin_frame.pack(fill="both", expand=True)


class AddActionFrame(ctk.CTkFrame):
    def __init__(self, master_frame, edit_config_frame_master, origin_frame, configuration, settings_object, added_from=None):
        super().__init__(master=master_frame, corner_radius=0, fg_color="transparent")  # Initialize the CTkFrame
        self.edit_config_frame_master = edit_config_frame_master
        self.master_frame = master_frame
        self.origin_frame = origin_frame
        self.configuration = configuration
        self.settings_object = settings_object
        self.added_from = added_from


        self.container_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        self.container_frame.pack_forget()

        go_back_button = ctk.CTkButton(master=self.container_frame, text="Cancel", command=self.go_back)
        go_back_button.grid(row=0, column=0)

        options = {}

        options_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        options_frame.grid(row=3, column=0)
        
        
        options["Keypress"] = KeyPressFrame(master=options_frame, go_back_function=self.go_back, origin_frame=self.origin_frame, app_root=self.edit_config_frame_master, settings_object=self.settings_object, added_from=self.added_from)
        options["Axis"] = AddAxisFrame(master=options_frame, go_back_function=self.go_back, origin_frame=self.origin_frame, app_root=self.edit_config_frame_master, settings_object=self.settings_object, added_from=self.added_from)
        options["CycleDPI"] = AddCycleDPI(master=options_frame, go_back_function=self.go_back, origin_frame=self.origin_frame, app_root=self.edit_config_frame_master, settings_object=self.settings_object, max_dpi=configuration.max_dpi, min_dpi = configuration.min_dpi, added_from=self.added_from)
        options["ChangeHost"] = AddChangeHost(master=options_frame, go_back_function=self.go_back, origin_frame=self.origin_frame, app_root=self.edit_config_frame_master, settings_object=self.settings_object, added_from=self.added_from)
        options["ChangeDPI"] = AddChangeDPI(master=options_frame, go_back_function=self.go_back, origin_frame=self.origin_frame, app_root=self.edit_config_frame_master, settings_object=self.settings_object, added_from=self.added_from)
        options["Keypress"].pack()
        self.selected_option = "Keypress"

        def segmented_button_callback(value):
            options[self.selected_option].pack_forget()
            options[value].pack()
            self.selected_option = value

        segmented_button = ctk.CTkSegmentedButton(master=self.container_frame)
        segmented_button.configure(values=[i for i in options.keys()], command=segmented_button_callback)
        segmented_button.grid(row=1, column=0)
        segmented_button.set("Keypress")  

        self.container_frame.pack()

    def go_back(self):
        self.origin_frame.pack()
        self.destroy()

    def pack(self, *args, **kwargs):
        """
        Allows AddActionFrame to be packed like a regular widget.
        Passes all arguments to its container_frame's pack method.
        """
        self.container_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)


class GestureRadioFrame(ctk.CTkFrame):
    def __init__(self, config_object, container_outer_frame, master_frame, edit_config_frame_instance, configuration, edit_config_frame_master, *args, **kwargs): 
        super().__init__(fg_color="transparent", *args, **kwargs) 
    

    
        self.config_object = config_object
        radio_buttons_to_create = []
        self.radio_buttons_dictionary = {}

        self.container_outer_frame = container_outer_frame 
        self.master_frame = master_frame
        self.edit_config_frame_instance = edit_config_frame_instance
        self.configuration = configuration
        self.edit_config_frame_master = edit_config_frame_master
    

        mode_stringvar = ctk.StringVar(value=self.config_object.mode)
        mode_dropdown = ctk.CTkOptionMenu(master=self,
                                               variable=mode_stringvar,
                                               values=["OnRelease", "OnInterval", "OnThreshold"],
                                               state="normal",
                                               width=200,
                                               height=36,
                                            command=lambda new_mode=mode_stringvar: self.config_object.update_mode(new_mode)
                                               )
        mode_dropdown.grid(row=0, column=0)

        threshold_spinbox = IntSpinbox(master=self,
                                       db_query=self.config_object.update_threshold,
                                        width=140,
                                        step_size=1,
                                        max_value=99999,
                                        min_value=1,
                                        value=self.config_object.threshold
        )
        threshold_spinbox.grid(row=0, column=1)




        def show_new_action_frame():

            self.edit_config_frame_instance.add_action_frame = AddActionFrame(

                                            # Need to figure out 
                                            origin_frame=self.edit_config_frame_instance.frames[self.edit_config_frame_instance.currently_selected_menu],
                                            added_from=self,

                                            
                                            master_frame=self.master_frame,
                                            edit_config_frame_master = self.edit_config_frame_master,
                                            configuration = self.configuration,
                                            settings_object = self.config_object,
                                            )
            self.container_outer_frame.pack_forget()



    
        add_new_action_button = ctk.CTkButton(master=self, command= lambda: show_new_action_frame(), text="Add New Button Action")
        add_new_action_button.grid(row=99, column=0)



        if config_object.gesture_nopress is not None:
            radio_buttons_to_create.append(["No Press", config_object.gesture_nopress])
        if config_object.gesture_togglesmartshift is not None:
            radio_buttons_to_create.append(["Toggle Smart Shift", config_object.gesture_togglesmartshift])
        if config_object.gesture_togglehiresscroll is not None:
            radio_buttons_to_create.append(["Toggle Hi Res Scroll", config_object.gesture_togglehiresscroll])



        radio_buttons_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        radio_buttons_frame.grid(row=1, column=0)



        for i,v in enumerate(radio_buttons_to_create):
            radio_button_row = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
            radio_button_row.grid(row=i, column=0)

            radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=v[0], command=lambda c=v[1]: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            

            if config_object.selected_gesture_id == v[1]:
                radio_button.radio_button_clicked()



            self.radio_buttons_dictionary[v[1]] = radio_button











        self.keypress_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
        self.keypress_radio_buttons_frame.grid(row=2, column=0)


        if len(self.config_object.gesture_keypresses) > 0:
            for i in self.config_object.gesture_keypresses.keys():
                self.create_keypress_radio_button_row(i=i)
        else:
            self.keypress_radio_buttons_frame.grid_forget()



        self.changehost_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
        self.changehost_radio_buttons_frame.grid(row=4, column=0)

        if len(self.config_object.gesture_changehost) > 0:
            for i in self.config_object.gesture_changehost.keys():
                self.create_changehost_radio_button_row(gesture_id=i)
        else:
            self.changehost_radio_buttons_frame.grid_forget()


        self.axis_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
        self.axis_radio_buttons_frame.grid(row=7, column=0)

        if len(self.config_object.gesture_axes) > 0:
            for i in self.config_object.gesture_axes.keys():
                self.create_axes_radio_button_row(gesture_id=i)
        else:
            self.axis_radio_buttons_frame.grid_forget()



        self.changedpi_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
        self.changedpi_radio_buttons_frame.grid(row=5, column=0)

        if len(self.config_object.gesture_changedpi) > 0:
            for i in self.config_object.gesture_changedpi.keys():
                self.create_changedpi_radio_button_row(gesture_id=i)
        else:
            self.changedpi_radio_buttons_frame.grid_forget()



        self.cycledpi_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
        self.cycledpi_radio_buttons_frame.grid(row=6, column=0)

        if len(self.config_object.gesture_cycledpi) > 0:
            for i in self.config_object.gesture_cycledpi.keys():
                self.create_cycledpi_radio_button_row(gesture_id=i)
        else:
            self.cycledpi_radio_buttons_frame.grid_forget()





    def create_cycledpi_radio_button_row(self, gesture_id):
        cycledpi_button_row = ctk.CTkFrame(master=self.cycledpi_radio_buttons_frame, fg_color="transparent")
        cycledpi_button_row.pack()

        radio_button = MatthewsRadioButton(master=cycledpi_button_row, width=600, text=f"cycledpi {self.config_object.gesture_cycledpi[gesture_id].dpi_array}", command=lambda c=gesture_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

        if self.config_object.selected_gesture_id == gesture_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[gesture_id] = radio_button

        delete_cycledpi_button = ctk.CTkButton(
                master=cycledpi_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=gesture_id, f=cycledpi_button_row, : self.cycledpi_deletion_warning(c, f,)
        )
        delete_cycledpi_button.grid(row=0, column=3, pady="5", sticky="e")

        cycledpi_button_row.columnconfigure(1, weight=2)



    def create_changedpi_radio_button_row(self, gesture_id):
        changedpi_button_row = ctk.CTkFrame(master=self.changedpi_radio_buttons_frame, fg_color="transparent")
        changedpi_button_row.pack()

        radio_button = MatthewsRadioButton(master=changedpi_button_row, width=600, 
                                           text=f"Changedpi {self.config_object.gesture_changedpi[gesture_id].increment}",
                                             command=lambda c=gesture_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")

        if self.config_object.selected_gesture_id == gesture_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[gesture_id] = radio_button
        delete_changedpi_button = ctk.CTkButton(
                master=changedpi_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=gesture_id, f=changedpi_button_row, : self.changedpi_deletion_warning(c, f,)
        )
        delete_changedpi_button.grid(row=0, column=3, pady="5", sticky="e")

        changedpi_button_row.columnconfigure(1, weight=2)



    def select_configuration(self, gesture_id):
        try:
            Classes.update_selected_gesture_id(gesture_id)
            self.radio_buttons_dictionary[self.config_object.selected_gesture_id].another_button_clicked()
            self.config_object.selected_gesture_id = gesture_id
        except KeyError:
            pass




    def create_keypress_radio_button_row(self, i):     
        keypress_button_row = ctk.CTkFrame(master=self.keypress_radio_buttons_frame, fg_color="transparent")                
        keypress_button_row.pack()

        radio_button = MatthewsRadioButton(master=keypress_button_row, width=300, 
                                        #    text=f"Keypress",
                                           text=f"Keypress: {self.config_object.gesture_keypresses[i].keypresses[0:29]}",
                                            #  font=ctk.CTkFont(family="Noto Sans", size=12),
                                               command=lambda c=i: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

        if self.config_object.selected_gesture_id == i:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[i] = radio_button

        # edit_keypress_button = ctk.CTkButton(
        #         master=keypress_button_row,
        #         height=20,
        #         width=80,
        #         text="Edit",
        #         fg_color="transparent",
        #         # border_color="red",
        #         font=ctk.CTkFont(family="Noto Sans"),
        #         text_color="#6C757D",
        #         border_color="#6C757D",
        #         hover_color="#450C0F",
        #         border_width=1,
        #         corner_radius=2,
        #         # command=
        # )
        # edit_keypress_button.grid(row=0, column=2, pady="5", sticky="e")

        delete_keypress_button = ctk.CTkButton(
                master=keypress_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=i, f=keypress_button_row, : self.keypress_deletion_warning(c, f,)
        )
        delete_keypress_button.grid(row=0, column=3, pady="5", sticky="e")

        keypress_button_row.columnconfigure(1, weight=2)



    def axis_deletion_warning(self, c, f):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.config_object.selected_gesture_id == c:
                self.radio_buttons_dictionary[self.config_object.gesture_nopress].radio_button_clicked()
            self.config_object.delete_axis(gesture_id=c)
            f.destroy()
            if len(self.config_object.gesture_axes) == 0:
                self.axis_radio_buttons_frame.grid_forget()




    def keypress_deletion_warning(self, c, f,):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.config_object.selected_gesture_id == c:
                self.radio_buttons_dictionary[self.config_object.gesture_nopress].radio_button_clicked()
            self.config_object.delete_keypresses(gesture_id=c)
            f.destroy()
            if len(self.config_object.gesture_keypresses) == 0:
                self.keypress_radio_buttons_frame.grid_forget()



    def create_changehost_radio_button_row(self, gesture_id):
        changehost_button_row = ctk.CTkFrame(master=self.changehost_radio_buttons_frame, fg_color="transparent")
        changehost_button_row.pack()

        radio_button = MatthewsRadioButton(master=changehost_button_row, width=600, text=f"Changehost {self.config_object.gesture_changehost[gesture_id].host_change}", command=lambda c=gesture_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

        if self.config_object.selected_gesture_id == gesture_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[gesture_id] = radio_button



        delete_changehost_button = ctk.CTkButton(
                master=changehost_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=gesture_id, f=changehost_button_row, t=self.config_object.gesture_changehost[gesture_id].host_change : self.changehost_deletion_warning(c, f, t)
        )
        delete_changehost_button.grid(row=0, column=3, pady="5", sticky="e")



    def create_axes_radio_button_row(self, gesture_id):
        axis_button_row = ctk.CTkFrame(master=self.axis_radio_buttons_frame, fg_color="transparent")
        axis_button_row.pack()

        radio_button = MatthewsRadioButton(master=axis_button_row, width=600,
                                            text=f"Axis {self.config_object.gesture_axes[gesture_id].axis_button}: {self.config_object.gesture_axes[gesture_id].axis_multiplier}",
                                             command=lambda c=gesture_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")

        if self.config_object.selected_gesture_id == gesture_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[gesture_id] = radio_button

        delete_axis_button = ctk.CTkButton(master=axis_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=gesture_id, f=axis_button_row, : self.axis_deletion_warning(c, f,)
                                           )
        delete_axis_button.grid(row=0, column=3, pady="5", sticky="e")

        axis_button_row.columnconfigure(1, weight=2)




class GestureFrame(ctk.CTkFrame):
    def __init__(self, button, container_outer_frame, master_frame, edit_config_frame_instance, configuration, edit_config_frame_master, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        if button.gesture_support == False:
            pass

        self.container_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.container_frame.pack(fill="both", expand="true")

        self.gesture_dict = button.gesture_dict

        button_label2 = ctk.CTkLabel(master=self.container_frame, text = f"GESTURES HERE ({button.button_cid})")
        button_label2.grid(row=0, column=0)

        def create_gesture_radio_frame(i):
            self.gesture_radio_frames[i] = GestureRadioFrame(master=self.container_frame, config_object=self.gesture_dict[i], container_outer_frame=container_outer_frame, master_frame=master_frame, edit_config_frame_instance=edit_config_frame_instance, configuration=configuration, edit_config_frame_master=edit_config_frame_master)

        self.currently_selected_menu = "Up"
        def segmented_button_callback(value):
            if value not in self.gesture_radio_frames.keys():
                create_gesture_radio_frame(value)
            self.gesture_radio_frames[self.currently_selected_menu].grid_forget()
            self.gesture_radio_frames[value].grid(row=2, column=0)
            self.currently_selected_menu = value


        segmented_button = ctk.CTkSegmentedButton(master=self.container_frame,
                                                            values=[i for i in self.gesture_dict.keys()],
                                                            command=segmented_button_callback)
        segmented_button.grid(row=1, column=0)
        segmented_button.set("Up")

        self.gesture_radio_frames = {}

        create_gesture_radio_frame("Up")

        self.gesture_radio_frames["Up"].grid(row=2, column=0)



class ButtonConfigFrame():
    def __init__(self, edit_config_frame_master,
                  edit_config_frame_instance,
                    master_frame, configuration, button,
                    # toggle_second_scrollable_frame,
                    # second_scrollable_frame
                      ): 
        self.edit_config_frame_master = edit_config_frame_master
        self.edit_config_frame_instance = edit_config_frame_instance
        self.master_frame = master_frame
        self.configuration = configuration
        self.button = button




        self.container_outer_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        self.container_outer_frame.pack_forget()



        self.container_frame = ctk.CTkFrame(master=self.container_outer_frame, corner_radius=0, fg_color="transparent")
        # self.container_frame.grid(row=0, column=0)
        self.container_frame.pack(side="left")

    





        button_label = ctk.CTkLabel(master=self.container_frame, text = f"{button.button_name} ({button.button_cid})")
        button_label.grid(row=0, column=0)

        def show_new_action_frame():

            self.edit_config_frame_instance.add_action_frame = AddActionFrame(
                                            origin_frame=self.edit_config_frame_instance.frames[self.edit_config_frame_instance.currently_selected_menu],
                                            master_frame=self.master_frame,
                                            edit_config_frame_master = self.edit_config_frame_master,

                                            configuration = self.configuration,
                                            settings_object = self.button,
                                            )
            self.container_outer_frame.pack_forget()



        add_new_action_button = ctk.CTkButton(master=self.container_frame, command= lambda: show_new_action_frame(), text="Add New Action")
        add_new_action_button.grid(row=99, column=0)

        self.container_frame2 = None


        radio_buttons_to_create = []
        self.radio_buttons_dictionary = {}

        if button.button_default is not None:
            radio_buttons_to_create.append(["Default", button.button_default])
        if button.button_nopress is not None:
            radio_buttons_to_create.append(["No Press", button.button_nopress])
        if button.button_togglesmartshift is not None:
            radio_buttons_to_create.append(["Toggle Smart Shift", button.button_togglesmartshift])
        if button.button_togglehiresscroll is not None:
            radio_buttons_to_create.append(["Toggle Hi Res Scroll", button.button_togglehiresscroll])

        radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        radio_buttons_frame.grid(row=1, column=0, sticky="w")



        for i,v in enumerate(radio_buttons_to_create):
            radio_button_row = ctk.CTkFrame(master=radio_buttons_frame, fg_color="transparent")
            radio_button_row.grid(row=i, column=0, sticky="w", padx=0, pady=0)
            # radio_button_row.pack(side="left")

            radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=v[0], command=lambda c=v[1]: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            

            if button.selected_button_config_id == v[1]:
                radio_button.radio_button_clicked()



            self.radio_buttons_dictionary[v[1]] = radio_button

        if button.button_gestures is not None:
            self.gesture_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
            self.gesture_frame.grid(row=2, column=0, sticky="w", padx=0, pady=0)
            radio_button = MatthewsRadioButton(master=self.gesture_frame, width=600, text="Gestures", command=lambda c=button.button_gestures: self.select_configuration(c))
            radio_button.pack()
            if button.selected_button_config_id == button.button_gestures:
                radio_button.radio_button_clicked()
            self.radio_buttons_dictionary[button.button_gestures] = radio_button

            # radio_buttons_to_create.append(["Gestures", button.button_gestures])

        self.keypress_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        self.keypress_radio_buttons_frame.grid(row=3, column=0, sticky="w")


        if len(button.button_keypresses) > 0:
            for i in button.button_keypresses.keys():
                self.create_keypress_radio_button_row(i=i)
        else:
            self.keypress_radio_buttons_frame.grid_forget()

        self.changehost_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        self.changehost_radio_buttons_frame.grid(row=4, column=0, sticky="w")

        if len(button.button_changehost) > 0:
            for i in button.button_changehost.keys():
                self.create_changehost_radio_button_row(button_config_id=i)
        else:
            self.changehost_radio_buttons_frame.grid_forget()


        self.changedpi_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        self.changedpi_radio_buttons_frame.grid(row=5, column=0, sticky="w")

        if len(button.button_changedpi) > 0:
            for i in button.button_changedpi.keys():
                self.create_changedpi_radio_button_row(button_config_id=i)
        else:
            self.changedpi_radio_buttons_frame.grid_forget()



        self.cycledpi_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        self.cycledpi_radio_buttons_frame.grid(row=6, column=0, sticky="w")

        if len(button.button_cycledpi) > 0:
            for i in button.button_cycledpi.keys():
                self.create_cycledpi_radio_button_row(button_config_id=i)
        else:
            self.cycledpi_radio_buttons_frame.grid_forget()


        self.axis_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame, fg_color="transparent")
        self.axis_radio_buttons_frame.grid(row=7, column=0, sticky="w")


        if len(button.button_axes) > 0:
            for i in button.button_axes.keys():
                self.create_axes_radio_button_row(button_config_id=i)
        else:
            self.axis_radio_buttons_frame.grid_forget()


    def create_cycledpi_radio_button_row(self, button_config_id):
        cycledpi_button_row = ctk.CTkFrame(master=self.cycledpi_radio_buttons_frame, width=600, height=50, fg_color="transparent")
        cycledpi_button_row.pack()
        cycledpi_button_row.pack_propagate(False)
        
        hidden_frame = ctk.CTkFrame(master=cycledpi_button_row, fg_color="transparent")
        cycledpi_dpi_array = ctk.CTkLabel(master=cycledpi_button_row, text=self.button.button_cycledpi[button_config_id].dpi_array, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=cycledpi_button_row, width=100, 
                                        text="CycleDPI", 
                                        command=lambda c=button_config_id: self.select_configuration(c),
                                        hover_elements=(hidden_frame, cycledpi_dpi_array))
        radio_button.pack(side="left", anchor="w")
        
        if self.button.selected_button_config_id == button_config_id:
            radio_button.radio_button_clicked()
            
        self.radio_buttons_dictionary[button_config_id] = radio_button

        delete_cycledpi_button = ctk.CTkButton(
            master=cycledpi_button_row,
            height=20,
            width=80,
            text="Delete",
            fg_color="transparent",
            font=ctk.CTkFont(family="Noto Sans"),
            text_color="#6C757D",
            border_color="#6C757D",
            hover_color="#450C0F",
            border_width=1,
            corner_radius=2,
            command=lambda c=button_config_id, f=cycledpi_button_row: self.cycledpi_deletion_warning(c, f)
        )

        cycledpi_dpi_array.pack(anchor="w", pady=0, side="left", fill="x")
        delete_cycledpi_button.pack(side="right", anchor="e")
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)


    def create_changedpi_radio_button_row(self, button_config_id):
        changedpi_button_row = ctk.CTkFrame(master=self.changedpi_radio_buttons_frame, width=600, height=50, fg_color="transparent")
        changedpi_button_row.pack()
        changedpi_button_row.pack_propagate(False)

        hidden_frame = ctk.CTkFrame(master=changedpi_button_row, fg_color="transparent")
        changedpi_increment = ctk.CTkLabel(master=changedpi_button_row, text=self.button.button_changedpi[button_config_id].increment, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=changedpi_button_row, width=100, 
                                           text=f"ChangeDPI",
                                             command=lambda c=button_config_id: self.select_configuration(c),
                                             hover_elements=(hidden_frame, changedpi_increment)
                                             )
        radio_button.pack(side="left", anchor="w")        
        
        # radio_button.grid(row=0, column=0, sticky="w")

        if self.button.selected_button_config_id == button_config_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[button_config_id] = radio_button
        delete_changedpi_button = ctk.CTkButton(
                master=changedpi_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=button_config_id, f=changedpi_button_row, : self.changedpi_deletion_warning(c, f,)
        )
        # delete_changedpi_button.grid(row=0, column=3, pady="5", sticky="e")
        changedpi_increment.pack(anchor="w",pady=0,side="left",fill="x",)
        delete_changedpi_button.pack(side="right", anchor="e")
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)



    def create_changehost_radio_button_row(self, button_config_id):
        changehost_button_row = ctk.CTkFrame(master=self.changehost_radio_buttons_frame, width=600, height=50, fg_color="transparent")
        changehost_button_row.pack()
        changehost_button_row.pack_propagate(False)
        hidden_frame = ctk.CTkFrame(master=changehost_button_row, fg_color="transparent")

        changehost_text = ctk.CTkLabel(master=changehost_button_row, text="Previous" if self.button.button_changehost[button_config_id].host_change == "prev" else self.button.button_changehost[button_config_id].host_change.title(), text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=changehost_button_row, width=100, text=f"ChangeHost", command=lambda c=button_config_id: self.select_configuration(c), hover_elements=(hidden_frame, changehost_text))
        radio_button.pack(side="left", anchor="w")        

        if self.button.selected_button_config_id == button_config_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[button_config_id] = radio_button

        delete_changehost_button = ctk.CTkButton(
                master=changehost_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=button_config_id, f=changehost_button_row, t=self.button.button_changehost[button_config_id].host_change : self.changehost_deletion_warning(c, f, t)
        )

        changehost_text.pack(anchor="w",pady=0,side="left",fill="x",)
        delete_changehost_button.pack(side="right", anchor="e")
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)




    def create_axes_radio_button_row(self, button_config_id):
        axis_button_row = ctk.CTkFrame(master=self.axis_radio_buttons_frame, width=600, height=50, fg_color="transparent")
        axis_button_row.pack()
        axis_button_row.pack_propagate(False)
        hidden_frame = ctk.CTkFrame(master=axis_button_row, fg_color="transparent")
        axis_info1 = ctk.CTkLabel(master=axis_button_row, text=f"{self.button.button_axes[button_config_id].axis_button}: ",
                                     text_color="#6C757D")
        axis_info2 = ctk.CTkLabel(master=axis_button_row, text=self.button.button_axes[button_config_id].axis_multiplier, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=axis_button_row, width=100,
                                            text=f"Axis:",
                                             command=lambda c=button_config_id: self.select_configuration(c),
                                             hover_elements=(hidden_frame, axis_info1, axis_info2))
        radio_button.pack(side="left", anchor="w")
        if self.button.selected_button_config_id == button_config_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[button_config_id] = radio_button

        delete_axis_button = ctk.CTkButton(master=axis_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=button_config_id, f=axis_button_row, : self.axis_deletion_warning(c, f,)
                                           )
        # delete_axis_button.grid(row=0, column=3, pady="5", sticky="e")


        axis_info1.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
        )

        axis_info2.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
        )
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)


        delete_axis_button.pack(side="right", anchor="e")




    def axis_deletion_warning(self, c, f):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_axis(button_config_id=c)
            f.destroy()
            if len(self.button.button_axes) == 0:
                self.axis_radio_buttons_frame.grid_forget()




    def create_keypress_radio_button_row(self, i):     
        keypress_button_row = ctk.CTkFrame(master=self.keypress_radio_buttons_frame, width=600, height=50, fg_color="transparent")                
        keypress_button_row.pack(anchor="w", fill="both", expand="true")
        keypress_button_row.pack_propagate(False)  # Prevent the frame from resizing to fit its children

        list_representation = ast.literal_eval(self.button.button_keypresses[i].keypresses)

        keypress_text = ""
        for key in list_representation:
            key = keymates.get_keymates(key.replace("KEY_", ""))[1]
            keypress_text = keypress_text + key + " "

        hidden_frame = ctk.CTkFrame(master=keypress_button_row, fg_color="transparent")
        keypress_keys = ctk.CTkLabel(master=keypress_button_row, text=keypress_text,
                                     text_color="#6C757D")

            

        radio_button = MatthewsRadioButton(master=keypress_button_row, width=100, 
                                           text=f"Keypresses:",
                                               command=lambda c=i: self.select_configuration(c),
                                               hover_elements=(keypress_keys, hidden_frame),)
           
        radio_button.pack(side="left", anchor="w")

        if self.button.selected_button_config_id == i:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[i] = radio_button

        delete_keypress_button = ctk.CTkButton(
                master=keypress_button_row,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda c=i, f=keypress_button_row, : self.keypress_deletion_warning(c, f,)
        )
        delete_keypress_button.pack(side="right", anchor="e")
        

        keypress_keys.pack(
            anchor="w",
            pady=3,
            side="left",
            fill="x",
        )
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)



    def axis_deletion_warning(self, c, f):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_axis(button_config_id=c)
            f.destroy()
            if len(self.button.button_axes) == 0:
                self.axis_radio_buttons_frame.grid_forget()



    def cycledpi_deletion_warning(self, c, f):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_cycledpi(button_config_id=c)
            f.destroy()
            if len(self.button.button_cycledpi) == 0:
                self.cycledpi_radio_buttons_frame.grid_forget()





    def changedpi_deletion_warning(self, c, f):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_changedpi(button_config_id=c)
            f.destroy()
            if len(self.button.button_changedpi) == 0:
                self.changedpi_radio_buttons_frame.grid_forget()




    def keypress_deletion_warning(self, c, f,):
        msg = CTkMessagebox(title="Delete Action?",
                                message="Delete action?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_keypresses(button_config_id=c)
            f.destroy()
            if len(self.button.button_keypresses) == 0:
                self.keypress_radio_buttons_frame.grid_forget()




    def changehost_deletion_warning(self, c, f, t=''):
        msg = CTkMessagebox(title="Delete Action?",
                                message=f"Delete action: ChangeHost {t}?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=800,
                                height=400,
                                fade_in_duration=200,
                                )

        if msg.get() == "Delete":
            if self.button.selected_button_config_id == c:
                self.radio_buttons_dictionary[self.button.button_default].radio_button_clicked()
            self.button.delete_changehost(button_config_id=c)
            f.destroy()
            if len(self.button.button_changehost) == 0:
                self.changehost_radio_buttons_frame.grid_forget()



    def select_configuration(self, button_configuration_id):
        if self.button.gesture_support == True:
            
            # if not hasattr(self, "gesture_buttons"):
            #     gesture_buttons = {}

            #     for i in ["Up", "Down", "Left", "Right", "None"]:
            #         gesture_button = ctk.CTkButton(master=)
            #         # device_button = ctk.CTkButton(master=self.left_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=i.device_name, font=ctk.CTkFont(family="Noto Sans",size=18 ), command=lambda d=i.device_id: self.button_clicked(d), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            #         # device_button.pack(fill="x", expand=True)
            #         # self.button_objects_dict[i.device_id] = device_button
                


            if button_configuration_id == self.button.button_gestures:
                if self.container_frame2 == None:
                    self.container_frame2 = GestureFrame(master=self.container_outer_frame, button=self.button, container_outer_frame=self.container_outer_frame, master_frame=self.master_frame, edit_config_frame_instance=self.edit_config_frame_instance, 
                                                        configuration=self.configuration, edit_config_frame_master=self.edit_config_frame_master, corner_radius=0, fg_color="transparent")
                    # self.container_frame2.grid(row=0, column=1)
                    self.container_frame2.pack(side="right", anchor="n")
                else:
                    self.container_frame2.container_frame.pack()
            elif self.container_frame2 != None:
                    self.container_frame2.container_frame.pack_forget()
        try:
            Classes.update_selected_button_config_id(button_configuration_id)
            self.radio_buttons_dictionary[self.button.selected_button_config_id].another_button_clicked()
            self.button.selected_button_config_id = button_configuration_id
        except KeyError:
            pass


    def pack(self, *args, **kwargs):
        """
        Allows ButtonConfigFrame to be packed like a regular widget.
        Passes all arguments to its container_frame's pack method.
        """
        # self.container_outer_frame.pack(*args, **kwargs)
        self.container_outer_frame.pack(fill="both", expand=True)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_outer_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_outer_frame.destroy(*args, **kwargs)






class ThumbwheelFrame():
    def __init__(self, master_frame, scroll_properties, configuration): 
        self.master_frame = master_frame
        self.configuration = configuration
        self.scroll_properties = scroll_properties

        self.container_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        self.container_frame.pack_forget()

        thumbwheel_frame_label = ctk.CTkLabel(master=self.container_frame, text = "Thumbwheel Frame")
        thumbwheel_frame_label.grid(row=0, column=0, columnspan=2)



        thumbwheel_divert_var = ctk.BooleanVar(value=configuration.thumbwheel_divert)
        thumbwheel_divert_checkbox = ctk.CTkCheckBox(master=self.container_frame, text="Thumbwheel Divert", command=lambda configuration=configuration: self.thumbwheel_divert_event(configuration),
                                            variable=thumbwheel_divert_var, onvalue=True, offvalue=False)
        thumbwheel_divert_checkbox.grid(row=2, column=0)

        thumbwheel_invert_var = ctk.BooleanVar(value=configuration.thumbwheel_invert)
        thumbwheel_invert_checkbox = ctk.CTkCheckBox(master=self.container_frame, text="Thumbwheel Invert", command=lambda configuration=configuration: self.thumbwheel_invert_event(configuration),
                                            variable=thumbwheel_invert_var, onvalue=True, offvalue=False)
        thumbwheel_invert_checkbox.grid(row=2, column=1)

        def create_thumbwheel_controls(direction):
            threshold_label = ctk.CTkLabel(
                master=self.container_frame,
                text=f"Thumbwheel {direction} Threshold"
            )
        
            spinbox = IntSpinbox(master=self.container_frame,
                                 db_query=self.scroll_properties.update_left_threshold if direction == "Left" else self.scroll_properties.update_right_threshold,
                                 value=scroll_properties.scroll_left_threshold if direction == "Left" else scroll_properties.scroll_right_threshold,
                                width=200,
                                step_size=5,
                                min_value=1,
                                max_value=9999
                                )
            
            mode_label = ctk.CTkLabel(
            master=self.container_frame,
            text = f"Thumbwheel {direction} Mode"
        )
            mode_dropdown = ctk.CTkOptionMenu(master=self.container_frame,
                                                variable=ctk.StringVar(value=scroll_properties.scroll_left_mode if direction=="Left" else scroll_properties.scroll_right_mode),
                                                values=["OnInterval", "OnThreshold"],
                                                state="normal",
                                                width=200,
                                                height=36,
                                                command=self.update_scroll_left_mode if direction=="Left" else self.update_scroll_right_mode)


            return threshold_label, spinbox, mode_label, mode_dropdown

        thumbwheel_left_threshold_label, self.thumbwheel_left_spinbox, thumbwheel_left_mode_label, self.scroll_left_mode_dropdown = create_thumbwheel_controls("Left")
        thumbwheel_left_threshold_label.grid(row=5, column=0)
        self.thumbwheel_left_spinbox.grid(row=6, column=0)
        thumbwheel_left_mode_label.grid(row=5, column=1)
        self.scroll_left_mode_dropdown.grid(row=6, column=1)

        thumbwheel_right_threshold_label, self.thumbwheel_right_spinbox, thumbwheel_right_mode_label, self.scroll_right_mode_dropdown = create_thumbwheel_controls("Right")
        thumbwheel_right_threshold_label.grid(row=5, column=2)
        self.thumbwheel_right_spinbox.grid(row=6, column=2)
        thumbwheel_right_mode_label.grid(row=5, column=3)
        self.scroll_right_mode_dropdown.grid(row=6, column=3)














        radio_buttons_to_create = []
        self.radio_buttons_dictionary = {}
    
    #     if button.button_default is not None:
    #         radio_buttons_to_create.append(["Default", button.button_default])
    #     if button.button_nopress is not None:
    #         radio_buttons_to_create.append(["No Press", button.button_nopress])
    #     if button.button_togglesmartshift is not None:
    #         radio_buttons_to_create.append(["Toggle Smart Shift", button.button_togglesmartshift])
    #     if button.button_togglehiresscroll is not None:
    #         radio_buttons_to_create.append(["Toggle Hi Res Scroll", button.button_togglehiresscroll])
    #     if button.button_gestures is not None:
    #         radio_buttons_to_create.append(["Gestures", button.button_gestures])

    #     self.selected_button_configuration = ctk.StringVar()

    #     radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
    #     radio_buttons_frame.grid(row=1, column=0)


    #     radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
    #     radio_buttons_frame.grid(row=2, column=0)

    #     for i in radio_buttons_to_create:
    #         radio_button_row = ctk.CTkFrame(master=radio_buttons_frame)
    #         radio_button_row.pack()

    #         radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=i[0], command=lambda c=i[1]: self.select_configuration(c))
    #         radio_button.grid(row=0, column=0)            

    #         if button.selected_button_config_id == i[1]:
    #             radio_button.radio_button_clicked()

    #         self.radio_buttons_dictionary[i[1]] = radio_button


    # def select_configuration(self, button_configuration_id):
    #     try:
    #         Classes.update_selected_button_config_id(button_configuration_id)
    #         self.radio_buttons_dictionary[self.button.selected_button_config_id].another_button_clicked()
    #         self.button.selected_button_config_id = button_configuration_id
    #     except KeyError:
    #         pass






















    def update_scroll_left_mode(self, new_mode):
        self.scroll_properties.scroll_left_mode = new_mode

    def update_scroll_right_mode(self, new_mode):
        self.scroll_properties.scroll_right_mode = new_mode


    def thumbwheel_divert_event(self, configuration):
        configuration.thumbwheel_divert = not(configuration.thumbwheel_divert)

    def thumbwheel_invert_event(self, configuration):
        configuration.thumbwheel_invert = not(configuration.thumbwheel_invert)

    def pack(self, *args, **kwargs):
        self.container_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)




class Checkbox(ctk.CTkCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(font=("Roboto", 14), corner_radius=0, onvalue=True, offvalue=False, checkbox_width=26, checkbox_height=26,
                         text_color=gui_variables.text_grey1,
                        #  fg_color=gui_variables.blue_standard1,
                        hover_color=gui_variables.grey_standard1,
                         border_width=3,
                          *args, **kwargs)


class CycleDPIRadioButton(ctk.CTkFrame):
    def __init__(self, master, cycledpi_object, delete_command, passthrough_command, *args, **kwargs):
        super().__init__(master, fg_color="transparent", width=600, height=50, *args, **kwargs)
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()

        self.pack_propagate(False)
        cycledpi_dpi_array = ctk.CTkLabel(master=self, text=cycledpi_object.dpi_array, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100, text="CycleDPI", command=lambda: passthrough_command(), hover_elements=(cycledpi_dpi_array))
        radio_button.pack(side="left", anchor="w")
        
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()


        delete_cycledpi_button = ctk.CTkButton( master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=2, 
                                                command=lambda: (self.destroy(), delete_command()))
        cycledpi_dpi_array.configure(anchor="w", 
                                  justify="left")
        cycledpi_dpi_array.pack(anchor="w", pady=0, side="left", fill="x", expand=True)
        delete_cycledpi_button.pack(side="right", anchor="e")



class KeypressRadioButton(ctk.CTkFrame):
    def __init__(self, master, keypress_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=600, height=50)
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.pack_propagate(False)
        
        try:
            list_representation = ast.literal_eval(keypress_object.keypresses)
            keypress_text = ""
            for key in list_representation:
                key = keymates.get_keymates(key.replace("KEY_", ""))[1]
                keypress_text = keypress_text + key + " "
        except ValueError:
            keypress_text = keypress_object.keypresses

        keypress_keys = ctk.CTkLabel(master=self, text=keypress_text if len(keypress_text)<30 else f"{keypress_text[0:30]}...",
                                     text_color="#6C757D")

        radio_button = MatthewsRadioButton(master=self, width=100, text="Keypresses", command=lambda: passthrough_command(), hover_elements=(keypress_keys))
        radio_button.pack(side="left", anchor="w")
        keypress_keys.configure(anchor="w", 
                                  justify="left")
        keypress_keys.pack(
            anchor="w",
            pady=3,
            side="left",
            fill="x",
            expand=True
        )



        delete_keypress_button = ctk.CTkButton(master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=2, 
                                               command=lambda: (self.destroy(), delete_command())
                                               )
        delete_keypress_button.pack(side="right", anchor="e")
        


class ChangeDPIRadioButton(ctk.CTkFrame):
    def __init__(self, master, changedpi_object, delete_command, passthrough_command, *args, **kwargs):
        super().__init__(master, fg_color="transparent", width=600, height=50, *args, **kwargs)
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.pack_propagate(False)
        
        changedpi_increment = ctk.CTkLabel(master=self, text=changedpi_object.increment, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100, text=f"ChangeDPI",  command=lambda: passthrough_command(),  hover_elements=(changedpi_increment)  )
        radio_button.pack(side="left", anchor="w")        
        
        delete_changedpi_button = ctk.CTkButton(master=self,height=20,width=80,text="Delete",fg_color="transparent",font=ctk.CTkFont(family="Noto Sans"),text_color="#6C757D",border_color="#6C757D",hover_color="#450C0F",border_width=1,corner_radius=2,
                                                command=lambda: (self.destroy(), delete_command())
        )
        changedpi_increment.configure(anchor="w", 
                                  justify="left")
        changedpi_increment.pack(anchor="w",pady=0,side="left",fill="x", expand=True)
        delete_changedpi_button.pack(side="right", anchor="e")


class AxisRadioButton(ctk.CTkFrame):
    def __init__(self, master, axis_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=600, height=50)
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.pack_propagate(False)


        hidden_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        axis_info1 = ctk.CTkLabel(master=self, text=f"{axis_object.axis_button}: ",
                                     text_color="#6C757D")

        axis_info2 = ctk.CTkLabel(master=self, text=axis_object.axis_multiplier, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100,
                                            text=f"Axis:",
                                             command=lambda: passthrough_command(),
                                             hover_elements=(hidden_frame, axis_info1, axis_info2))
        radio_button.pack(side="left", anchor="w")


        delete_axis_button = ctk.CTkButton(master=self,
                height=20,
                width=80,
                text="Delete",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                command=lambda: (self.destroy(), delete_command())
                                           )


        axis_info1.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
        )

        axis_info2.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
        )
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)


        delete_axis_button.pack(side="right", anchor="e")


class TouchTapProxyFrame(ctk.CTkFrame):
    def __init__(self, master, root, ttt_object):
        super().__init__(master)
        # self.master=master
        self.label = ctk.CTkLabel(master=self, text=f"Thumbwheel {ttt_object.ttt}")
        self.label.pack()

        action_selection_frame = ActionSelectionFrame(master=self, root=root, actions=ttt_object)
        new_action_frame_button = ctk.CTkButton(master=self, text="Add New Action", command=lambda: (self.pack_forget(), NewActionFrame(master=master, root=root, 
                                                                                                                                        origin_frame=self,
                                                                                                                                         action_selection_frame=action_selection_frame,
                                                                                                                                          settings_object=ttt_object)))
        new_action_frame_button.pack()

        action_selection_frame.pack()



# class ActionSelectionFrame(ctk.CTkFrame):
#     def __init__(self, master, actions):
class ChangeHostRadioButton(ctk.CTkFrame):
    def __init__(self, master, changehost_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=600, height=50)
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.pack_propagate(False)
        
        hidden_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        changehost_text = ctk.CTkLabel(master=self, text="Previous" if changehost_object.host_change == "prev" else changehost_object.host_change.title(), text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100, text=f"ChangeHost", command=lambda: passthrough_command(), hover_elements=(hidden_frame, changehost_text))
        radio_button.pack(side="left", anchor="w")        

        changehost_text.pack(anchor="w",pady=0,side="left",fill="x",)

        delete_changehost_button = ctk.CTkButton(master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=2,
                    command=lambda: (self.destroy(), delete_command())
        )

        delete_changehost_button.pack(side="right", anchor="e")
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)



        # if hasattr(self.actions, "gestures"):
            # print("TODO gestures here")
# 

class ActionSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, root, actions, pack_order=None):
        super().__init__(master, fg_color="transparent")
        self.actions = actions

        self.radio_buttons_dictionary = {}

        def create_simple_button(id, name):
            radio_button_row = ctk.CTkFrame(master=self, fg_color="transparent")
            radio_button_row.pack()
            radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=name, command=lambda c=id: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            
            self.radio_buttons_dictionary[id] = radio_button


        for i in [(actions.default, "Default"), (actions.nopress, "NoPress"), (actions.togglesmartshift, "Toggle SmartShift"), (actions.togglehiresscroll, "Toggle Hi-res Scroll")]:
            if i[0] is not None:
                create_simple_button(id=i[0], name=i[1])

        if len(self.actions.cycledpi) > 0:
            for i in self.actions.cycledpi.values():
                self.create_cycledpi_button(i)

        if len(self.actions.changedpi) > 0:
            for i in self.actions.changedpi.values():
                self.create_changedpi_button(i)
                
        if len(self.actions.axes) > 0:
            for i in self.actions.axes.values():
                self.create_axis_button(i)

        if len(self.actions.keypresses) > 0:
            for i in self.actions.keypresses.values():
                self.create_keypress_button(i)

        if len(self.actions.changehost) > 0:
            for i in self.actions.changehost.values():
                self.create_changehost_button(i)

        if pack_order is not None:
            for i in pack_order:
                try:
                    self.radio_buttons_dictionary[i].pack(side="bottom")    
                except KeyError:
                    pass
        else:
            for i in self.radio_buttons_dictionary.values():
                i.pack(side="bottom")

        self.radio_buttons_dictionary[actions.selected_action_id].set_clicked()

    def create_changedpi_button(self, changedpi_object):
        radio_button = ChangeDPIRadioButton(master=self, changedpi_object=changedpi_object, delete_command=lambda n=changedpi_object.reference_id: (self.update_deleted_configuration(n), self.actions.delete_changedpi_action(n)), passthrough_command=lambda n=changedpi_object.reference_id: self.select_configuration(n))
        self.radio_buttons_dictionary[changedpi_object.reference_id] = radio_button
        return radio_button
    def create_cycledpi_button(self, cycledpi_object):
        radio_button = CycleDPIRadioButton(master=self, cycledpi_object=cycledpi_object, delete_command=lambda n=cycledpi_object.reference_id: (self.update_deleted_configuration(n), self.actions.delete_cycledpi_action(n)), passthrough_command=lambda n=cycledpi_object.reference_id: self.select_configuration(n))
        self.radio_buttons_dictionary[cycledpi_object.reference_id] = radio_button
        return radio_button
    def create_axis_button(self, axis_object):
        radio_button = AxisRadioButton(master=self, axis_object=axis_object, delete_command=lambda n=axis_object.reference_id: (self.update_deleted_configuration(n), self.actions.delete_axis_action(n)), passthrough_command=lambda n=axis_object.reference_id: self.select_configuration(n))
        self.radio_buttons_dictionary[axis_object.reference_id] = radio_button
        return radio_button
    def create_keypress_button(self, keypress_object):
        radio_button = KeypressRadioButton(master=self, keypress_object=keypress_object, delete_command=lambda n=keypress_object.reference_id: (self.update_deleted_configuration(n), self.actions.delete_keypress_action(n)), passthrough_command=lambda n=keypress_object.reference_id: self.select_configuration(n))
        self.radio_buttons_dictionary[keypress_object.reference_id] = radio_button
        return radio_button
    def create_changehost_button(self, changehost_object):
        radio_button = ChangeHostRadioButton(master=self, changehost_object=changehost_object, delete_command=lambda n=changehost_object.reference_id: (self.update_deleted_configuration(n), self.actions.delete_changehost_action(n)), passthrough_command=lambda n=changehost_object.reference_id: self.select_configuration(n))
        self.radio_buttons_dictionary[changehost_object.reference_id] = radio_button
        return radio_button
    def select_configuration(self, new_selected_id):
        self.radio_buttons_dictionary[self.actions.selected_action_id].another_button_clicked()
        self.actions.update_selected(new_selected_id=new_selected_id)

    def update_deleted_configuration(self, deleted_id):
        if deleted_id == self.actions.selected_action_id:
            if self.actions.default is not None:
                self.radio_buttons_dictionary[self.actions.default].set_clicked()
                self.actions.selected_action_id = self.actions.default
            else:
                # TODO double check expected behaviour
                self.radio_buttons_dictionary[self.actions.nopress].set_clicked()
                self.actions.selected_action_id = self.actions.nopress






class VerticalScrollwheelFrame():
    def __init__(self, master, root, configuration): 

        self.configuration = configuration
        
        self.container_frame = ctk.CTkFrame(master=master, corner_radius=0,
                                             fg_color="transparent"
                                            # fg_color="brown"
                                             )
        self.container_frame.pack_forget()

        self.top_frame = ctk.CTkFrame(master=self.container_frame, fg_color="red")
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        scrollwheel_title = ctk.CTkLabel(master=self.top_frame, text="Scrollwheel")
        scrollwheel_title.pack()

        self.middle_frame = ctk.CTkFrame(master=self.container_frame,
                                        #   fg_color="green"
                                        fg_color="transparent"
                                          )
        self.middle_frame.grid(row=1, column=0, sticky="nsew")

        self.right_frame = ctk.CTkFrame(master=self.container_frame,
                                        #  fg_color="blue"
                                        fg_color="transparent"
                                         )
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        self.container_frame.grid_columnconfigure(0, weight=0)  # Do not expand left_frame column
        self.container_frame.grid_columnconfigure(1, weight=1)  # Allow right_frame column to expand
        self.container_frame.grid_rowconfigure(1, weight=1)


        if configuration.smartshift_support == True:
            smartshift_options_label = ctk.CTkLabel(master=self.middle_frame, text=("SmartShift Options"), font=ctk.CTkFont( family="Roboto", size=18, ), )
            # smartshift_options_label.grid(row=3, column=0, padx=(10,0), pady=(30,0), sticky="w")
            smartshift_options_label.pack()

            smartshift_frame = ctk.CTkFrame(master=self.middle_frame, fg_color="transparent")
            # smartshift_frame.grid(row=4, column=0, sticky="ew")
            smartshift_frame.pack()
            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = Checkbox(master=smartshift_frame, text="SmartShift On", command=lambda: setattr(configuration, 'smartshift_on', check_var.get()), variable=check_var,)
            checkbox.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w", 
                        #   rowspan=2
                          )
            
            
            smartshift_threshold_label = ctk.CTkLabel(master=smartshift_frame, text=("Threshold"), font=ctk.CTkFont(family="Roboto", size=12, ),)
            smartshift_threshold_label.grid(row=1, column=0)

            smartshift_threshold_spinbox = IntSpinbox(master=smartshift_frame, db_query=configuration.update_smartshift_threshold, width=140, step_size=5, min_value=1, max_value=255, value=configuration.smartshift_threshold)            
            smartshift_threshold_spinbox.grid(row=2, column=0, sticky="w", padx=(0,10))

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
            smartshift_torque_label.grid(row=1, column=1)

            smartshift_torque_spinbox = IntSpinbox(master=smartshift_frame,
                                                   db_query=configuration.update_smartshift_torque,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    value=configuration.smartshift_torque
                                    )
            
            smartshift_torque_spinbox.set(configuration.smartshift_torque) #TODO: Update
            smartshift_torque_spinbox.grid(row=2, column=1)
            





        if configuration.hires_scroll_support == True:

            hiresscroll_options_label = ctk.CTkLabel(master=self.middle_frame, text=("HiRes Scroll Options"), font=ctk.CTkFont( family="Roboto", weight="bold", size=18,))
            hiresscroll_options_label.pack()

            def hiresscroll_hires_toggle():
                configuration.hiresscroll_hires = not(configuration.hiresscroll_hires)
            hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
            hirescroll_hires_checkbox = Checkbox(master=self.middle_frame, text=" HiRes Scroll On", command=hiresscroll_hires_toggle, variable=hiresscroll_hires_var)
            hirescroll_hires_checkbox.pack(anchor="w", padx=30, pady=(7, 7))

            def hiresscroll_invert_toggle():
                configuration.hiresscroll_invert = not(configuration.hiresscroll_invert)
            hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
            hirescroll_invert_checkbox = Checkbox(master=self.middle_frame, text=" Scroll Invert", command=hiresscroll_invert_toggle, variable=hiresscroll_invert_var)
            hirescroll_invert_checkbox.pack(anchor="w", padx=30, pady=(7, 7))


            def hiresscroll_target_toggle():
                configuration.hiresscroll_target = not(configuration.hiresscroll_target)
            hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
            hirescroll_target_checkbox = Checkbox(master=self.middle_frame, text=" Scroll target", command=hiresscroll_target_toggle, variable=hiresscroll_target_var)
            hirescroll_target_checkbox.pack(anchor="w", padx=30, pady=(7, 7))



        self.middle_buttons_frame = ctk.CTkFrame(master=self.middle_frame, 
                                               fg_color="transparent") #TODO UPDATE
        self.middle_buttons_frame.pack(side="left", fill="x", expand=True)
        self.frames = {}
        self.currently_selected_menu = None
        self.buttons_dict = {}


        def create_left_buttons(direction, text):
            self.buttons_dict[direction] = ctk.CTkButton(master=self.middle_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=text, font=ctk.CTkFont(family="Noto Sans",size=18 ), 
                                command=lambda b=direction: self.on_button_click(b),
                                #    command=lambda d=device.device_id: self.on_button_click(d),
                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            self.buttons_dict[direction].pack(fill="x", expand=True)

        for direction in self.configuration.scroll_directions.keys():
            create_left_buttons(direction=direction, text=f"Scroll {direction} Actions")
            self.frames[direction] = ScrollFrame(master=self.right_frame, root=root, scroll_settings=self.configuration.scroll_directions[direction])

        if self.configuration.touch is not None:
            create_left_buttons(direction="Touch",text=f"Thumbwheel Touch")
            self.frames["Touch"] = TouchTapProxyFrame(master=self.right_frame, root=root, ttt_object=self.configuration.touch)
        if self.configuration.tap is not None:
            create_left_buttons(direction="Tap",text=f"Thumbwheel Tap")
            self.frames["Tap"] = TouchTapProxyFrame(master=self.right_frame, root=root, ttt_object=self.configuration.tap)
        if self.configuration.proxy is not None:
            create_left_buttons(direction="Proxy",text=f"Thumbwheel Proxy")
            self.frames["Proxy"] = TouchTapProxyFrame(master=self.right_frame, root=root, ttt_object=self.configuration.proxy)



    def on_button_click(self, direction):
        if direction != self.currently_selected_menu:
            if self.currently_selected_menu is not None:
                self.buttons_dict[self.currently_selected_menu].configure(fg_color="transparent")
                self.frames[self.currently_selected_menu].pack_forget()
            self.frames[direction].pack(fill="both", expand=True)
            self.buttons_dict[direction].configure(fg_color="gray25")
            self.currently_selected_menu = direction











    #     def create_left_buttons(direction, text):
    #         self.buttons_dict[direction] = ctk.CTkButton(master=self.middle_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=text, font=ctk.CTkFont(family="Noto Sans",size=18 ), 
    #                             command=lambda b=direction: self.on_button_click(b),
    #                             #    command=lambda d=device.device_id: self.on_button_click(d),
    #                                  fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
    #         self.buttons_dict[direction].pack(fill="x", expand=True)
    #     def create_right_frames():
    #         self.frames["Up"] = ctk.CTkFrame(master=self.right_frame, fg_color="transparent")
    #         self.frames["Down"] = ctk.CTkFrame(master=self.right_frame, fg_color="transparent")





    #     create_right_frames()

    #     for direction in self.configuration.scroll_directions.keys():

    #         create_left_buttons(direction=direction, text=f"Scroll {direction} Actions")
    #         self.frames[direction] = ScrollFrame(master=self.right_frame, scroll_settings=self.configuration.scroll_directions[direction])


    # def on_button_click(self, direction):


    #     if self.currently_selected_menu is not None:
    #         self.buttons_dict[self.currently_selected_menu].configure(fg_color="transparent")
    #         self.frames[self.currently_selected_menu].pack_forget()
    #     self.frames[direction].pack(fill="both", expand=True)
    #     self.buttons_dict[direction].configure(fg_color="gray25")
    #     self.currently_selected_menu = direction




        # scrollwheel_up_threshold_label = ctk.CTkLabel(master=self.container_frame, text = "Scrollwheel Up Threshold")
        # scrollwheel_up_threshold_label.grid(row=0, column=0)
        # scrollwheel_down_threshold_label = ctk.CTkLabel(master= self.container_frame, text = "Scrollwheel Down Threshold")
        # scrollwheel_down_threshold_label.grid(row=0, column=2)

        # self.scrollwheel_up_spinbox = IntSpinbox(master=self.container_frame, width=200, step_size=5, min_value=1, max_value=9999)
        # self.scrollwheel_up_spinbox.set(scroll_properties.scroll_up_threshold)
        # self.scrollwheel_up_spinbox.grid(row=1, column=0)
        # self.scrollwheel_down_spinbox = IntSpinbox(master=self.container_frame, width=200, step_size=5, min_value=1, max_value=9999)
        # self.scrollwheel_down_spinbox.set(scroll_properties.scroll_down_threshold)
        # self.scrollwheel_down_spinbox.grid(row=1, column=2)


        # scrollwheel_up_mode_label = ctk.CTkLabel(master=self.container_frame, text = "Scrollwheel Up Mode")
        # scrollwheel_up_mode_label.grid(row=0,column=1)
        # scroll_up_mode_dropdown = ctk.CTkOptionMenu(master=self.container_frame, variable=ctk.StringVar(value=scroll_properties.scroll_up_mode), values=["OnInterval", "OnThreshold"], state="normal", width=200, height=36, command=lambda new_mode: setattr(scroll_properties, 'scroll_up_mode', new_mode))
        # scroll_up_mode_dropdown.grid(row=1, column=1)




        # scrollwheel_down_mode_label = ctk.CTkLabel(master=self.container_frame, text = "Scrollwheel Down Mode")
        # scrollwheel_down_mode_label.grid(row=0,column=3)
        # scroll_down_mode_dropdown = ctk.CTkOptionMenu(master=self.container_frame, variable=ctk.StringVar(value=scroll_properties.scroll_down_mode), values=["OnInterval", "OnThreshold"], state="normal", width=200, height=36, command=lambda new_mode: setattr(scroll_properties, 'scroll_down_mode', new_mode))
        # scroll_down_mode_dropdown.grid(row=1, column=3)






        

        # if configuration.hires_scroll_support == True:


        #     hiresscroll_options_label = ctk.CTkLabel(
        #                             master=self.container_frame,
        #                                                                 text=("HiRes Scroll Options"),
        #                                             font=ctk.CTkFont(
        #                                                     family="Roboto",
        #                                                         # weight="bold",
        #                                                     size=18,
        #                                                     ),
        #                                                     # text_color="#1F538D",
        #                                     # pady=30,
        #                                     # anchor='s'
        #     )
        #     hiresscroll_options_label.grid(row=3, column=1, padx=(10,0), pady=(30,0), sticky="w")


        #     hiresscroll_frame = ctk.CTkFrame(master=self.container_frame)
        #     hiresscroll_frame.grid(row=4, column=1, sticky="ew")


        #     def hiresscroll_hires_toggle():
        #         configuration.hiresscroll_hires = not(configuration.hiresscroll_hires)


        #     hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
        #     hirescroll_hires_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="HiRes Scroll On", command=hiresscroll_hires_toggle,
        #                                         variable=hiresscroll_hires_var, onvalue=True, offvalue=False)
        #     hirescroll_hires_checkbox.grid(row=0, column=0, rowspan=2)


        #     def hiresscroll_invert_toggle():
        #         configuration.hiresscroll_invert = not(configuration.hiresscroll_invert)


        #     hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
        #     hirescroll_invert_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll Invert", command=hiresscroll_invert_toggle,
        #                                         variable=hiresscroll_invert_var, onvalue=True, offvalue=False)
        #     hirescroll_invert_checkbox.grid(row=0, column=1, rowspan=2)


        #     def hiresscroll_target_toggle():
        #         configuration.hiresscroll_target = not(configuration.hiresscroll_target)

        #     hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
        #     hirescroll_target_checkbox = ctk.CTkCheckBox(master=hiresscroll_frame, text="Scroll target", command=hiresscroll_target_toggle,
        #                                         variable=hiresscroll_target_var, onvalue=True, offvalue=False)
        #     hirescroll_target_checkbox.grid(row=0, column=2, rowspan=2)











    def pack(self, *args, **kwargs):
        self.container_frame.pack(fill="both", expand=True, *args, **kwargs)

    def pack_forget(self, *args, **kwargs): 
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.container_frame.destroy(*args, **kwargs)
















def get_geometry_and_window_and_widget_scaling():
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'window_scaling'""")
    window_scaling = float(cursor.fetchone()[0])
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'widget_scaling'""")
    widget_scaling = float(cursor.fetchone()[0])
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'geometry'""")
    geometry = cursor.fetchone()[0]
    execute_db_queries.close_without_committing_changes(conn)
    return window_scaling, widget_scaling, geometry

# def update_window_geometry_in_db(new_geometry):
#     try:
#         conn, cursor = execute_db_queries.create_db_connection()
#         cursor.execute("""UPDATE UserSettings SET value = ? WHERE key = 'geometry' """, (f"{new_geometry.width}x{new_geometry.height}",))
#         execute_db_queries.commit_changes_and_close(conn)
#     except:




import argparse
import sys
import psutil
import os

class SystemMemory:
    @staticmethod
    def get_total_ram_mb():
        return f"{SystemMemory.get_total_ram() / 1024 ** 2:.2f} MB"

    @staticmethod
    def get_total_ram():
        mem = psutil.virtual_memory()
        return mem.total  # in bytes

    @staticmethod
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss  # in bytes

    @staticmethod
    def get_memory_usage_mb():
        return f"{SystemMemory.get_memory_usage() / 1024 ** 2:.2f} MB"

    @staticmethod
    def get_ram_in_use_mb():
        return f"{SystemMemory.get_ram_in_use() / 1024 ** 2:.2f} MB"

    @staticmethod
    def get_ram_in_use():
        mem = psutil.virtual_memory()
        return mem.used  # in bytes




def setup_gui(root, start_in_background=None, arg2=None):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    ctk.DrawEngine.preferred_drawing_method = "font_shapes"


    # def make_a_splash(self, text="LogiOpsGUI"):
    splash = NewDeviceSplash(root, text="LogiOpsGUI")
    splash.pack(fill="both", expand=True)


    front_page = FrontPage(root)

    front_page.show()

    return splash



def main(start_in_background=None, arg2=None):
    create_app_data.configure_logging() 
    create_app_data.initialise_database() 

    root = ctk.CTk()
    import tkinter as tk
    icon = tk.PhotoImage(file="/home/matthew/LogiOpsGui/images/icon.png")  # Convert .ico to .png if necessary
    root.iconphoto(True, icon)

    

    window_scaling, widget_scaling, geometry = get_geometry_and_window_and_widget_scaling()

    ctk.set_window_scaling(window_scaling)
    ctk.set_widget_scaling(widget_scaling)
    root.attributes('-alpha', 0.1)
    # root.geometry(geometry)
    root.resizable(True, True)
    root.title("LogiOpsGUI")

    def center_window():

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()

        x = (screen_width // 2) - window_width*2
        y = (screen_height // 2) - window_height - 100

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")


    root.overrideredirect(True)
    center_window()  # Center the window initially
    splash = setup_gui(root, start_in_background=start_in_background, arg2=arg2)  

    root.withdraw() 


    root.attributes('-alpha', 1.0)    
    root.after(600, root.deiconify)

    splash.destroy()
    root.overrideredirect(False)



    def center_window2():

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()

        x = (screen_width // 2) - window_width*2
        y = (screen_height // 2) - window_height*5
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    center_window2()  # Re-center the window after restoring the title bar
    
    root.geometry(geometry)

    root.mainloop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="LogiOpsGUI with command line arguments.")
    parser.add_argument("--start_in_background", type=str, help="TODO UPDATE")
    parser.add_argument("--arg2", type=str, help="TODO UPDATE")
    args = parser.parse_args()
    main(args.start_in_background, args.arg2)
