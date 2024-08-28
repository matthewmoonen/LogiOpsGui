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
import subprocess
import BackendData
from GraphicalControlElements import svg_to_image, MatthewsRadioButton, FloatSpinbox, IntSpinbox





class DeviceDropdown(ctk.CTkFrame):
    def __init__(self, master, front_page, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        self.master = master
        self.front_page = front_page
        self.add_device_button = ctk.CTkButton(master=self, height=44, width=180, state="disabled", text="Add Device", text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=("#28A745"), font=ctk.CTkFont(size=14, family="Noto Sans"))
        self.add_device_button.grid(row=0, column=1, padx=(0, 10))
        self.setup_option_menu()

    def setup_option_menu(self):
        # Create the new option menu first
        self.options = [i.device_name for i in self.front_page.device_data.non_user_devices.values()]
        self.selected_option_var = ctk.StringVar(value=' Select New Device')
        new_option_menu = DropdownMenu(master=self, variable=self.selected_option_var, values=self.options, width=350, height=44, command=self.device_dropdown_option_chosen)
        new_option_menu.grid(row=0, column=0, padx=(10, 10))

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

        self.edit_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", border_width=1, hover_color="#113A1B", corner_radius=0, text=" Edit", command=lambda c=self.config.configuration_id, d=self.config.device_id: self.edit_configuration(configuration_id=c, device_id=d))
        self.edit_configuration_button.grid(row=0, column=2, sticky="e")

        delete_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=0, command=lambda: self.configuration_deletion_warning())
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

        self.new_configuration_button = ctk.CTkButton(master=self.device_options_frame, text="Add Configuration", fg_color=gui_variables.standard_green1, corner_radius=0, height=55, width=250, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), command=lambda: self.add_new_configuration())
        self.new_configuration_button.grid(row=0, column=1, sticky="e")

        self.delete_device_button = ctk.CTkButton(master=self.device_options_frame, text="Delete Device", fg_color=gui_variables.standard_red4, corner_radius=0, hover_color=gui_variables.standard_red6,height=55, width=200, font=ctk.CTkFont(family="Helvetica Neue", size=16), command=lambda d=user_device.device_id: self.device_deletion_warning(d))
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

        # app_title_image = ctk.CTkImage(light_image=Image.open(os.path.join("images/logo.png")), size=(392, 132))
        app_title_image = ctk.CTkImage(light_image=Image.open(os.path.join("images/logo.png")), size=(392*1.15, 132*1.15))
        # app_title_image = ctk.CTkImage(light_image=Image.open(os.path.join("images/logo.png")), size=(470, 158))
        # app_title_image = ctk.CTkImage(light_image=Image.open(os.path.join("images/logo.png")), size=(490, 165))
        
        app_title = ctk.CTkLabel(master=left_frame, image=app_title_image, text='')
        app_title.pack(padx=(0, 7), pady=(40,40))

        def handle_file_selection(selected_path, selected_filename):
            self.cfg_location, self.cfg_filename = create_cfg.set_cfg_location(selected_path, selected_filename)
            self.show_cfg_location.configure(text=f"{self.cfg_location}/{self.cfg_filename}")

        def on_create_cfg_button_click():            
            cfg_message = create_cfg.generate_in_user_chosen_directory()
            CTkMessagebox(title="Error", message=cfg_message, option_1="OK", width=600, height=300, fade_in_duration=200)

        def update_restart_logid():
            create_cfg.generate_in_app_data()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bash_script = os.path.join(script_dir, 'restart_sctl.sh')
            result = subprocess.run(['sudo', '-n', 'bash', bash_script], capture_output=True, text=True)
            # TODO: create popup.
            print("Output:", result.stdout)
            print("Error:", result.stderr)
            print("Return Code:", result.returncode)

        ignored_devices_label = gui_variables.MainPageLabel1(master=left_frame, text="Ignored Devices",)
        cfg_file_label = ctk.CTkLabel(master=left_frame, text="Logid Configuration", font=ctk.CTkFont(family="Noto Sans", weight="bold", size=20),)
        self.cfg_location, self.cfg_filename = create_cfg.get_cfg_location()
        self.show_cfg_location = ctk.CTkLabel(master=left_frame, text=f"{self.cfg_location}/{self.cfg_filename}" if self.cfg_location != "default" else "etc/logid.cfg")
        create_cfg_button = ctk.CTkButton(master=left_frame, text="Create CFG", command=on_create_cfg_button_click)
        set_logid_path_button = ctk.CTkButton(master=left_frame,text="Edit CFG Location",command=lambda: FileBrowserWindow.BrowserWindow(self, permitted_formats="cfg", current_path=self.cfg_location, current_filename=self.cfg_filename, on_select=handle_file_selection))
        restart_logid_button = ctk.CTkButton(master=left_frame, text="Apply Changes and Restart Logid", command=update_restart_logid)

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
        super().__init__(master, fg_color="#191919", corner_radius=0)

        self.master = master
        self.configuration = configuration
        self.main_page_radio_button = radio_button
        self.add_action_frame = add_action_frame
        self.front_page = front_page

        """Create the page's frames. Add title to page."""
        self.frame01 = ctk.CTkFrame(master=self, fg_color="#292929")
        self.frame01.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)  # Set the weight of the row in the main frame

        self.frame02 = ctk.CTkFrame(master=self, fg_color="#292929")
        self.frame02.grid(row=1, column=1, sticky="nsew", rowspan=1)
        
        self.frame02a = ctk.CTkFrame(master=self.frame02, fg_color="#242424")
        self.frame02a.grid(row=0, column=0, pady=(100,0) if configuration.has_thumbwheel != True else (60,0))

        self.frame03 = ctk.CTkFrame(master=self, fg_color="#191919")
        self.frame03.grid(row=0, column=2, sticky="nsew", rowspan=2)
        self.grid_columnconfigure(2, weight=2)  

        self.frame00 = ctk.CTkFrame(master=self, fg_color="#343434", corner_radius=0, height=20)
        self.frame00.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10)

        # device_name_label = ctk.CTkLabel(master=self.frame00, text=configuration.device_name, font=ctk.CTkFont( family="Noto Sans", size=30 if len(configuration.device_name) < 15 else 20, ), text_color=gui_variables.primary_colour, pady=(20), corner_radius=0 )
        device_name_label = ctk.CTkLabel(master=self.frame00, text=configuration.device_name, font=ctk.CTkFont( family="Noto Sans", size=30 if len(configuration.device_name) < 15 else 28, ), text_color=gui_variables.primary_colour, pady=(12), corner_radius=0 )

        device_name_label.pack()

        back_button = ctk.CTkButton(master=self.frame01, text="Back",command=lambda: [self.go_back(),update_spinboxes_in_db(), update_config_file_name()], 
                                    border_width=0,
                                    fg_color="#8847C4", hover_color="#A579CD",

                                    # hover_color="#B69BD4",
                                    text_color="#272727",
                                    width=220,
                                    height=50,
                                    font=ctk.CTkFont(size=20)
                                    )
        # back_button.grid(row=2, column=0)
        back_button.pack(pady=(30,20))

        self.left_buttons_dictionary = {}
        self.currently_selected_menu = None

        self.frames = {}

        device_buttons_label = gui_variables.MainPageLabel2(master=self.frame02a, text="Device Buttons", text_color="#0091EA")
        device_buttons_label.pack(padx=(0,0), pady=(10,0))

        def create_button_left_buttons(button_text, button_reference):
            created_button = ctk.CTkButton(master=self.frame02a, corner_radius=0, height=40, border_spacing=7, text=button_text, font=ctk.CTkFont(family="Noto Sans",size=16 if configuration.has_thumbwheel==True else 18), command=lambda c=button_reference: self.show_button_config_frame(c), fg_color="transparent", text_color="gray63", hover_color= "gray30", anchor="w")
            created_button.pack(fill="x",pady=0 if configuration.has_thumbwheel==True else 2)
            self.left_buttons_dictionary[button_reference] = created_button

        for button in self.configuration.buttons.values():
            create_button_left_buttons(button_text=button.button_name, button_reference=button.button_id)



        def create_ttp_buttons(direction, text):
            self.left_buttons_dictionary[direction] = ctk.CTkButton(master=self.frame02a, corner_radius=0, height=40, border_spacing=7, text=text, font=ctk.CTkFont(family="Noto Sans",size=16 if configuration.has_thumbwheel==True else 18), command=lambda b=direction: self.ttp_button_clicked(b), fg_color="transparent", text_color="gray63", hover_color="gray30", anchor="w")
            self.left_buttons_dictionary[direction].pack(fill="x", pady=0 if configuration.has_thumbwheel==True else 2)

        def create_scroll_buttons(direction):
            self.left_buttons_dictionary[direction] = ctk.CTkButton(master=self.frame02a, corner_radius=0, height=40, border_spacing=7, text=f"Scroll {direction}", font=ctk.CTkFont(family="Noto Sans",size=16 if configuration.has_thumbwheel==True else 18), command=lambda b=direction: self.scroll_button_clicked(b), fg_color="transparent", text_color="gray63", hover_color="gray30", anchor="w")

            self.left_buttons_dictionary[direction].pack(fill="x", pady=0 if configuration.has_thumbwheel==True else 2)
            
        scrollwheels_label_text = "Scrollwheel"
        if configuration.has_scrollwheel == True and configuration.has_thumbwheel == True:
            scrollwheels_label_text = "Vertical Scrollwheel"
        if configuration.has_scrollwheel == True or configuration.has_thumbwheel == True: 
            scrollwheel_label = gui_variables.MainPageLabel2(master=self.frame02a, text=scrollwheels_label_text, text_color="#0091EA")
            scrollwheel_label.pack(padx=(0,0), pady=(10,0))
            create_scroll_buttons("Up")
            create_scroll_buttons("Down")

            if self.configuration.has_thumbwheel == True:
                thumbwheel_label = gui_variables.MainPageLabel2(master=self.frame02a, text="Thumbwheel", text_color="#0091EA")
                thumbwheel_label.pack(padx=(0,0), pady=(10,0))

                create_scroll_buttons("Left")
                create_scroll_buttons("Right")
                if self.configuration.touch is not None:
                    create_ttp_buttons(direction="Touch",text=f"Thumbwheel Touch")
                if self.configuration.tap is not None:
                    create_ttp_buttons(direction="Tap",text=f"Thumbwheel Tap")
                if self.configuration.proxy is not None:
                    create_ttp_buttons(direction="Proxy",text=f"Thumbwheel Proxy")

        def focus_next_widget(event):

            # Make TAB key push focus to next widget rather than inserting tabs
            current_widget = event.widget
            next_widget = current_widget.tk_focusNext() 
            
            if next_widget:
                self.master.focus_set()
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
                self.main_page_radio_button.update_text(config_name_stripped)

        configuration_name_label = gui_variables.EditPageLabel1(master=self.frame01,text="Configuration Name")
        configuration_name_label.pack(pady=(40,0) if configuration.smartshift_support==False and configuration.thumbwheel_touch_support == False else (20, 0) if configuration.smartshift_support==True and configuration.thumbwheel_touch_support == False else 0)

        configuration_name_textbox = ctk.CTkTextbox(master=self.frame01, height=45, width=350,
                                                    activate_scrollbars=False,
                                                    fg_color="#343638",
                                                    text_color="gray70",
                                                     font=ctk.CTkFont(     family="Noto Sans",          size=15 ), corner_radius=1, 
                                                     
                                                     )

        configuration_name_textbox.pack(padx=12)
        configuration_name_textbox.tag_config("center", justify="center")
        configuration_name_textbox.insert("end", configuration.configuration_name, "center")

        configuration_name_textbox.bind("<Tab>", focus_next_widget)
        configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)

        dpi_label = gui_variables.EditPageLabel1(master=self.frame01, text=("DPI"),)
        dpi_label.pack(pady=(15,0))    
        dpi_spinbox = IntSpinbox(master=self.frame01, width=200, height=30, db_query=self.configuration.update_dpi, step_size=50, min_value=configuration.min_dpi, max_value=configuration.max_dpi, value=configuration.dpi, )
        dpi_spinbox.pack()
        dpi_spinbox.bind("<Tab>", focus_next_widget)

        if configuration.smartshift_support == True:
            smartshift_options_label = gui_variables.EditPageLabel1(master=self.frame01, text=("SmartShift"))
            smartshift_options_label.pack(pady=(10,0))

            smartshift_frame = ctk.CTkFrame(master=self.frame01, fg_color="#212121", corner_radius=0)
            smartshift_frame.pack(fill="x", padx=15)

            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = Checkbox(master=smartshift_frame, text="SmartShift On", command=lambda: setattr(configuration, 'smartshift_on', check_var.get()), variable=check_var,)
            if configuration.has_thumbwheel == True:
                checkbox.pack(pady=(20,0))
            else:
                checkbox.pack(pady=(25,0))
            

            spinbox_frame = ctk.CTkFrame(master=smartshift_frame, fg_color="transparent", corner_radius=0)
            spinbox_frame.pack(padx=0, pady=0)

            smartshift_threshold_label = ctk.CTkLabel(master=spinbox_frame, text=("Threshold"), font=ctk.CTkFont(family="Roboto",size=15,), text_color="gray70",)
            smartshift_threshold_spinbox = IntSpinbox(master=spinbox_frame, db_query=configuration.update_smartshift_threshold, width=150, height=29, step_size=5, min_value=1, max_value=255, value=configuration.smartshift_threshold)            
            smartshift_torque_label = ctk.CTkLabel(master=spinbox_frame, text=("Torque"), font=ctk.CTkFont(family="Roboto",size=15,), text_color="gray70",)

            smartshift_torque_spinbox = IntSpinbox(master=spinbox_frame, db_query=configuration.update_smartshift_torque, width=150, height=29, step_size=5, min_value=1, max_value=255, value=configuration.smartshift_torque )
            smartshift_torque_spinbox.set(configuration.smartshift_torque) #TODO: Update
            
            if configuration.has_thumbwheel == True:
                smartshift_threshold_label.grid(column=0, row=0, pady=(15,0))
                smartshift_threshold_spinbox.grid(column=0, row=1, padx=(0, 7), pady=(0,10))
                smartshift_torque_label.grid(column=1, row=0, pady=(15,0))
                smartshift_torque_spinbox.grid(column=1, row=1, padx=(7,0), pady=(0,10))
            else:
                smartshift_threshold_label.grid(column=0, row=0, pady=(15,0))
                smartshift_threshold_spinbox.grid(column=0, row=1, pady=(5, 0))
                smartshift_torque_label.grid(column=0, row=2, pady=(15,0))
                smartshift_torque_spinbox.grid(column=0, row=3, pady=(0, 20))
                

            smartshift_torque_spinbox.bind("<Tab>", focus_next_widget)
            smartshift_threshold_spinbox.bind("<Tab>", focus_next_widget)

        if configuration.hires_scroll_support == True:

            hiresscroll_options_label = gui_variables.EditPageLabel1(master=self.frame01, text=("HiRes Scroll"),)
            hiresscroll_options_label.pack(pady=(10,0))

            hiresscroll_frame = ctk.CTkFrame(master=self.frame01, fg_color="#212121", corner_radius=0)
            hiresscroll_frame.pack(
                fill="x",

                  padx=15)

            def hiresscroll_hires_toggle():
                configuration.hiresscroll_hires = not(configuration.hiresscroll_hires)
            hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
            hirescroll_hires_checkbox = Checkbox(master=hiresscroll_frame, text=" HiRes Scroll On", command=hiresscroll_hires_toggle, variable=hiresscroll_hires_var)
            hirescroll_hires_checkbox.pack(anchor="w", padx=30, pady=(20,16))

            def hiresscroll_invert_toggle():
                configuration.hiresscroll_invert = not(configuration.hiresscroll_invert)
            hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
            hirescroll_invert_checkbox = Checkbox(master=hiresscroll_frame, text=" Scroll Invert", command=hiresscroll_invert_toggle, variable=hiresscroll_invert_var)
            hirescroll_invert_checkbox.pack(anchor="w", padx=30, )

            def hiresscroll_target_toggle():
                configuration.hiresscroll_target = not(configuration.hiresscroll_target)
            hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
            hirescroll_target_checkbox = Checkbox(master=hiresscroll_frame, text=" Scroll target", command=hiresscroll_target_toggle, variable=hiresscroll_target_var)
            hirescroll_target_checkbox.pack(anchor="w", padx=30, pady=(20,16))

        if configuration.has_thumbwheel == True:

            thumbwheel_options_label = gui_variables.EditPageLabel1(master=self.frame01, text=("Thumbwheel"))
            thumbwheel_options_label.pack(pady=(10,0))

            thumbwheel_frame = ctk.CTkFrame(master=self.frame01, fg_color="#212121", corner_radius=0)
            thumbwheel_frame.pack(fill="x", 
                                #   expand=True,
                                    padx=15)

            thumbwheel_divert_var = ctk.BooleanVar(value=configuration.thumbwheel_divert)
            thumbwheel_divert_checkbox = Checkbox(master=thumbwheel_frame, text=" Thumbwheel Divert", command=lambda configuration=configuration: self.thumbwheel_divert_event(configuration), variable=thumbwheel_divert_var)
            thumbwheel_divert_checkbox.pack(anchor="w", padx=30, pady=(20,16))
            
            thumbwheel_invert_var = ctk.BooleanVar(value=configuration.thumbwheel_invert)
            thumbwheel_invert_checkbox = Checkbox(master=thumbwheel_frame, text=" Thumbwheel Invert", command=lambda configuration=configuration: self.thumbwheel_invert_event(configuration), variable=thumbwheel_invert_var)
            thumbwheel_invert_checkbox.pack(anchor="w", padx=30, pady=(0, 20))


        def update_config_file_name():
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            if len(config_name_stripped) > 0:
                configuration.configuration_name = config_name_stripped
                self.main_page_radio_button.update_text(config_name_stripped)

        def update_spinboxes_in_db():
            configuration.dpi = dpi_spinbox.get()

    def thumbwheel_divert_event(self, configuration):
        configuration.thumbwheel_divert = not(configuration.thumbwheel_divert)

    def thumbwheel_invert_event(self, configuration):
        configuration.thumbwheel_invert = not(configuration.thumbwheel_invert)

    def create_ttp_frame(self, menu):
        if menu == "Touch":
            ttp_object=self.configuration.touch
        elif menu == "Tap":
            ttp_object=self.configuration.tap
        else:
            ttp_object= self.configuration.proxy
        self.frames[menu] = TouchTapProxyFrame(master=self.frame03, root=self.master, ecf=self, ttp_object=ttp_object)

    def ttp_button_clicked(self, menu):
        if menu not in self.frames.keys():
            print("creating ttp frame now")
            self.create_ttp_frame(menu)
        self.left_button_clicked(clicked_menu_item=menu)

    def scroll_button_clicked(self, direction):
        if direction not in self.frames.keys():
            print("creating scroll frame now")
            self.create_scroll_frame(direction)
        self.left_button_clicked(clicked_menu_item=direction)

    def create_scroll_frame(self, direction):
        self.frames[direction] = ScrollFrame(master=self.frame03, root=self.master, ecf=self, scroll_settings=self.configuration.scroll_directions[direction])

    def show_button_config_frame(self, button_reference):
        if button_reference not in self.frames.keys():
            print("creating now")
            self.create_button_config_frame(button_reference)
        self.left_button_clicked(clicked_menu_item=button_reference)

    def create_button_config_frame(self, button_reference):        
        self.frames[button_reference] = ButtonConfigFrame(master=self.frame03, ecf=self, button_settings_object=self.configuration.buttons[button_reference], root=self.master)

    def left_button_clicked(self, clicked_menu_item):
        if clicked_menu_item != self.currently_selected_menu:
            if self.currently_selected_menu is not None:
                self.left_buttons_dictionary[self.currently_selected_menu].configure(fg_color = "transparent")
            self.activate_left_button(menu_to_activate=clicked_menu_item)


    def activate_left_button(self, menu_to_activate):

        try:
            self.frames[menu_to_activate].pack(fill="both", expand=True)
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
        self.master.focus_set()
        self.pack_forget()
        self.front_page.show()

    def show(self):
        self.pack(fill="both", expand=True)

    def on_mousewheel_linux(self, event):
        
        if event.num == 4:
            self.frame03._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.frame03._parent_canvas.yview_scroll(1, "units")

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
    def __init__(self, master, settings_object, action_selection_frame, go_back, bottom_button_frame, root):
        super().__init__(master, fg_color="#292929",)
        self.root=root
        self.settings_object = settings_object
        self.action_selection_frame=action_selection_frame
        self.go_back=go_back

        self.bottom_frame = ctk.CTkFrame(master=bottom_button_frame, fg_color=test_colour5, corner_radius=0, height=50)

        # self.keypress_button_frame = ctk.CTkFrame(master=self, fg_color="transparent", height=60)
        # self.keypress_button_frame.pack()
        # self.keypress_button_frame.pack_propagate(False)


        self.click_box = ctk.CTkButton(master=self, border_spacing=80, corner_radius=0)

        self.initialise_clickbox()
        self.click_box.pack(
            pady=50, padx=50,
              fill="both", expand=True)
        self.root.wm_attributes('-type', 'dialog')

    def initialise_clickbox(self):
        self.click_box.configure(text="\nCLICK HERE \n to record keyboard shortcut\n                                                                                    ",
                                       command=self.activate_key_listener,
                                       fg_color="transparent",
                                       hover=True,
                                       border_width=10,
                                       border_color="#404040",
                                       font=ctk.CTkFont(size=24, family="Veranda"),
                                       border_spacing=80,
                                       text_color="gray50",
                                       hover_color="#313131"
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
        self.stop_recording_button = ctk.CTkButton(self.bottom_frame, text="Stop Recording",
                                                   
                                            command=self.deactivate_key_listener,
                                            height=50,
                                            width=250,
                                            fg_color="#8847C4", hover_color="#A579CD",
                                            #   text_color="black",
                                              text_color="gray80",

                                            font=ctk.CTkFont(family="Roboto", size=16)
                                            )
        self.stop_recording_button.pack(side="bottom", anchor="e")

        self.click_box.configure(
            hover=False,
            border_spacing=107 ,
                                  text="                                                                              \nStart typing...\n", command=None, border_color="#198754",)
        self.click_box.focus_set()



    def stop_listening(self):
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")

    def deactivate_key_listener(self):
        self.stop_listening()

        if not hasattr(self, "db_keypress_array"):
            self.initialise_clickbox()
        elif hasattr(self, "reset_button") and bool(self.reset_button.winfo_exists()):
            pass
        else:
            self.click_box.configure(border_color="#8847C4")
            self.save_button = ctk.CTkButton(master=self.bottom_frame, 
                                             
                                             
                                             
                                             text="Save new shortcut", command=self.save_button_clicked, corner_radius=0,
                                             height=50, width=250,
                                            fg_color=gui_variables.standard_green1, hover_color=gui_variables.standard_green3,
                                             font=ctk.CTkFont(family="Roboto", size=16), 
                                            #  text_color="black"
                                             )
            self.save_button.pack(side="right")
            self.reset_button = ctk.CTkButton(master=self.bottom_frame, text="Reset", height=50, width=130, command=self.initialise_clickbox, fg_color=gui_variables.standard_red4, corner_radius=0, hover_color=gui_variables.standard_red6,
                                              font=ctk.CTkFont(family="Roboto", size=15),
                                              text_color="gray85"
                                              )
            self.reset_button.pack(side="left", padx=(0,40))
        self.stop_recording_button.destroy()

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




# class KeyPressFrame(ctk.CTkFrame):
#     def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
#         super().__init__(master, **kwargs)

#         self.configure(fg_color="transparent")

#         self.app_root = app_root
#         self.origin_frame = origin_frame
#         self.settings_object = settings_object
#         self.go_back_function = go_back_function
#         self.added_from = added_from

    

#         self.click_box = ctk.CTkButton(master=self, border_spacing=80)

#         self.initialise_clickbox()
#         self.click_box.pack(pady=50, padx=50, fill="both", expand=True)
#         self.app_root.wm_attributes('-type', 'dialog')

#         self.enter_manually_button = ctk.CTkButton(master=self, text="Enter Array Manually", command=self.enter_manually)
#         # self.enter_manually_button.pack()


#     def enter_manually(self):
        
            
#         asdf = KeypressManual(master=self, db_keypress_array=self.db_keypress_array if hasattr(self, "db_keypress_array") else [], click_box=self.click_box)




#     def initialise_clickbox(self):
#         self.click_box.configure(text="\nCLICK HERE \n to enter keyboard shortcut\n                                                                                    ",
#                                        command=self.activate_key_listener,
#                                        fg_color="transparent",
#                                        hover=False,
#                                        border_width=10,
#                                        border_color="#363636",
#                                        font=ctk.CTkFont(size=14, family="Veranda"),
#                                        border_spacing=80
#                                        )
#         if hasattr(self, "reset_button"):
#             self.reset_button.destroy()
#             self.save_button.destroy()
#         if hasattr(self, "db_keypress_array"):
#             del self.db_keypress_array
#             del self.gui_keypress_array

#     def activate_key_listener(self):
#         self.app_root.bind("<KeyPress>", self.handle_key_press)
#         self.app_root.bind("<KeyRelease>", self.handle_key_release)
#         self.stop_recording_button = ctk.CTkButton(self, text="Click here to stop recording",
#                                             command=self.deactivate_key_listener,
#                                             height=50,
#                                             corner_radius=0,
                                            
#                                             )
#         self.stop_recording_button.pack()
#         self.click_box.configure(border_spacing=97 , text="                                                                              \nStart typing...\n", command=None, border_color="#198754",)
#         self.click_box.focus_set()



#     def stop_listening(self):
#         self.app_root.unbind("<KeyPress>")
#         self.app_root.unbind("<KeyRelease>")

#     def deactivate_key_listener(self):
#         self.stop_listening()
#         self.stop_recording_button.destroy()

#         if not hasattr(self, "db_keypress_array"):
#             self.initialise_clickbox()
#         elif hasattr(self, "reset_button") and bool(self.reset_button.winfo_exists()):
#             pass
#         else:
#             self.click_box.configure(border_color="#DC3545")
#             self.reset_button = ctk.CTkButton(self, text="Reset", command=self.initialise_clickbox)
#             self.reset_button.pack()
#             self.save_button = ctk.CTkButton(self, text="Save new keypress shortcut", command=self.save_button_clicked)
#             self.save_button.pack()

#     def save_button_clicked(self):
#         new_primary_key = self.settings_object.add_new_keypress_action(keypresses=json.dumps(self.db_keypress_array))

#         if not isinstance(self.added_from, GestureRadioFrame):
#             self.origin_frame.create_keypress_radio_button_row(i=new_primary_key)
#             self.origin_frame.keypress_radio_buttons_frame.grid(row=3, column=0)
#         else:
#             self.added_from.create_keypress_radio_button_row(i=new_primary_key)
#             self.added_from.keypress_radio_buttons_frame.grid(row=3, column=0)

#         self.go_back_function()

#     def pack_forget(self, *args, **kwargs):
#         if hasattr(self, 'stop_recording_button'):
#             self.deactivate_key_listener()
#         else:
#             print("no button")
#         super().pack_forget(*args, **kwargs)

#     def handle_key_press(self, event):

#         db_keymate, gui_keymate = keymates.get_keymates(event.keysym)
#         if not hasattr(self, "db_keypress_array"):
#             self.db_keypress_array = [db_keymate]            
#             self.gui_keypress_array = [gui_keymate]
#             self.click_box.configure(text=f"                                                                              \n{gui_keymate}\n")
            
#         # elif db_keymate not in self.db_keypress_array:
#         else:
#             self.click_box.configure(text=f"{self.click_box._text[:-1]} {gui_keymate}\n")
#             self.db_keypress_array.append(db_keymate)
#             self.gui_keypress_array.append(gui_keymate)
#         if event.keysym == "Super_L":
#             self.app_root.after(150, lambda: self.app_root.focus_force())  # Try to force focus back after a short delay
#         return "break"


#     def handle_key_release(self, event):
#         if event.keysym == "Super_L":
#             self.app_root.after(150, lambda: self.app_root.focus_force())  # Try to force focus back after key is released



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





class AddCycleDPI(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, bottom_button_frame, go_back):
        super().__init__(master, fg_color="#292929")
        self.settings_object = settings_object
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back

        self.bottom_frame = ctk.CTkFrame(master=bottom_button_frame, fg_color=test_colour5, corner_radius=0)

        


        label_spinbox_container = ctk.CTkFrame(master=self, fg_color="transparent", )
        label_spinbox_container.pack(padx=(100,100), pady=(60,0), fill="x")
        # label_spinbox_frame = ctk.CTkFrame(master=label_spinbox_container, fg_color="transparent", )
        # label_spinbox_frame.pack(side="left", anchor="w")
        
        self.hidden_frame=ctk.CTkFrame(master=label_spinbox_container, fg_color="transparent", height=4)

        label=ctk.CTkLabel(master=label_spinbox_container, text="DPI Value", font=ctk.CTkFont(family="Roboto", size=16,))
        # label.pack(pady=(0,5))
        label.grid(column=0, row=0, sticky="ew")
        label_spinbox_container.grid_columnconfigure(1, weight=2)

        self.spinbox = IntSpinbox(master=label_spinbox_container, height=36, value=1000, width=200, step_size=100, min_value=self.settings_object.config_object.min_dpi, max_value=self.settings_object.config_object.max_dpi )
        # self.spinbox.pack()            
        self.spinbox.grid(column=0, row=1)

        self.add_to_array_button = ctk.CTkButton(master=label_spinbox_container, height=50, width=250, text="Add value to array", command=self.add_value_to_array, corner_radius=0,
                                            


                                                fg_color="transparent",
                                                hover_color="#252525",
                                                text_color="#0089EB",
                                                border_color="#0089EB",
                                                border_width=3,


                                                #  fg_color=gui_variables.standard_green1,
                                                #    text_color_disabled=("#9FA5AB"),
                                                #    text_color_disabled=("red"),

                                                     font=ctk.CTkFont( size=15, family="Roboto"))
        # self.add_to_array_button.pack(side="right", anchor="se",)
        self.add_to_array_button.grid(row=0, column=1, rowspan=2, sticky="se")

        self.save_button = ctk.CTkButton(master=self.bottom_frame, height=50, width=250, text="Save CycleDPI Array", state="disabled", command=self.save_button_clicked, text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=gui_variables.standard_green3, font=ctk.CTkFont( size=14, family="Roboto"))
        self.save_button.pack()

        self.array_frame_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.array_frame_container.pack(
            # side="bottom",
              anchor="s", pady=113)

        array_left_bracket = ctk.CTkLabel(master=self.array_frame_container,text="dpis = [", font=ctk.CTkFont(size=28), text_color="gray50")
        array_right_bracket = ctk.CTkLabel(master=self.array_frame_container, text="]",font=ctk.CTkFont(size=28), text_color="gray50")

        array_left_bracket.pack(side="left", anchor="center",padx=(0, 10))
        array_right_bracket.pack(side="right",anchor="center",)

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

            self.hidden_frame.grid(column=0, row=2)
        if len(self.array_dict) == 1:
            self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1,)


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
            self.save_button.configure(state="disabled", fg_color=gui_variables.secondary_colour)
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



# ///
class AddAxisFrame(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, bottom_button_frame, go_back):
        super().__init__(master, fg_color="#292929")
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back
        self.settings_object = settings_object

        self.bottom_frame = ctk.CTkFrame(master=bottom_button_frame, fg_color=test_colour5, corner_radius=0)

        rel_list = [
            "REL_WHEEL (Scroll Up/Down)", "REL_WHEEL_HI_RES (Hi-res Scroll Up/Down)",
            "REL_HWHEEL (Scroll Left/Right)", "REL_HWHEEL_HI_RES (Hi-res Scroll Left/Right)",
            "REL_X (x-axis Movement)", "REL_Y (y-axis Movement)", "REL_Z (z-axis Movement)",
            "REL_RX (Rotational x-axis Movement)", "REL_RY (Rotational y-axis Movement)",
            "REL_RZ (Rotational z-axis Movement)", "REL_DIAL (Dial Movement)",
            "REL_MISC (Miscellaneous Relative Movement)", "REL_RESERVED (Typically Unused)",
            "REL_MAX (Maximum Relative Axis Value.)", "REL_CNT (Total Relative Axes Count)"
        ]

        axis_dropdown_variable = ctk.StringVar(value=" Select Axis")
        axis_dropdown = DropdownMenu(
            master=self,
            variable=axis_dropdown_variable,
            values=rel_list,
            width=400,
            height=40,
            command=self.enable_save_button
        )
        axis_dropdown.pack(side="top", anchor="n", padx=100, pady=(100, 334))

        multiplier_label=ctk.CTkLabel(master=self, text="Axis Multiplier")
        multiplier_label.pack()
        multiplier_floatspinbox = FloatSpinbox(
            master=self,
            value=1,
            width=200,
            step_size=0.1,
            min_value=-9999,
            max_value=9999
        )
        multiplier_floatspinbox.pack()

        self.save_button = ctk.CTkButton(
            master=self.bottom_frame,
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
        self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)

    def save_button_clicked(self, axis_button, axis_multiplier):
        new_axis_object = self.settings_object.add_new_axis_action(axis_button,axis_multiplier)
        new_button = self.action_selection_frame.create_axis_button(new_axis_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()
        
        self.go_back()












class AddChangeHost(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, go_back, bottom_button_frame):
        super().__init__(master, fg_color="#292929")
        self.settings_object=settings_object
        self.action_selection_frame=action_selection_frame
        self.go_back=go_back

        self.bottom_frame = ctk.CTkFrame(master=bottom_button_frame, fg_color=test_colour5, corner_radius=0)

        label_menu_frame = ctk.CTkFrame(master=self, fg_color="transparent", )
        label_menu_frame.pack(anchor="w", padx=100, pady=(80,307))

        label=ctk.CTkLabel(master=label_menu_frame, text="Host to Toggle", font=ctk.CTkFont(family="Roboto", size=16))
        label.pack(pady=(0, 15), anchor="w")

        def enable_save_button(x):
            self.save_button.configure(state="normal", fg_color=gui_variables.standard_green1)
            

        self.menu_var = ctk.StringVar(value=" Select Host")
        self.menu = DropdownMenu(master=label_menu_frame,
                                 variable=self.menu_var,
                                 values=["1", "2", "3", "Previous", "Next"],
                                 width=350,
                                 height=40,
                                 command=enable_save_button
                                 )
        self.menu.pack()
            
        self.save_button = ctk.CTkButton(master=self.bottom_frame, width=250, height=50, text="Add New ChangeHost", state="disabled", text_color="white", command=lambda: self.save_button_clicked(), text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=gui_variables.standard_green3, font=ctk.CTkFont( size=14, family="Roboto"))
        self.save_button.pack(side="bottom",)

    def save_button_clicked(self):
        chosen_option = self.menu_var.get()
        host_change = "prev" if chosen_option == "Previous" else "next" if chosen_option=="Next" else chosen_option
        new_changehost_object = self.settings_object.add_new_changehost_action(host_change=host_change)

        new_button = self.action_selection_frame.create_changehost_button(new_changehost_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()



class AddChangeDPI(ctk.CTkFrame):
    def __init__(self, master, settings_object, action_selection_frame, bottom_button_frame, go_back):
        super().__init__(master, fg_color="#292929")
        self.settings_object = settings_object
        self.action_selection_frame = action_selection_frame
        self.go_back = go_back

        self.bottom_frame = ctk.CTkFrame(master=bottom_button_frame, fg_color=test_colour5, corner_radius=0)
        

        label=ctk.CTkLabel(master=self, text="DPI Change", font=ctk.CTkFont(size=26))
        label.pack(anchor="center", pady=(80,0))

        spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=340,
                                height=45,
                                step_size=100,
                                min_value=-settings_object.config_object.max_dpi,
                                max_value=settings_object.config_object.max_dpi
                                )
        spinbox.pack(pady=(0,276))            

        save_button = ctk.CTkButton(master=self.bottom_frame, text="Save ChangeDPI", command=lambda: self.save_button_clicked(spinbox.get()), text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.standard_green1, font=ctk.CTkFont( size=14, family="Veranda"))
        save_button.pack()

    def save_button_clicked(self, dpi_change):      
        new_changedpi_object = self.settings_object.add_new_changedpi_action(dpi_change)
        
        new_button = self.action_selection_frame.create_changedpi_button(new_changedpi_object)
        new_button.pack(side="bottom")
        new_button.radio_button_clicked()

        self.go_back()


# test_colour1="green"
test_colour1="transparent"
# test_colour2 = "blue"
test_colour2 = "transparent"
# test_colour3 = "yellow"
test_colour3 = "transparent"
# test_colour4 = test_colour5
test_colour4 = "transparent"
# test_colour5 = "red"
test_colour5 = "transparent"

class NewActionFrame(ctk.CTkFrame):
    def __init__(self, master, root, ecf, origin_frame, action_selection_frame, settings_object):
        super().__init__(master, corner_radius=0, fg_color=test_colour1)

        self.origin_frame=origin_frame        

        if isinstance(settings_object, BackendData.ButtonSettings1):
            title_text=f"New {settings_object.button_name} Action" if settings_object.button_name[-6:] == "Button" else f"New {settings_object.button_name} Button Action"
        elif isinstance(settings_object, BackendData.GestureSettings1):
            title_text=f"New Gesture {settings_object.direction} Action ({settings_object.button.button_name})" if settings_object.button.button_name[-6:] == "Button" else f"New Gesture {settings_object.direction} Button Action ({settings_object.button.button_name})"
        elif isinstance(settings_object, BackendData.ScrollProperties):
            title_text=f"New Scroll {settings_object.scroll_direction} Action"
            settings_object = settings_object.actions
        elif isinstance(settings_object, BackendData.TouchTapProxy):
            title_text=f"New {settings_object.ttp} Action"
        else:
            title_text=f"New Action"

        title=ctk.CTkLabel(master=self, text=title_text, font=ctk.CTkFont(size=28, family="Roboto"), text_color="gray70")
        title.pack(pady=(0,65))

        ecf.add_action_frame=self

        dark_colour = "#181818"
        segment_button_colour = "#0091EA"

        options_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        control_frame = ctk.CTkFrame(master=self, fg_color=test_colour2, corner_radius=0)
        bottom_button_frame = ctk.CTkFrame(master=control_frame, fg_color=test_colour3, corner_radius=0)
        cancel_button_frame = ctk.CTkFrame(master=control_frame, fg_color=test_colour4, corner_radius=0)

        options = {}
        options["Keypress"] = AddKeypressFrame(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, bottom_button_frame=bottom_button_frame, root=root)
        options["Axis"] = AddAxisFrame(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, bottom_button_frame=bottom_button_frame)
        options["CycleDPI"] = AddCycleDPI(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, bottom_button_frame=bottom_button_frame)
        options["ChangeHost"] = AddChangeHost(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, bottom_button_frame=bottom_button_frame)
        options["ChangeDPI"] = AddChangeDPI(master=options_frame, settings_object=settings_object, action_selection_frame=action_selection_frame, go_back=self.go_back, bottom_button_frame=bottom_button_frame)
        
        self.selected_option = "ChangeDPI"
        button_dict = {}
        segmented_frame = ctk.CTkFrame(master=self, fg_color=dark_colour)
        segmented_frame.pack()

        def button_callback(new_selected_button):
            if new_selected_button != self.selected_option:
                options[self.selected_option].pack_forget()
                options[self.selected_option].bottom_frame.pack_forget()
                options[new_selected_button].pack(fill="x",
                                                #    expand=True
                                                   )
                options[new_selected_button].bottom_frame.pack(fill="x", side="right", anchor="e", 
                                                            #    expand=True
                                                               )
                        

                button_dict[self.selected_option].configure(fg_color="transparent", hover=True, text_color=segment_button_colour)
                button_dict[new_selected_button].configure(fg_color=segment_button_colour, hover=False, text_color="black")
                self.selected_option = new_selected_button

        for i in ["Keypress", "Axis", "CycleDPI", "ChangeHost", "ChangeDPI"]:
            button_dict[i] = ctk.CTkButton(master=segmented_frame, text=i, command= lambda i=i: button_callback(i), text_color=segment_button_colour, width=180, height=40, fg_color='transparent', border_width=1, border_color=segment_button_colour, corner_radius=0)
            button_dict[i].pack(side="left", pady=(0,40))
        button_callback("Keypress")

        options_frame.pack(fill="both", expand=True, padx=
                        #    118
                        0
                           )
        control_frame.pack(fill="x", 
                           expand=True,
                             side="bottom",
                             anchor="s"
                             )
        cancel_button_frame.pack(side="left", anchor="s")
        bottom_button_frame.pack(side="right", anchor="s",
                                #  expand=True
                                 )

        go_back_button = ctk.CTkButton(master=cancel_button_frame, text="Cancel", command=lambda: self.go_back(),
                                       height=50,
                                       width=250,
                                       fg_color="#0071C2",
                                       hover_color="#0089EB",
                                       text_color="#101010",
                                       font=ctk.CTkFont(family="Roboto", size=16)

                                       )
        go_back_button.pack(side="bottom",
            anchor="s"
            # side="left",
                            # anchor="w", 
                            # padx=118, pady=(60,100)
                            )

        self.pack(fill="both", expand=True, padx=130, pady=(90, 110))

    def go_back(self):
        self.destroy()
        self.origin_frame.pack(fill="both", expand=True)


class GestureFrame(ctk.CTkFrame):
    def __init__(self, master, root, gesture_object, 
                 ecf,
                 controller_frame,
                   *args, **kwargs):
        super().__init__(master, fg_color="#212121", *args, **kwargs)

        label = ctk.CTkLabel(master=self, text=f"Gesture {gesture_object.direction}", font=ctk.CTkFont(size=27, family="Roboto"), text_color="#606060")
        label.pack(pady=(5,12))
        
        mode_threshold_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        mode_threshold_frame.pack()
        
        new_action_frame_button = ctk.CTkButton(master=mode_threshold_frame, text=f"New Gesture", height=45, width=170, fg_color=gui_variables.standard_green1, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), command=lambda: (controller_frame.pack_forget(), NewActionFrame(master=controller_frame.master, root=root, ecf=ecf, action_selection_frame=action_selection_frame, origin_frame=controller_frame, settings_object=gesture_object)), corner_radius=0)
        
        if gesture_object.direction == "None":
            new_action_frame_button.pack(anchor="s", pady=(20,5), padx=(352,0))
        else:
            new_action_frame_button.pack(side="right", anchor="se", pady=(0,5))
            mode_frame = ctk.CTkFrame(master=mode_threshold_frame, fg_color="transparent")
            mode_frame.pack(side="right", padx=(23,23))
            threshold_frame = ctk.CTkFrame(master=mode_threshold_frame, fg_color="transparent")
            threshold_frame.pack(side="left", padx=(0,0))
            gesture_mode_label = ctk.CTkLabel(master=mode_frame, text="Mode")
            gesture_mode_label.pack()

            mode_stringvar = ctk.StringVar(value=gesture_object.mode)
            gesture_threshold_label = ctk.CTkLabel(master=threshold_frame, text="Interval" if gesture_object.mode == "OnInterval" else "Threshold")
            mode_dropdown = DropdownMenu(master=mode_frame, width=175, height=25, variable=mode_stringvar, values=["OnRelease", "OnInterval", "OnThreshold"], state="normal", command=lambda new_mode=mode_stringvar: (gesture_object.update_mode(new_mode), gesture_threshold_label.configure(text="Interval" if new_mode=="OnInterval" else "Threshold")))
            mode_dropdown.pack(pady=(4,5), padx=2)
            
            gesture_threshold_label.pack()

            threshold_spinbox = IntSpinbox(master=threshold_frame, height=25, width=125, db_query=gesture_object.update_threshold, step_size=1, max_value=99999, min_value=1, value=gesture_object.threshold) 
            threshold_spinbox.pack()

        action_selection_frame = ActionSelectionFrame(master=self, root=root, actions=gesture_object, pack_order=gesture_object.get_added_order())
        action_selection_frame.pack()

        gesture_action_label = gui_variables.EditPageLabel1(master=action_selection_frame.top_frame, text="Gesture Actions:")
        gesture_action_label.pack(anchor="w", pady=(20,0))


class ButtonConfigFrame(ctk.CTkFrame):
    def __init__(self, master, root, ecf, button_settings_object):
        super().__init__(master, fg_color="#191919")

        left_frame = ctk.CTkFrame(master=self, fg_color="#222222",)
        
        self.selected_action_id = button_settings_object.selected_action_id

        right_frame = ctk.CTkFrame(master=self, width=519, fg_color="transparent")

        action_selection_frame = ActionSelectionFrame(master=left_frame, root=root, actions=button_settings_object, pack_order=button_settings_object.get_added_order(), ecf=ecf, gesture_master_frame=right_frame,controller_frame=self)

        title_frame = ctk.CTkFrame(master=left_frame, fg_color="#191919", corner_radius=0)
        label = ctk.CTkLabel(master=title_frame, text=button_settings_object.button_name, font=ctk.CTkFont(family="Roboto", size=30), text_color="#505050")
        label.pack(fill="x", expand=True, pady=(3,5))

        new_action_frame_button = ctk.CTkButton(master=left_frame, text="New Button Action", height=50, width=250, fg_color=gui_variables.standard_green1, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), command=lambda: (self.pack_forget(), NewActionFrame(master=master, root=root, ecf=ecf, action_selection_frame=action_selection_frame, origin_frame=self, settings_object=button_settings_object)), corner_radius=0)

        title_frame.pack(fill="x")
        new_action_frame_button.pack(padx=(240,0), pady=(30,0))

        action_selection_frame.pack()

        action_selection_frame.top_frame.configure(width=1000)

        button_action_label = gui_variables.EditPageLabel1(master=action_selection_frame.top_frame, text="Button Actions:")
        button_action_label.pack(anchor="w", pady=(20, 2),)

        right_frame.pack(side="right", fill="both", expand=True, anchor="e", padx=(0, 10), pady=(10,10))
        left_frame.pack(side="left", fill="both", expand=True, anchor="w", padx=10, pady=(0,10))


class ScrollFrame(ctk.CTkFrame):
    def __init__(self, master, root, ecf, scroll_settings):
        super().__init__(master, fg_color="transparent")

        container= ctk.CTkFrame(master=self, fg_color="#222222")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        title=ctk.CTkLabel(master=container, text=f"Scroll {scroll_settings.scroll_direction}", text_color="#606060", font=ctk.CTkFont(size=40))
        title.pack(pady=(8, 15))

        # self.selected_action_id = scroll_settings.actions.selected_action_id
        selected_mode_var = ctk.StringVar(value=scroll_settings.mode)

        options_frame = ctk.CTkFrame(master=container, fg_color="transparent")
        options_frame.pack(pady=(0,20))

        scroll_mode_dropdown = DropdownMenu(master=options_frame, width=200, height=40, variable=ctk.StringVar(value=scroll_settings.mode), values=["OnInterval", "OnThreshold"], state="normal", command=lambda new_mode = selected_mode_var: scroll_settings.save_new_mode(new_mode))
        scroll_mode_dropdown.pack(side="left")

        scrollwheel_threshold_spinbox = IntSpinbox(master=options_frame, width=180, step_size=5, min_value=1, max_value=9999, db_query=scroll_settings.update_threshold)
        scrollwheel_threshold_spinbox.set(scroll_settings.threshold)
        scrollwheel_threshold_spinbox.pack(side="left", padx=70)

        action_selection_frame = ActionSelectionFrame(master=container, root=root, actions=scroll_settings.actions, pack_order=scroll_settings.actions.get_added_order())
        new_action_frame_button = ctk.CTkButton(master=options_frame, height=45, width=220, fg_color=gui_variables.standard_green1, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), text="New Scroll Action", command=lambda: (self.pack_forget(), NewActionFrame(master=master, root=root, ecf=ecf, action_selection_frame=action_selection_frame, origin_frame=self, settings_object=scroll_settings)), corner_radius=0)
        new_action_frame_button.pack(side="right")

        action_selection_frame.pack(padx=(0,200))
        
        scroll_action_label = gui_variables.EditPageLabel1(master=action_selection_frame.top_frame, text="Scroll Actions:")
        scroll_action_label.pack(anchor="w", pady=(20,0))



class TouchTapProxyFrame(ctk.CTkFrame):
    def __init__(self, master, root, ecf, ttp_object):
        super().__init__(master, fg_color="transparent")

        container = ctk.CTkFrame(master=self, fg_color="#222222")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        title=ctk.CTkLabel(master=container, text=f"Thumbwheel {ttp_object.ttp}", text_color="#606060", font=ctk.CTkFont(size=40))
        title.pack(pady=(8, 15))


        action_selection_frame = ActionSelectionFrame(master=container, root=root, actions=ttp_object)

        new_action_frame_button = ctk.CTkButton(master=container, text=f"New {ttp_object.ttp} Action", height=45, width=220, corner_radius=0, fg_color=gui_variables.standard_green1, hover_color=gui_variables.standard_green3, font=ctk.CTkFont(family="Helvetica Neue",size=15), command=lambda: (self.pack_forget(), NewActionFrame(master=master, root=root, ecf=ecf, origin_frame=self, action_selection_frame=action_selection_frame, settings_object=ttp_object)))

        new_action_frame_button.pack(padx=(400,0))
        action_selection_frame.pack(padx=(0,200))



        ttp_action_label = gui_variables.EditPageLabel1(master=action_selection_frame.top_frame, text=f"{ttp_object.ttp} Actions:")
        ttp_action_label.pack(anchor="w", pady=(20,0))




class Checkbox(ctk.CTkCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(font=("Roboto", 15), corner_radius=0, onvalue=True, offvalue=False, checkbox_width=28, checkbox_height=28,
                         text_color="gray45",
                        
                        # hover_color="#0071C2",
                        # fg_color="#0089EB",
                        
fg_color="#0071C2",
                                        hover_color="#0089EB",

                        
                         border_width=3,
                          *args, **kwargs)


class CycleDPIRadioButton(ctk.CTkFrame):
    def __init__(self, master, cycledpi_object, delete_command, passthrough_command, *args, **kwargs):
        super().__init__(master, fg_color="transparent", width=520, height=50, *args, **kwargs)
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()

        self.pack_propagate(False)
        cycledpi_dpi_array = ctk.CTkLabel(master=self, text=cycledpi_object.dpi_array if len(cycledpi_object.dpi_array) < 25 else f"{cycledpi_object.dpi_array[0:25]}...", text_color=gui_variables.primary_colour, font=ctk.CTkFont(family="Noto Sans"))

        radio_button = MatthewsRadioButton(master=self, width=100, text="CycleDPI", command=lambda: passthrough_command(), hover_elements=(cycledpi_dpi_array))
        radio_button.pack(side="left", anchor="w")

        delete_cycledpi_button = ctk.CTkButton( master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=0, 
                                                command=lambda: (self.destroy(), delete_command()))
        cycledpi_dpi_array.configure(anchor="w", 
                                  justify="left")
        cycledpi_dpi_array.pack(anchor="w", pady=0, side="left", fill="x", 
                                expand=True
                                )
        delete_cycledpi_button.pack(side="right", anchor="e")



class KeypressRadioButton(ctk.CTkFrame):
    def __init__(self, master, keypress_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=520, height=50)
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

        keypress_keys = ctk.CTkLabel(master=self, text=keypress_text if len(keypress_text)<28 else f"{keypress_text[0:25]}...",
                                     text_color="#6C757D",
                                     font=ctk.CTkFont(family="Noto Sans", 
                                                      size=14 if len(keypress_text)<20 else 12
                                                      ))

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



        delete_keypress_button = ctk.CTkButton(master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=0, 
                                               command=lambda: (self.destroy(), delete_command())
                                               )
        delete_keypress_button.pack(side="right", anchor="e")
        


class ChangeDPIRadioButton(ctk.CTkFrame):
    def __init__(self, master, changedpi_object, delete_command, passthrough_command, *args, **kwargs):
        super().__init__(master, fg_color="transparent", width=520, height=50, *args, **kwargs)
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.pack_propagate(False)
        
        changedpi_increment = ctk.CTkLabel(master=self, text=changedpi_object.increment, text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100, text=f"ChangeDPI",  command=lambda: passthrough_command(),  hover_elements=(changedpi_increment)  )
        radio_button.pack(side="left", anchor="w")        
        
        delete_changedpi_button = ctk.CTkButton(master=self,height=20,width=80,text="Delete",fg_color="transparent",font=ctk.CTkFont(family="Noto Sans"),text_color="#6C757D",border_color="#6C757D",hover_color="#450C0F",border_width=1,corner_radius=0, command=lambda: (self.destroy(), delete_command()))
        changedpi_increment.configure(anchor="w", justify="left")
        changedpi_increment.pack(anchor="w",pady=0,side="left",fill="x", expand=True)
        delete_changedpi_button.pack(side="right", anchor="e")


class AxisRadioButton(ctk.CTkFrame):
    def __init__(self, master, axis_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=520, height=50)
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.pack_propagate(False)


        # hidden_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        axis_info1 = ctk.CTkLabel(master=self, text=f"{axis_object.axis_button}: ",
                                     text_color="#6C757D",
                                     font=ctk.CTkFont(family="Noto Sans"))

        axis_info2 = ctk.CTkLabel(master=self, text=axis_object.axis_multiplier, text_color=gui_variables.primary_colour,
                                  font=ctk.CTkFont(family="Noto Sans"))

        radio_button = MatthewsRadioButton(master=self, width=100,
                                            text=f"Axis:",
                                             command=lambda: passthrough_command(),
                                             hover_elements=(
                                                #  hidden_frame,
                                                   axis_info1, axis_info2))
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
                corner_radius=0,
                command=lambda: (self.destroy(), delete_command())
                                           )


        axis_info1.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
        )
        axis_info2.configure(anchor="w", 
                                  justify="left")       
        axis_info2.pack(
            anchor="w",
            pady=0,
            side="left",
            fill="x",
            expand=True
        )

        delete_axis_button.pack(side="right", anchor="e")


class DropdownMenu(ctk.CTkOptionMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
        fg_color="#1263A1",
        button_color="#0F558A",
        button_hover_color="#3A9EE9",
        dropdown_fg_color="#0D4773",
        dropdown_hover_color="#0F558A",
        dropdown_text_color="white",
        # width=300,
        # height=40,
        font=ctk.CTkFont(size = 14, family="Noto Sans",),
        dropdown_font=ctk.CTkFont(size=15, family="Noto Sans",),
        corner_radius=0,
        )


class ChangeHostRadioButton(ctk.CTkFrame):
    def __init__(self, master, changehost_object, delete_command, passthrough_command):
        super().__init__(master, fg_color="transparent", width=520, height=50)
        self.radio_button_clicked = lambda: radio_button.radio_button_clicked()
        self.another_button_clicked = lambda: radio_button.another_button_clicked()
        self.set_clicked = lambda: radio_button.set_clicked()
        self.pack_propagate(False)
        
        hidden_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        changehost_text = ctk.CTkLabel(master=self, text="Previous" if changehost_object.host_change == "prev" else changehost_object.host_change.title(), text_color=gui_variables.primary_colour)

        radio_button = MatthewsRadioButton(master=self, width=100, text=f"ChangeHost", command=lambda: passthrough_command(), hover_elements=(hidden_frame, changehost_text))
        radio_button.pack(side="left", anchor="w")        

        changehost_text.pack(anchor="w",pady=0,side="left",fill="x",)

        delete_changehost_button = ctk.CTkButton(master=self, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=0,
                    command=lambda: (self.destroy(), delete_command())
        )

        delete_changehost_button.pack(side="right", anchor="e")
        hidden_frame.pack(anchor="w", side="left", fill="x", expand=True)



class ShowGestureButton(ctk.CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs, 
                         image=svg_to_image(path="images/arrow1.svg", output_height=22, output_width=22), 
                        #  corner_radius=0, height=40, border_spacing=10,  font=ctk.CTkFont(family="Noto Sans",size=14 ), 
                        #    fg_color="transparent", text_color=("gray10", "gray90"), anchor="w"
                           )

        self.down_arrow = svg_to_image(path="images/arrow1.svg", output_height=22, output_width=22)
        self.down_arrow_hover = svg_to_image(path="images/arrow1a.svg", output_height=22, output_width=22)
        
        self.up_arrow = svg_to_image(path="images/arrow2.svg", output_height=22, output_width=22)
        self.up_arrow_hover = svg_to_image(path="images/arrow2a.svg", output_height=22, output_width=22)
        self.arrow_down_leave()
        self.configure_down()

    def configure_up(self, event=None):
        self.arrow_up_enter()
        self.bind('<Enter>', lambda event: self.arrow_up_enter(event))
        self.bind('<Leave>', lambda event: self.arrow_up_leave(event))

    def configure_down(self, event=None):
        self.arrow_down_leave   ()
        self.bind('<Enter>', lambda event: self.arrow_down_enter(event))
        self.bind('<Leave>', lambda event: self.arrow_down_leave(event))

    def arrow_up_enter(self, event=None):
        self.configure(image=self.up_arrow_hover)

    def arrow_up_leave(self, event=None):
        self.configure(image=self.up_arrow)

    def arrow_down_enter(self, event=None):
        self.configure(image=self.down_arrow_hover)

    def arrow_down_leave(self, event=None):
        self.configure(image=self.down_arrow)



class GestureRadioButton(ctk.CTkFrame):
    def __init__(self, master, gesture_objects, ecf, gesture_master_frame, controller_frame, passthrough_command, root):
        super().__init__(master, fg_color="transparent")

        self.passthrough_command = passthrough_command
        self.gesture_objects = gesture_objects
        self.controller_frame = controller_frame
        self.gesture_frame_dict = {}
        self.gesture_master_frame = gesture_master_frame
        self.root = root
        self.ecf=ecf

        radio_button_frame = ctk.CTkFrame(master=self, fg_color="transparent", width=520, height=50)
        radio_button_frame.pack(fill="x", expand=True)
        radio_button_frame.pack_propagate(False)
        self.radio_button = MatthewsRadioButton(master=radio_button_frame, width=100, text=f"Gestures", command=lambda: self.radio_button_clicked(),)
        self.radio_button.pack(side="left", anchor="w", fill="x", expand=True)       

        self.gesture_frame_toggled = False

        self.show_hide_gestures_button = ShowGestureButton(master=radio_button_frame, hover=False, height=20, width=100, text="Show Gestures", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#43474C", border_width=0, anchor="w", command=self.toggle_gesture_frame)
        self.show_hide_gestures_button.pack(side="right", anchor="e")
        self.gesture_button_dict = {}
        self.gesture_button_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.currently_viewed_frame = None
        self.currently_active_button = None

        for i in self.gesture_objects.values():
            self.create_gesture_button(i)

    def toggle_gesture_frame(self):
        if self.gesture_frame_toggled == True:
            self.gesture_button_frame.pack_forget()
            self.show_hide_gestures_button.configure(text="Show Gestures")
            self.show_hide_gestures_button.configure_down()
            if self.currently_viewed_frame is not None:
                self.currently_viewed_frame.pack_forget()
                self.currently_viewed_frame = None
            if self.currently_active_button is not None:
                self.currently_active_button.configure(fg_color="transparent")
                self.currently_active_button = None
        else:
            self.show_hide_gestures_button.configure(text="Hide Gestures ")     
            self.show_hide_gestures_button.configure_up()
            self.gesture_button_frame.pack(side="bottom", anchor="s", fill="x", expand=True)
        self.gesture_frame_toggled = not self.gesture_frame_toggled

    def create_gesture_button(self, gesture_settings):
        self.gesture_button_dict[gesture_settings.direction] = ctk.CTkButton(master=self.gesture_button_frame, corner_radius=0, height=40, border_spacing=10,  font=ctk.CTkFont(family="Noto Sans",size=14 ),  fg_color="transparent", text_color="gray60", hover_color="#606060", anchor="w", text=f"Gesture {gesture_settings.direction}",)
        self.gesture_button_dict[gesture_settings.direction].pack(fill="x", anchor="w", padx=(40,0))

        self.gesture_button_dict[gesture_settings.direction].configure(command=lambda button=gesture_settings.direction: self.gesture_button_clicked(button))
        
    def create_gesture_frames(self, button):
        self.gesture_frame_dict[button] = GestureFrame(master=self.gesture_master_frame, gesture_object=self.gesture_objects[button], ecf=self.ecf, controller_frame=self.controller_frame, root=self.root)



    def gesture_button_clicked(self, button):
        if button not in self.gesture_frame_dict.keys():
            self.create_gesture_frames(button)
        
        if self.currently_viewed_frame != self.gesture_frame_dict[button]:
            if self.currently_active_button is not None:
                self.currently_active_button.configure(fg_color="transparent")
            self.currently_active_button = self.gesture_button_dict[button]
            self.currently_active_button.configure(fg_color="#353535")


            if self.currently_viewed_frame is not None:
                self.currently_viewed_frame.pack_forget()

            self.currently_viewed_frame = self.gesture_frame_dict[button]
            self.currently_viewed_frame.pack(fill="both", expand=True,)


    def set_clicked(self):
        self.show_hide_gestures_button.pack_forget()
        self.radio_button.set_clicked()
        self.gesture_button_frame.pack(side="bottom", anchor="s", fill="x", expand=True)
        self.gesture_button_clicked("Up")

    def radio_button_clicked(self):
        self.passthrough_command()
        self.show_hide_gestures_button.pack_forget()
        if self.gesture_frame_toggled == False:
            self.gesture_button_frame.pack(side="bottom", anchor="s", fill="x", expand=True)
        if self.currently_viewed_frame == None:
            # self.gesture_frame_dict["Up"].pack(fill="both", expand=True)
            # self.currently_viewed_frame = self.gesture_frame_dict["Up"]
            # self.pack_gesture_frame()
            # self.gesture_button_dict["Up"].configure(fg_color="blue")
            # self.currently_active_button = self.gesture_button_dict["Up"]
            self.gesture_button_clicked("Up")

    def another_button_clicked(self):
        self.radio_button.another_button_clicked()
        self.show_hide_gestures_button.pack(side="right", anchor="e")
        self.gesture_frame_toggled = False
        self.show_hide_gestures_button.configure(text="Show Gestures")
        self.show_hide_gestures_button.configure_down()
        self.gesture_button_frame.pack_forget()
        if self.currently_active_button != None:
            self.currently_active_button.configure(fg_color="transparent")
            self.currently_active_button = None
        if self.currently_viewed_frame != None:
            self.currently_viewed_frame.pack_forget()
            self.currently_viewed_frame = None

class ActionSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, root, actions, pack_order=None, 
                create_top_frame=True,
                gesture_master_frame=None,
                ecf=None,
                controller_frame=None):
        super().__init__(master, fg_color="transparent")
        
        self.actions = actions
        self.radio_buttons_dictionary = {}
        self.ecf=ecf

        if create_top_frame==True:
            self.top_frame = ctk.CTkFrame(master=self, fg_color="transparent", corner_radius=0, height=10)
            self.top_frame.pack(fill="x")

        def create_simple_button(id, name):
            radio_button_row = ctk.CTkFrame(master=self, fg_color="transparent")
            radio_button_row.pack()
            radio_button = MatthewsRadioButton(master=radio_button_row, width=520, text=name, command=lambda c=id: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            
            self.radio_buttons_dictionary[id] = radio_button

        for i in [(actions.default, "Default"), (actions.nopress, "NoPress"), (actions.togglesmartshift, "Toggle SmartShift"), (actions.togglehiresscroll, "Toggle HiRes Scroll")]:
            if i[0] is not None:
                create_simple_button(id=i[0], name=i[1])

        self.id_of_gesture = None
        if gesture_master_frame is not None:
            self.create_gesture_elements(self.actions.gestures, gesture_master_frame, controller_frame, root)

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
        try:
            self.radio_buttons_dictionary[self.actions.selected_action_id].set_clicked()
        except:
            print("error setting clicked button")

    def create_gesture_elements(self, gestures, gesture_master_frame, controller_frame, root):
        self.gesture_button = GestureRadioButton(master=self, gesture_objects=gestures, gesture_master_frame = gesture_master_frame, controller_frame=controller_frame, ecf=self.ecf, root=root, passthrough_command=lambda n=self.actions.gestures.button_config_id: self.select_configuration(n))
        self.gesture_button.pack()
        self.radio_buttons_dictionary[gestures.button_config_id] = self.gesture_button
        self.id_of_gesture = gestures.button_config_id
        return 

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

        if self.id_of_gesture != None and self.id_of_gesture != new_selected_id and self.gesture_button.gesture_frame_toggled == True: 
            self.gesture_button.toggle_gesture_frame()
    def update_deleted_configuration(self, deleted_id):
        if deleted_id == self.actions.selected_action_id:
            if self.actions.default is not None:
                self.radio_buttons_dictionary[self.actions.default].set_clicked()
                self.actions.selected_action_id = self.actions.default
            else:

                self.radio_buttons_dictionary[self.actions.nopress].set_clicked()
                self.actions.selected_action_id = self.actions.nopress


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



# TODO
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
    icon = tk.PhotoImage(file="images/icon.png")
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
