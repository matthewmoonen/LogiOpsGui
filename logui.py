import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
# from CTkListbox import *
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
import keymates
import json

from PIL import Image, ImageTk
import io
import cairosvg










def svg_to_image(path, output_width=300, output_height=300):
    with open(path, 'rb') as svg_file:
        svg_content = svg_file.read()

    png_data = cairosvg.svg2png(bytestring=svg_content, output_width=output_width, output_height=output_height)
    
    # Convert PNG data to PIL Image
    return ctk.CTkImage(Image.open(io.BytesIO(png_data)), size=(output_width, output_height))


class MatthewsRadioButton:
    """
    Some UI elements have rendering issues in CustomTkinter on Linux, radio buttons in particular look blocky.
    
    This class creates smooth-looking radio buttons using SVG files.
    
    See here for further information:
    https://github.com/TomSchimansky/CustomTkinter/issues/1384
    """

    def __init__(self, master, text, font=None, command=None, selected_image_path="images/radio_button_selected.svg", deselected_image_path="images/radio_button_deselected.svg", hover_image_path="images/radio_button_hover.svg", icon_size=27, width=400, height=None, fg_color="transparent",):

        self.radio_button_selected = svg_to_image(path=selected_image_path, output_height=icon_size, output_width=icon_size)
        self.radio_button_deselected = svg_to_image(path=deselected_image_path, output_height=icon_size, output_width=icon_size)
        self.radio_button_hover = svg_to_image(path=hover_image_path, output_height=icon_size, output_width=icon_size)
        self.user_command = command

        if height is None: # Set height to icon_size if not explicitly set
            height = icon_size

        if font == None:
            font=ctk.CTkFont(family="Noto Sans", size=17)

        self.button = ctk.CTkButton(master=master, text=text, image=self.radio_button_deselected, command=self.radio_button_clicked, anchor="w", font=font, text_color="gray65", height=height, width=width, fg_color=fg_color, hover=False)
        self.button.bind('<Enter>', lambda event: self.radio_button_enter(event))
        self.button.bind('<Leave>', lambda event: self.radio_button_leave(event))
        
        self.is_selected = False

    def radio_button_enter(self, event):
        self.button.configure(image=self.radio_button_hover)

    def radio_button_leave(self, event):
        self.button.configure(image=self.radio_button_deselected)
        # self.button.configure('<Leave>', text_color="gray65")

    def another_button_clicked(self):
        try:
            self.button.configure(image=self.radio_button_deselected)
            self.is_selected = False
            self.button.bind('<Enter>', lambda event: self.radio_button_enter(event))
            self.button.bind('<Leave>', lambda event: self.radio_button_leave(event))
        except:
            pass

    def radio_button_clicked(self):
        if self.is_selected: # If the button is already selected, just return without changing anything
            return

        self.is_selected = True

        self.button.unbind('<Enter>')
        self.button.unbind('<Leave>')
        self.button.configure(image=self.radio_button_selected)

        if self.user_command: # Run the user's command, if provided
            self.user_command()

    def grid(self, **kwargs):
        self.button.grid(**kwargs)

    def update_text(self, new_text):
        """Update the text of the radio button."""
        self.button.configure(text=new_text)
    


class FloatSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: float = 1.0, min_value: float = None, 
                 max_value: float = None, decimal_places: int = 1, command: Callable = None, db_query=None, value=None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places
        self.command = command
        self.db_query = db_query
        self.value = value if value is not None else (min_value if min_value is not None else 0.0)

        self.enabled = True  # Initial state is enabled
        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-2, height=height-2, command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'), width=width-(2.8*height), height=height-4, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.insert(0, self.format_value(self.value))

        self.add_button = ctk.CTkButton(self, text="+", width=height-2.5, height=height-2.5, command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.bind("<FocusOut>", self.on_focus_out)

    def format_value(self, value):
        return f"{value:.{self.decimal_places}f}"

    def validate(self, new_text):
        if new_text in ("", "-"):
            return True
        try:
            float(new_text)
            return True
        except ValueError:
            return False

    def on_focus_out(self, event):
        try:
            value = float(self.entry.get())
            value = max(self.min_value, value) if self.min_value is not None else value
            value = min(self.max_value, value) if self.max_value is not None else value
        except ValueError:
            value = self.value  # Use stored value if parsing fails

        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()

    def add_button_callback(self):
        try:
            value = float(self.entry.get())
            value = value + self.step_size
            value = min(self.max_value, value) if self.max_value is not None else value
        except ValueError:
            return
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()


    def subtract_button_callback(self):
        try:
            value = float(self.entry.get())
            value = value - self.step_size
            value = max(self.min_value, value) if self.min_value is not None else value
        except ValueError:
            return
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()

    def get(self) -> float:
        try:
            return float(self.entry.get())
        except ValueError:
            return self.value

    def set(self, value: float):
        value = max(self.min_value, value) if self.min_value is not None else value
        value = min(self.max_value, value) if self.max_value is not None else value
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        self.value = value

    def toggle_enable(self, new_enabled_state):
        self.enabled = new_enabled_state
        state = "normal" if self.enabled else "disabled"
        self.entry.configure(state=state)
        self.add_button.configure(state=state)
        self.subtract_button.configure(state=state)

    def run_command(self):
        if callable(self.command):
            self.command()

    def run_db_query(self):
        if callable(self.db_query):
            self.db_query(self.value)


class IntSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: int = 1, min_value: int = None, max_value: int = None, 
                 command: Callable = None, #TODO: Remove
                 db_query = None, value=None,
                  **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.command = command
        self.db_query = db_query
        self.value = value


        self.enabled = True  # TODO: Initial state is enabled

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand TODO: Fix repeats here
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-2, height=height-2, command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.default_value = 0 if min_value is None else min_value  # Set default value based on min_value

        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'), width=width-(2.8*height), height=height-4, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        
        self.entry.bind("<FocusOut>", self.on_focus_out)  # Bind the FocusOut event

        self.add_button = ctk.CTkButton(self, text="+", width=height-2.5, height=height-2.5, command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, ["0" if self.value == None else self.value]) 



    def validate(self, new_text):
        if new_text == "":
            return True
        if self.min_value < 0:
            if new_text == "-":
                return True        
        try:
            int(new_text)
            return True
        except ValueError:
            return False



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
        if self.value != value:
            self.value = value
            self.run_db_query()

    def add_button_callback(self):
        try: 
            value = int(self.entry.get()) // self.step_size * self.step_size + self.step_size # Set new value to closest multiple of step size after the current value
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            if self.value != value:
                self.value = value
                self.run_db_query()
        except ValueError:
            return

    def run_db_query(self):

        if callable(self.db_query):
            self.db_query(self.value)


    def subtract_button_callback(self):
        # if self.command is not None:
        #     self.command()
        try:
            def get_nearest_rounded_value(): # Set new value to closest multiple of step size after the current value
                previous_value = int(self.entry.get())
                return previous_value // self.step_size * self.step_size - self.step_size if previous_value % self.step_size == 0 else previous_value // self.step_size * self.step_size

            value = get_nearest_rounded_value()
            
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            if self.value != value:
                self.value = value
                self.run_db_query()
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
        self.value = value

    def toggle_enable(self, new_enabled_state):
        self.enabled = new_enabled_state
        state = "normal" if self.enabled else "disabled"
        self.entry.configure(state=state)
        self.add_button.configure(state=state)
        self.subtract_button.configure(state=state)



class DeviceDropdown():
    def __init__(self, master_frame, device_added_callback):
        self.master_frame = master_frame
        self.device_added_callback = device_added_callback
        self.setup_option_menu()
        self.create_add_device_button()

    def setup_option_menu(self):
        if hasattr(self, 'option_menu'): # If the option menu already exists, destroy it first
            self.option_menu.destroy()

        self.options = execute_db_queries.get_unconfigured_devices()
        self.selected_option_var = ctk.StringVar(value=' Select Device To Add')
        self.option_menu = ctk.CTkOptionMenu(master=self.master_frame, variable=self.selected_option_var, values=self.options, state="normal", width=350, height=35, corner_radius=0, dropdown_fg_color="#212121", dropdown_text_color="#D6D6D6", dropdown_hover_color="#1F538D", text_color="#D6D6D6", font=("Noto Sans", 14), dropdown_font=("Noto Sans", 16), command=self.device_dropdown_option_chosen)
        self.option_menu.grid(row=1, column=0, pady=20, padx=(15, 0), sticky="w")


    def create_add_device_button(self):
        if hasattr(self, 'button_for_adding_devices'):
            self.button_for_adding_devices.destroy()

        self.button_for_adding_devices = ctk.CTkButton(master=self.master_frame, height=37, width=140, state="disabled", text="Add Device", text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=("#28A745"), font=ctk.CTkFont( size=14, family="Veranda"))
        self.button_for_adding_devices.grid(padx=15, row=1, column=1, sticky="w")

    def add_device_button_clicked(self):
        self.device_added_callback(self.selected_option_var.get())
        self.create_add_device_button()
        self.setup_option_menu()

    def device_dropdown_option_chosen(self, new_device):
        self.selected_device = new_device
        self.button_for_adding_devices.configure(state="normal", fg_color="#198754")
        self.button_for_adding_devices.configure(command=self.add_device_button_clicked) 


class ConfigurationFrame():
    def __init__(self, master_frame, config, is_selected_configuration, edit_configuration_callback, delete_config_callback, select_configuration):
        self.master_frame = master_frame
        self.config = config
        self.edit_configuration_callback = edit_configuration_callback
        self.select_configuration = select_configuration
        self.delete_config_callback = delete_config_callback

        self.config_row_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent")
        self.config_row_frame.pack()

        self.radio_button = MatthewsRadioButton(master=self.config_row_frame, width=600, text=config.configuration_name, command=lambda c=self.config.configuration_id: select_configuration(c))
        self.radio_button.grid(row=0, column=0)

        if is_selected_configuration == True:
            self.radio_button.radio_button_clicked()

        duplicate_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", border_width=1, corner_radius=2, text=" Copy",)
        duplicate_configuration_button.grid(row=0, column=1, sticky="e", padx=15)

        self.edit_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", border_width=1, hover_color="#113A1B", corner_radius=2, text=" Edit", command=lambda c=self.config.configuration_id: self.edit_configuration(configuration_id=c))
        self.edit_configuration_button.grid(row=0, column=2, sticky="e")

        delete_configuration_button = ctk.CTkButton(master=self.config_row_frame, height=20, width=80, text="Delete", fg_color="transparent", font=ctk.CTkFont(family="Noto Sans"), text_color="#6C757D", border_color="#6C757D", hover_color="#450C0F", border_width=1, corner_radius=2, command=lambda: self.configuration_deletion_warning())
        delete_configuration_button.grid(row=0, column=3, padx="15", pady="5", sticky="e")
        
        self.config_row_frame.columnconfigure(1, weight=2)
        self.master_frame.columnconfigure(2, weight=1)



    def edit_configuration(self, configuration_id):
        # Disable the edit button to prevent multiple clicks
        self.edit_configuration_button.configure(state='disabled')
        self.edit_configuration_callback(configuration_id, self.radio_button)

        def task():

            # Re-enable the button in the main thread
            self.edit_configuration_button.after(0, lambda: self.edit_configuration_button.configure(state='normal'))
        # Run the task in a separate thread
        threading.Thread(target=task).start()


    def configuration_deletion_warning(self):
        msg = CTkMessagebox(title="Delete Configuration?", message="Delete configuration?", option_1="Delete", option_2="Cancel", width=600, height=300, fade_in_duration=200)
        if msg.get() == "Delete":
            self.config_row_frame.destroy()
            self.delete_config_callback(configuration_id=self.config.configuration_id)
                    

class DeviceFrame():
    def __init__(self, master_frame, user_device, configs, delete_device_callback, edit_configuration_callback, delete_configuration_callback, add_configuration_callback, configuration_frames={}):
        self.user_device = user_device
        self.configs = configs
        self.delete_device_callback = delete_device_callback
        self.edit_configuration_callback = edit_configuration_callback
        self.delete_configuration_callback = delete_configuration_callback
        self.add_configuration_callback = add_configuration_callback
        self.configuration_frames = configuration_frames

        self.container_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        self.container_frame.pack_forget()

        self.frame_title = ctk.CTkLabel(master=self.container_frame, text=user_device.device_name, font=ctk.CTkFont(family="Roboto", size=60), text_color="gray50")
        self.frame_title.pack(fill="x", expand=False, pady=20)

        self.device_options_frame = ctk.CTkFrame(master=self.container_frame, corner_radius=0, fg_color="transparent")
        self.device_options_frame.pack(fill="x", expand=False)

        # self.new_configuration_button = ctk.CTkButton(master=self.device_options_frame, text="Add Device Configuration", text_color="white", fg_color="#198754", height=40, width=230, hover_color="#28A745", font=ctk.CTkFont(family="Noto Sans"), command=lambda d=self.user_device.device_id, n=self.user_device.device_name: self.add_new_configuration(d, n))
        # self.new_configuration_button.grid(row=0, column=1, sticky="e",)

        self.new_configuration_button = ctk.CTkButton(
            master=self.device_options_frame, 
            text="Add Device Configuration", 
            text_color="white", 
            fg_color="#198754", 
            height=40, 
            width=230, 
            hover_color="#28A745", 
            font=ctk.CTkFont(family="Noto Sans"), 
            command=lambda d=self.user_device.device_id, n=self.user_device.device_name: self.add_new_configuration(d, n)
        )
        self.new_configuration_button.grid(row=0, column=1, sticky="e")



        self.delete_device_button = ctk.CTkButton(master=self.device_options_frame, text="Delete Device", fg_color="#DC3545", height=40, width=150, hover_color="red", font=ctk.CTkFont(family="Noto Sans"), command=lambda d=user_device.device_id: self.device_deletion_warning(d))
        self.delete_device_button.grid(row=0, column=2, sticky="e", padx=(25, 15))

        self.device_options_frame.columnconfigure((0), weight=1)
        self.device_options_frame.columnconfigure((1), weight=2)

        self.radio_button_frame = ctk.CTkFrame(master=self.container_frame)
        self.radio_button_frame.pack(fill="x", expand=False)

        self.create_configuration_frames()




    def add_new_configuration(self, device_id, device_name):
        # Disable the button to prevent multiple clicks
        self.new_configuration_button.configure(state='disabled')
        # Perform the long-running task
        newest_configuration_id = execute_db_queries.new_empty_configuration(device_id, device_name)
        self.add_configuration_callback(device_id, newest_configuration_id)

        def task():

            # Update the GUI in the main thread
            self.new_configuration_button.after(200, lambda: self.new_configuration_button.configure(state='normal'))

        # Run the task in a separate thread
        threading.Thread(target=task).start()



    def select_configuration(self, configuration_id):
        try:
            self.configuration_frames[self.user_device.selected_config].radio_button.another_button_clicked()
            self.user_device.selected_config = configuration_id
        except KeyError:
            pass 

    def delete_configuration(self, configuration_id):
        self.delete_configuration_callback(configuration_id=configuration_id, device_id=self.user_device.device_id)
        self.user_device.config_ids.remove(configuration_id)

        if len(self.user_device.config_ids) < 1:
            self.delete_device_callback(device_id=self.user_device.device_id)
        # del self.configuration_frames[configuration_id] TODO: Remove if no issues arise
    

    def create_configuration_frame(self, configuration_id, return_button=False):
        if self.user_device.selected_config == configuration_id:
            is_selected_configuration = True
        else:
            is_selected_configuration = False
        self.configuration_frames[configuration_id] = ConfigurationFrame(master_frame=self.radio_button_frame, config=self.configs[configuration_id], is_selected_configuration=is_selected_configuration, edit_configuration_callback=self.edit_configuration_callback, delete_config_callback=self.delete_configuration, select_configuration=self.select_configuration)

        if return_button == True:
            return self.configuration_frames[configuration_id].radio_button

    def add_new_config_row(self, newest_configuration_id, configs, user_device):
        self.user_device = user_device
        self.configs = configs
        self.create_configuration_frame(configuration_id=newest_configuration_id, return_button=True)

    def create_configuration_frames(self):
        for i in self.user_device.config_ids:
            self.create_configuration_frame(i)

    def device_deletion_warning(self, device_id):
        msg = CTkMessagebox(title="Delete Device?",
                            message="Deleting device will also delete all its configurations.",
                            option_1="Delete",
                            option_2="Cancel",
                            width=600,
                            height=300,
                            fade_in_duration=200
                            )
        if msg.get() == "Delete":
            self.destroy()
            self.delete_device_callback(device_id)
            del self.user_device


    def pack(self, *args, **kwargs):
        """
        Allows DeviceFrame to be packed like a regular widget.
        Passes all arguments to its container_frame's pack method.
        """
        self.container_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)




class DeviceFrameController():
    def __init__(self, master_frame, user_devices_and_configs, delete_device_callback_to_main_page, left_buttons, refresh_user_devices_and_configs_callback, refresh_buttons_callback, edit_configuration_callback, configuration_added_callback_to_main_page, delete_configuration_callback, current_frame=None, device_frame_dict={}):
        self.user_devices_and_configs = user_devices_and_configs
        self.current_frame = current_frame
        self.device_frame_dict = device_frame_dict
        self.left_buttons = left_buttons
        self.refresh_buttons_callback = refresh_buttons_callback
        self.refresh_user_devices_and_configs_callback = refresh_user_devices_and_configs_callback
        self.master_frame = master_frame
        self.delete_device_callback_to_main_page = delete_device_callback_to_main_page
        self.edit_configuration_callback = edit_configuration_callback
        self.configuration_added_callback_to_main_page = configuration_added_callback_to_main_page
        self.delete_configuration_callback = delete_configuration_callback
        self.create_frames()

        if len(self.user_devices_and_configs.user_devices) > 0:
            self.pack_a_frame(frame_to_pack=next(iter(self.device_frame_dict)))
        else:
            self.pack_a_frame()

    def delete_device_callback(self, device_id):
        self.device_frame_dict[device_id].pack_forget()
        self.device_frame_dict[device_id].destroy()
        del self.device_frame_dict[device_id]
        self.delete_device_callback_to_main_page(device_id)

        self.pack_a_frame(frame_to_pack=next(iter(self.device_frame_dict)), device_has_been_deleted=True)


    def create_single_frame(self, id_to_create):
        self.device_frame_dict[id_to_create] = DeviceFrame(master_frame=self.master_frame, add_configuration_callback=self.configuration_added, edit_configuration_callback=self.edit_configuration_callback, delete_device_callback=self.delete_device_callback, delete_configuration_callback=self.delete_configuration, user_device=self.user_devices_and_configs.user_devices[id_to_create], configs=self.user_devices_and_configs.user_configurations)
        
    def create_frames(self):
        
        for i in self.user_devices_and_configs.user_devices.keys():
            self.create_single_frame(id_to_create=i)

        placeholder_device_frame = ctk.CTkFrame(master=self.master_frame, corner_radius=0, fg_color="transparent")
        placeholder_device_frame_text = ctk.CTkLabel(master=placeholder_device_frame, text="Add your first device to edit")
        placeholder_device_frame_text.pack()
        self.device_frame_dict[None] = placeholder_device_frame

    def pack_a_frame(self, frame_to_pack=None, device_has_been_deleted=False):
        for i in self.master_frame.winfo_children():
            i.pack_forget()

        if self.current_frame is not None and device_has_been_deleted == False:
            self.current_frame.pack_forget()

        self.current_frame = self.device_frame_dict[frame_to_pack]
        self.current_frame.pack()


    def configuration_added(self, device_id, newest_configuration_id):

        self.configuration_added_callback_to_main_page(device_id, newest_configuration_id)

    def add_new_config_row(self, device_id, newest_configuration_id, user_devices_and_configs):
        self.user_devices_and_configs = user_devices_and_configs
        self.device_frame_dict[device_id].add_new_config_row(newest_configuration_id=newest_configuration_id, configs=self.user_devices_and_configs.user_configurations, 
                                                             user_device=self.user_devices_and_configs.user_devices[device_id]
                                                             )

    def delete_configuration(self, configuration_id, device_id):
        config_before = self.user_devices_and_configs.user_devices[device_id].selected_config
        
        
        self.delete_configuration_callback(configuration_id)

        if config_before != self.user_devices_and_configs.user_devices[device_id].selected_config:
            self.device_frame_dict[device_id].user_device.selected_config = self.user_devices_and_configs.user_devices[device_id].selected_config
            # self.create_single_frame(id_to_create=device_id)
            self.create_frames()
            self.pack_a_frame(frame_to_pack=device_id)

    def finish_deleting_configuration(self):
        pass

    def delete_config_row(self):
        pass

    @property
    def add_new_device_frame(self):
        return self.device_frame_dict

    @add_new_device_frame.setter
    def add_new_device_frame(self, new_device_id):
        self.device_frame_dict.clear()
        self.create_frames()
        self.pack_a_frame(new_device_id)

    @property
    def update_user_devices_and_configs(self):
        return self.user_devices_and_configs

    @update_user_devices_and_configs.setter
    def update_user_devices_and_configs(self, user_devices_and_configs):
        self.user_devices_and_configs = user_devices_and_configs

class LeftButtons():
    def __init__(self, master_frame, user_devices, display_device_frame_callback, currently_selected_device=None):
        self.master_frame = master_frame
        self.user_devices = user_devices
        self.display_device_frame_callback = display_device_frame_callback

        self.left_buttons_frame = ctk.CTkFrame(master=master_frame)
        self.left_buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=0)
        self.currently_selected_device = currently_selected_device        
        
        self.button_objects_dict = {}
        self.setup_left_buttons()

    def setup_left_buttons(self):
                
        for i in self.user_devices.values():
            device_button = ctk.CTkButton(master=self.left_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=i.device_name, font=ctk.CTkFont(family="Noto Sans",size=18 ), command=lambda d=i.device_id: self.button_clicked(d), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            device_button.pack(fill="x", expand=True)
            self.button_objects_dict[i.device_id] = device_button
        
        if len(self.user_devices) > 0:
            self.activate_button(device_id_to_activate=next(iter(self.user_devices)))

    def refresh_left_buttons(self):
        for button in self.button_objects_dict.values():
            button.pack_forget()
        self.button_objects_dict = {}
        self.setup_left_buttons()

    def button_clicked(self, id_of_clicked_button):
        if id_of_clicked_button != self.currently_selected_device:
            self.display_device_frame_callback(id_of_clicked_button)
            self.button_objects_dict[self.currently_selected_device].configure(fg_color = "transparent")
            self.activate_button(device_id_to_activate=id_of_clicked_button)

    def activate_button(self, device_id_to_activate):
        self.currently_selected_device = device_id_to_activate
        self.button_objects_dict[self.currently_selected_device].configure(fg_color = "gray25")

    @property
    def remove_button(self):
        return self.button_objects_dict

    def remove_button(self, device_id):
        # self.button_objects_dict[device_id].destroy()
        self.button_objects_dict[device_id].pack_forget()

    @property
    def update_user_devices(self):
        return self.user_devices

    @update_user_devices.setter
    def update_user_devices(self, user_devices):
        self.user_devices = user_devices
        self.refresh_left_buttons()


class FrontPage(ctk.CTkFrame):
    def __init__(self,
                 master,
                 edit_page = None,
                 selected_device = None
                 ):
        super().__init__(master)

        left_frame = ctk.CTkFrame(master=self, fg_color="#2B2B2B")
        left_frame.grid(row=0, column=0, sticky="nsew", 
                        # rowspan=2
                        )



        app_title = ctk.CTkLabel(master=left_frame, text="  LogiOpsGUI  ", font=ctk.CTkFont(family="Noto Sans",size=44),text_color=gui_variables.primary_colour,pady=20,corner_radius=0)
        app_title.grid(row=0, column=0, columnspan=2, sticky="ew")

        user_devices_label = ctk.CTkLabel(master=left_frame, text="User Devices", font=ctk.CTkFont(family="Noto Sans", weight="bold", size=20),)
        user_devices_label.grid(row=2, column=0, columnspan=2, pady=(30,0))

        right_frame = ctk.CTkFrame(master=self, corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=2)

        self.edit_windows = {}

        self.grid_columnconfigure(1, weight=1)  # Set the weight of the column in the main frame
        self.grid_rowconfigure(1, weight=1)
        

        # TODO: delete now deprecated Classes2.get_devices_and_configs() if no longer needed.
        self.user_devices_and_configs = Classes2.DevicesAndConfigs()
        def refresh_user_devices_and_configs():
            self.user_devices_and_configs = Classes2.DevicesAndConfigs()
            self.devices_frames.update_user_devices_and_configs = self.user_devices_and_configs

        def device_added(new_device_name): # Logic to update the device list with the new device
            new_configuration_id, new_device_id = execute_db_queries.add_new_device(new_device_name)
            refresh_user_devices_and_configs()
            self.left_buttons.update_user_devices = self.user_devices_and_configs.user_devices
            self.devices_frames.update_user_devices_and_configs = self.user_devices_and_configs
            self.devices_frames.add_new_device_frame = new_device_id
            radio_button = self.devices_frames.device_frame_dict[new_device_id].configuration_frames[new_configuration_id].radio_button
            self.edit_configuration(configuration_id=new_configuration_id, radio_button=radio_button)

        def configuration_deleted(configuration_id):
            execute_db_queries.delete_configuration(configuration_id)
            refresh_user_devices_and_configs()
            self.devices_frames.update_user_devices_and_configs = self.user_devices_and_configs

        def configuration_added(device_id, newest_configuration_id):
            refresh_user_devices_and_configs()
            self.devices_frames.update_user_devices_and_configs = self.user_devices_and_configs
            self.devices_frames.add_new_config_row(device_id=device_id, newest_configuration_id=newest_configuration_id, user_devices_and_configs=self.user_devices_and_configs)
            radio_button = self.devices_frames.device_frame_dict[device_id].configuration_frames[newest_configuration_id].radio_button
            
            self.edit_configuration(configuration_id=newest_configuration_id, radio_button=radio_button)

        def device_deleted(deleted_device_id):
            execute_db_queries.delete_device(deleted_device_id)
            refresh_user_devices_and_configs()
            self.devices_frames.update_user_devices_and_configs = self.user_devices_and_configs
            self.left_buttons.update_user_devices = self.user_devices_and_configs.user_devices
            self.left_buttons.refresh_left_buttons()
            self.device_dropdown.setup_option_menu()
            self.device_dropdown.create_add_device_button()

        def refresh_buttons():
            self.left_buttons.refresh_left_buttons

        def display_device_frame(clicked_button_device_id): # Callback function to take the clicked left button's ID and display the corresponding right frame for the device. 
            self.devices_frames.pack_a_frame(frame_to_pack=clicked_button_device_id)

        self.left_buttons = LeftButtons(master_frame=left_frame, user_devices=self.user_devices_and_configs.user_devices, display_device_frame_callback=display_device_frame)
        self.devices_frames = DeviceFrameController(master_frame=right_frame, user_devices_and_configs=self.user_devices_and_configs, left_buttons=self.left_buttons, refresh_buttons_callback = refresh_buttons, edit_configuration_callback=self.edit_configuration, refresh_user_devices_and_configs_callback = refresh_user_devices_and_configs, delete_configuration_callback=configuration_deleted, configuration_added_callback_to_main_page=configuration_added, delete_device_callback_to_main_page=device_deleted)
        self.device_dropdown = DeviceDropdown(master_frame=left_frame, device_added_callback=device_added)

        bottom_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        bottom_frame.grid(row=1, column=1, sticky="ew",
                          columnspan=2
                          )



        def new_window():
            new_window = ctk.CTkToplevel(master)
            new_window.title = "Hi"
            new_window.geometry("800x800")

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

            window_scaling, widget_scaling = get_window_and_widget_scaling()

            widget_scaling_button = FloatSpinbox(master=new_window,
                                                value=widget_scaling,
                                                width=200,
                                                step_size=0.05,
                                                decimal_places=2,
                                                min_value=-1000,
                                                max_value=1000,
                                                command=lambda: set_widget_scaling(widget_scaling_button.get()))
            widget_scaling_button.pack()
            
            window_scaling_button = FloatSpinbox(master=new_window,
                                                value=window_scaling,
                                                width=200,
                                                step_size=0.05,
                                                decimal_places=2,
                                                min_value=-1000,
                                                max_value=1000,
                                                command=lambda: set_window_scaling(window_scaling_button.get()))
            window_scaling_button.pack()

        save_devices_button = ctk.CTkButton(master=bottom_frame, height=40, width=120, text="Set Scaling", command=new_window)
        save_devices_button.grid(pady=30, sticky="e")

        bottom_frame.grid_columnconfigure((0), weight=1)


        self.grid_columnconfigure(0, weight=0)  # Do not expand left_frame column
        self.grid_columnconfigure(1, weight=1)  # Allow right_frame column to expand
        self.grid_rowconfigure(0, weight=1)     # Allow right_frame row to expand
        self.grid_rowconfigure(1, weight=0)     # Keep bottom_frame from expanding vertically

        def start_window_creation():
            threading.Thread(target=self.create_windows).start()

        self.after(10, start_window_creation())



    def create_windows(self):

        for i in self.user_devices_and_configs.user_devices.values():
            for j in i.config_ids:
                if j not in self.edit_windows.keys():
                    self.edit_configuration(configuration_id=j, radio_button=self.devices_frames.device_frame_dict[i.device_id].configuration_frames[j].radio_button, add_to_dictionary=True)
                else:
                    print("already there")
                # radio_button = self.devices_frames.device_frame_dict[device_id].configuration_frames[newest_configuration_id].radio_button
        print("windows created")



    def edit_configuration(self, 
                           configuration_id,
                           radio_button,
                            devices_scrollable_frame=None,
                            create_devices_inner_frame=None,
                            create_and_update_device_dropdown=None,
                            is_new_device=False,
                            is_new_config=False,
                            add_to_dictionary = False
                           ):

        if configuration_id in self.edit_windows.keys():
            self.pack_forget()
            self.edit_windows[configuration_id].pack(fill="both", expand=True)

        else:
            configuration = Classes.DeviceConfig.create_from_configuration_id(configuration_id)
            edit_page = EditConfigFrame(self.master, configuration=configuration, radio_button=radio_button, is_new_config=is_new_config, is_new_device=is_new_device, main_page=self, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame, create_and_update_device_dropdown=create_and_update_device_dropdown, 
                                        front_page=self,
                                        show_main_page=self.show)

            self.edit_windows[configuration_id] = edit_page
            
            if add_to_dictionary == False:
                # self.edit_page = edit_page
                # edit_page.added_to_dict = False
                self.pack_forget()
                edit_page.pack(fill="both", expand=True)
            

    def show(self):
        self.pack(fill="both", expand=True)

    def show_edit_page(self):
        if self.edit_page:
            self.pack_forget()
            self.edit_page.pack(fill="both", expand=True)


class EditConfigFrame(ctk.CTkFrame):
    def __init__(self, master, show_main_page, radio_button,
                   main_page, configuration=None,
                devices_scrollable_frame = None,
                create_devices_inner_frame= None,
                create_and_update_device_dropdown=None,
            is_new_device=False,
            is_new_config=False,
            front_page = None,
            add_action_frame=None
                ):
        super().__init__(master)
        
        self.master = master
        self.show_main_page = show_main_page
        self.configuration = configuration
        self.main_page_radio_button = radio_button
        self.add_action_frame = add_action_frame
        self.front_page = front_page


        """Create the page's frames. Add title to page."""
        self.left_frame_edit_page = ctk.CTkFrame(master=self, fg_color="#2B2B2B")
        self.left_frame_edit_page.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Set the weight of the row in the main frame


        self.edit_page_left_buttons_frame = ctk.CTkFrame(master=self.left_frame_edit_page)
        self.edit_page_left_buttons_frame.grid(row=10, column=0, columnspan=2, sticky="ew", padx=0)



        self.edit_page_scrollable_frame = ctk.CTkScrollableFrame(master=self,)
        self.edit_page_scrollable_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)  

        # self.grid_columnconfigure(2, weight=0)



        # self.edit_page_scrollable_frame = ctk.CTkFrame(master=self.frame111,)
        # self.edit_page_scrollable_frame.grid(row=0, column=1, sticky="nsew")
        # self.edit_page_frame2 = ctk.CTkFrame(master=self.frame111,)
        # self.edit_page_frame2.grid(row=0, column=2, sticky="nsew",
                                #    )

        # label9 = ctk.CTkLabel(master=self.edit_page_frame2, text="edit_page_frame2")
        # label9.pack()








        device_name_label = ctk.CTkLabel(master=self.left_frame_edit_page, text=configuration.device_name, font=ctk.CTkFont( family="Noto Sans", size=36 if len(configuration.device_name) < 15 else 26, ), text_color=gui_variables.primary_colour, pady=(20), corner_radius=0 )
        device_name_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        """Create array to store left buttons, """
        # self.left_buttons_array = []
        self.left_buttons_dictionary = {}
        self.currently_selected_menu = None

        self.frames = {}



        def create_left_buttons(button_text, button_reference):
            created_button = ctk.CTkButton(master=self.edit_page_left_buttons_frame, corner_radius=0, height=40, border_spacing=10, text=button_text, font=ctk.CTkFont(family="Noto Sans",size=18 ), 
                                                
                                                command=lambda c=button_reference: self.left_button_clicked(c),

                                                  fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            
            created_button.pack(fill="x", expand=True)
            self.left_buttons_dictionary[button_reference] = created_button
            if len(self.left_buttons_dictionary) == 1:
                self.left_button_clicked(button_reference)


        if self.configuration.has_scrollwheel == True:
            self.scroll_properties = Classes.ScrollProperties.create_from_configuration_id(configuration.configuration_id)
            self.frames["Scrollwheel"] = VerticalScrollwheelFrame(master_frame=self.edit_page_scrollable_frame, scroll_properties=self.scroll_properties, configuration=self.configuration, )
            self.frames["Scrollwheel"].pack()

            if configuration.has_thumbwheel == True:
                create_left_buttons(button_reference="Scrollwheel", button_text="Vertical Scrollwheel")
                create_left_buttons(button_reference="Thumbwheel", button_text="Thumbwheel")

            else:
                create_left_buttons(button_reference="Scrollwheel", button_text="Scrollwheel")

        if self.configuration.has_thumbwheel == True:
            self.frames["Thumbwheel"] = ThumbwheelFrame(master_frame=self.edit_page_scrollable_frame, scroll_properties=self.scroll_properties, configuration=self.configuration)

        for button in self.configuration.buttons:
            create_left_buttons(button_text=button.button_name, button_reference=button.button_cid)
            self.frames[button.button_cid] = ButtonConfigFrame(edit_config_frame_master = self.master,
                                                                edit_config_frame_instance=self,
                                                                  master_frame=self.edit_page_scrollable_frame, configuration=self.configuration, button=button,
                                                                #   toggle_second_scrollable_frame = self.toggle_second_scrollable_frame,
                                                                #   second_scrollable_frame = self.edit_page_second_scrollable_frame,
                                                                  )


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
                # # TODO: make this target the desired widget more specifically. Now it's
                # for widget in devices_scrollable_frame.winfo_children():
                #     widget.destroy()
                # create_devices_inner_frame()
                self.main_page_radio_button.update_text(config_name_stripped)



        configuration_name_label = ctk.CTkLabel(master=self.left_frame_edit_page,text=" Configuration Name",font=ctk.CTkFont(    family="Noto Sans",    weight="bold",    size=14))
        configuration_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20, 0))

        configuration_name_textbox = ctk.CTkTextbox(master=self.left_frame_edit_page, height=10, width=250, font=ctk.CTkFont(     family="Noto Sans",          size=16 ), corner_radius=1 )
        configuration_name_textbox.grid(row=3, column=0, padx=10)
        configuration_name_textbox.insert("0.0", configuration.configuration_name)
        configuration_name_textbox.bind("<Tab>", focus_next_widget)
        configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)

        dpi_spinbox = IntSpinbox(master=self.left_frame_edit_page, 
                                 db_query=self.configuration.update_dpi,
                                 width=200, step_size=50, min_value=configuration.min_dpi, max_value=configuration.max_dpi, value=configuration.dpi)

        def create_dpi_widgets():
            dpi_label = ctk.CTkLabel( master=self.left_frame_edit_page, text=("DPI"), font=ctk.CTkFont( family="Roboto", size=18, ), )
            dpi_label.grid(row=4, column=0)        
            dpi_spinbox.grid(row=5, column=0)

        create_dpi_widgets()

        
        def update_config_file_name():
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            if len(config_name_stripped) > 0:
                configuration.configuration_name = config_name_stripped
                self.main_page_radio_button.update_text(config_name_stripped)

        self.bottom_frame = ctk.CTkFrame(master=self,fg_color="transparent")
        self.bottom_frame.grid(row=1, column=1)

        back_button = ctk.CTkButton(master=self.bottom_frame, text="Back",command=lambda: [self.go_back(),update_spinboxes_in_db(), update_config_file_name()])
        back_button.pack(pady=20)

        def update_spinboxes_in_db():

            configuration.dpi = dpi_spinbox.get()
            # if configuration.smartshift_support == True:
            #     configuration.smartshift_threshold = smartshift_threshold_spinbox.get()
            #     configuration.smartshift_torque = smartshift_torque_spinbox.get()
            if configuration.has_scrollwheel == True:
                pass
                # self.scroll_properties.scroll_up_threshold = self.frames["Scrollwheel"].scrollwheel_up_spinbox.get()
                # self.scroll_properties.scroll_down_threshold = self.frames["Scrollwheel"].scrollwheel_down_spinbox.get()
            if configuration.has_thumbwheel == True:
                self.scroll_properties.scroll_left_threshold = self.frames["Thumbwheel"].thumbwheel_left_spinbox.get()
                self.scroll_properties.scroll_right_threshold = self.frames["Thumbwheel"].thumbwheel_right_spinbox.get()



    # def button_clicked(self, id_of_clicked_button):
    #     if id_of_clicked_button != self.currently_selected_device:
    #         self.display_device_frame_callback(id_of_clicked_button)
    #         self.button_objects_dict[self.currently_selected_device].configure(fg_color = "transparent")
    #         self.activate_button(device_id_to_activate=id_of_clicked_button)



    def left_button_clicked(self, clicked_menu_item):
        if clicked_menu_item != self.currently_selected_menu:
            # self.display_device_frame_callback(id_of_clicked_button)
            if self.currently_selected_menu is not None:
                # self.left_buttons_dictionary[self.currently_selected]
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
            print("not in dict")
            try:
                self.front_page.edit_windows[self.configuration.configuration_id].destroy()
                del self.front_page.edit_windows[self.configuration.configuration_id]
            except KeyError:
                print("error in deleting")
            self.front_page.edit_windows[self.configuration.configuration_id] = self
        self.pack_forget()
        self.show_main_page()





class KeyPressFrame(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, added_from, **kwargs):
        super().__init__(master, **kwargs)
        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        self.click_box = ctk.CTkButton(master=self)
        self.initialise_clickbox()
        self.click_box.pack(pady=50, padx=50, fill="both", expand=True)
        self.app_root.wm_attributes('-type', 'dialog')

        self.enter_manually_button = ctk.CTkButton(master=self, text="Enter Array Manually", command=self.enter_manually)
        self.enter_manually_button.pack()

    def enter_manually(self):
        self.enter_manually_button.pack_forget()
        textbox = ctk.CTkTextbox(master=self)
        textbox.insert("0.0", "[  ]")
        textbox.pack()
        self.click_box.pack_forget()
        save_manual_button = ctk.CTkButton(master=self, text="Save Manual")

    def initialise_clickbox(self):
        self.click_box.configure(text="Click here to enter keyboard shortcut",
                                       command=self.activate_key_listener,
                                       fg_color="transparent",
                                       hover=False,
                                       border_width=10,
                                       border_color="#363636"
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

        self.click_box.configure(text="Start typing...", command=None, border_color="#198754",)
        self.click_box.focus_set()


    def deactivate_key_listener(self):
        self.app_root.unbind("<KeyPress>")
        self.app_root.unbind("<KeyRelease>")
        self.stop_recording_button.destroy()

        if not hasattr(self, "db_keypress_array"):
            self.initialise_clickbox()
        else:
            self.click_box.configure(border_color="#DC3545")
            self.reset_button = ctk.CTkButton(self, text="Reset", command=self.initialise_clickbox)
            self.reset_button.pack()
            self.save_button = ctk.CTkButton(self, text="Save new shortcut", command=self.save_button_clicked)
            self.save_button.pack()

    def save_button_clicked(self):
        new_primary_key = self.settings_object.add_new_keypress_action(keypresses=json.dumps(self.db_keypress_array))

        if not isinstance(self.added_from, GestureRadioFrame):
            self.origin_frame.create_keypress_radio_button_row(i=new_primary_key)
            self.origin_frame.keypress_radio_buttons_frame.grid(row=2, column=0)
        else:
            self.added_from.create_keypress_radio_button_row(i=new_primary_key)
            self.added_from.keypress_radio_buttons_frame.grid(row=2, column=0)

        self.go_back_function()


    def handle_key_press(self, event):

        db_keymate, gui_keymate = keymates.get_keymates(event.keysym)
        if not hasattr(self, "db_keypress_array"):
            self.db_keypress_array = [db_keymate]            
            self.gui_keypress_array = [gui_keymate]
            self.click_box.configure(text=gui_keymate)
        elif db_keymate not in self.db_keypress_array:
            self.click_box.configure(text=f"{self.click_box._text} {gui_keymate}")
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

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        label=ctk.CTkLabel(master=self, text="Axis")
        label.pack()

        
        rel_list = ["REL_X", "REL_Y", "REL_Z", "REL_RX", "REL_RY", "REL_RZ", "REL_HWHEEL", "REL_DIAL", "REL_WHEEL", "REL_MISC", "REL_RESERVED", "REL_WHEEL_HI_RES", "REL_HWHEEL_HI_RES", "REL_MAX", "REL_CNT"]

        
        axis_dropdown_variable = ctk.StringVar(value="Select Axis")
        axis_dropdown = ctk.CTkOptionMenu(master=self,
                                          variable=axis_dropdown_variable,
                                          values=rel_list,
                                          state="normal",
                                          width=200,
                                          height=36
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
                                        fg_color="#198754", 
                                        font=ctk.CTkFont(size=14, family="Veranda"))
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



class AddCycleDPI(ctk.CTkFrame):
    def __init__(self, master, app_root, settings_object, go_back_function, origin_frame, min_dpi, max_dpi, added_from, **kwargs):
        super().__init__(master, **kwargs)

        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        label=ctk.CTkLabel(master=self, text="CycleDPI")
        label.pack()

        self.spinbox = IntSpinbox(master=self,
                                value=1000,
                                width=200,
                                step_size=100,
                                min_value=min_dpi,
                                max_value=max_dpi
                                )
        self.spinbox.pack()            

        self.add_to_array_button = ctk.CTkButton(master=self, text="Add value to array", command=self.add_value_to_array, text_color="white", text_color_disabled=("#9FA5AB"), fg_color="#198754", font=ctk.CTkFont( size=14, family="Veranda"))
        self.add_to_array_button.pack()

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", state="disabled", command=self.add_new_cycledpi, text_color="white", text_color_disabled=("#9FA5AB"), fg_color="#198754", font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack()

        self.array = []
        self.array_dict = {}
        self.array_label = ctk.CTkLabel(master=self, text=self.array)
        self.array_label.pack()

        self.array_frame = ctk.CTkFrame(master=self)
        self.array_frame.pack()

    def add_to_array_frame(self, value):

        value_frame = ctk.CTkFrame(master=self.array_frame)
        value_frame.grid(row=0, column=value)

        label = ctk.CTkLabel(master=value_frame, text=value)
        label.grid(row=0, column=0)

        remove_button = ctk.CTkButton(master=value_frame, text="X", command=lambda value=value, value_frame=value_frame: self.delete_from_array(value, value_frame))
        remove_button.grid(row=0, column=1)

        if len(self.array) > 1:
            self.save_button.configure(state="enabled")

    def delete_from_array(self, value, value_frame):
        self.array.remove(value)
        value_frame.destroy()
        if len(self.array) < 2:
            self.save_button.configure(state="disabled")


    def add_value_to_array(self):
        value_to_add = self.spinbox.get()
        if value_to_add not in self.array:
            self.array.append(value_to_add)
            self.array = sorted(self.array)
            self.array_label.configure(text=self.array)
            self.add_to_array_frame(value=value_to_add)

    def add_new_cycledpi(self):
        new_primary_key = self.settings_object.add_new_cycledpi(str(self.array))

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

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", command=self.add_new_changedpi, text_color="white", text_color_disabled=("#9FA5AB"), fg_color="#198754", font=ctk.CTkFont( size=14, family="Veranda"))
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
        self.app_root = app_root
        self.origin_frame = origin_frame
        self.settings_object = settings_object
        self.go_back_function = go_back_function
        self.added_from = added_from

        label=ctk.CTkLabel(master=self, text="Host to Toggle")
        label.pack()

        def enable_save_button(x):
            self.save_button.configure(state="normal", fg_color="#198754")
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

        self.save_button = ctk.CTkButton(master=self, text="Save New Action", command=self.add_new_changehost, state="disabled", text_color="white", text_color_disabled=("#9FA5AB"), fg_color=gui_variables.secondary_colour, hover_color=("#28A745"), font=ctk.CTkFont( size=14, family="Veranda"))
        self.save_button.pack()

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
        self.container_frame.pack()

        go_back_button = ctk.CTkButton(master=self.container_frame, text="Cancel", command=self.go_back)
        go_back_button.grid(row=0, column=0)

        options = {}

        options_frame = ctk.CTkFrame(master=self.container_frame)
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



        segemented_button = ctk.CTkSegmentedButton(master=self.container_frame,
                                                            # values=["Keypress", "Value 2", "Value 3"],
                                                            values=[i for i in options.keys()],
                                                            command=segmented_button_callback)
        segemented_button.grid(row=1, column=0)
        segemented_button.set("Keypress")  



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
        super().__init__(*args, **kwargs) 
    
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



        


        add_new_action_button = ctk.CTkButton(master=self, command= lambda: show_new_action_frame(), text="Add New Action")
        add_new_action_button.grid(row=99, column=0)




        if config_object.gesture_nopress is not None:
            radio_buttons_to_create.append(["No Press", config_object.gesture_nopress])
        if config_object.gesture_togglesmartshift is not None:
            radio_buttons_to_create.append(["Toggle Smart Shift", config_object.gesture_togglesmartshift])
        if config_object.gesture_togglehiresscroll is not None:
            radio_buttons_to_create.append(["Toggle Hi Res Scroll", config_object.gesture_togglehiresscroll])



        radio_buttons_frame = ctk.CTkFrame(master=self)
        radio_buttons_frame.grid(row=1, column=0)



        for i,v in enumerate(radio_buttons_to_create):
            radio_button_row = ctk.CTkFrame(master=radio_buttons_frame)
            radio_button_row.grid(row=i, column=0)

            radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=v[0], command=lambda c=v[1]: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            

            if config_object.selected_gesture_id == v[1]:
                radio_button.radio_button_clicked()



            self.radio_buttons_dictionary[v[1]] = radio_button











        self.keypress_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame)
        self.keypress_radio_buttons_frame.grid(row=2, column=0)


        if len(self.config_object.gesture_keypresses) > 0:
            for i in self.config_object.gesture_keypresses.keys():
                self.create_keypress_radio_button_row(i=i)
        else:
            self.keypress_radio_buttons_frame.grid_forget()



        self.changehost_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame)
        self.changehost_radio_buttons_frame.grid(row=4, column=0)

        if len(self.config_object.gesture_changehost) > 0:
            for i in self.config_object.gesture_changehost.keys():
                self.create_changehost_radio_button_row(gesture_id=i)
        else:
            self.changehost_radio_buttons_frame.grid_forget()


        self.axis_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame)
        self.axis_radio_buttons_frame.grid(row=7, column=0)

        if len(self.config_object.gesture_axes) > 0:
            for i in self.config_object.gesture_axes.keys():
                self.create_axes_radio_button_row(gesture_id=i)
        else:
            self.axis_radio_buttons_frame.grid_forget()



        self.changedpi_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame)
        self.changedpi_radio_buttons_frame.grid(row=5, column=0)

        if len(self.config_object.gesture_changedpi) > 0:
            for i in self.config_object.gesture_changedpi.keys():
                self.create_changedpi_radio_button_row(gesture_id=i)
        else:
            self.changedpi_radio_buttons_frame.grid_forget()



        self.cycledpi_radio_buttons_frame = ctk.CTkFrame(master=radio_buttons_frame)
        self.cycledpi_radio_buttons_frame.grid(row=6, column=0)

        if len(self.config_object.gesture_cycledpi) > 0:
            for i in self.config_object.gesture_cycledpi.keys():
                self.create_cycledpi_radio_button_row(gesture_id=i)
        else:
            self.cycledpi_radio_buttons_frame.grid_forget()





    def create_cycledpi_radio_button_row(self, gesture_id):
        cycledpi_button_row = ctk.CTkFrame(master=self.cycledpi_radio_buttons_frame)
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
        changedpi_button_row = ctk.CTkFrame(master=self.changedpi_radio_buttons_frame)
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
        keypress_button_row = ctk.CTkFrame(master=self.keypress_radio_buttons_frame)                
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

        edit_keypress_button = ctk.CTkButton(
                master=keypress_button_row,
                height=20,
                width=80,
                text="Edit",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                # command=
        )
        edit_keypress_button.grid(row=0, column=2, pady="5", sticky="e")

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
        changehost_button_row = ctk.CTkFrame(master=self.changehost_radio_buttons_frame)
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
                command=lambda c=gesture_id, f=changehost_button_row, : self.changehost_deletion_warning(c, f,)
        )
        delete_changehost_button.grid(row=0, column=3, pady="5", sticky="e")

        changehost_button_row.columnconfigure(1, weight=2)



    def create_axes_radio_button_row(self, gesture_id):
        axis_button_row = ctk.CTkFrame(master=self.axis_radio_buttons_frame)
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


        self.container_frame = ctk.CTkFrame(master=self)
        self.container_frame.pack(fill="both", expand="true")

        self.gesture_dict = button.gesture_dict


        button_label2 = ctk.CTkLabel(master=self.container_frame, text = f"{f"GESTURES HERE"} ({button.button_cid})")
        button_label2.grid(row=0, column=0)

        self.currently_selected_menu = "Up"
        def segmented_button_callback(value):
            self.gesture_radio_frames[self.currently_selected_menu].grid_forget()
            self.gesture_radio_frames[value].grid(row=2, column=0)
            self.currently_selected_menu = value


        segemented_button = ctk.CTkSegmentedButton(master=self.container_frame,
                                                            values=[i for i in self.gesture_dict.keys()],
                                                            command=segmented_button_callback)
        segemented_button.grid(row=1, column=0)
        segemented_button.set("Up")

        self.gesture_radio_frames = {}

        for i in self.gesture_dict:
            self.gesture_radio_frames[i] = GestureRadioFrame(master=self.container_frame, config_object=self.gesture_dict[i], container_outer_frame=container_outer_frame, master_frame=master_frame, edit_config_frame_instance=edit_config_frame_instance, configuration=configuration, edit_config_frame_master=edit_config_frame_master)

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
        self.container_frame.grid(row=0, column=0)


    





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

        self.container_frame2 = GestureFrame(master=self.container_outer_frame, button=self.button, container_outer_frame=self.container_outer_frame, master_frame=self.master_frame, edit_config_frame_instance=self.edit_config_frame_instance, 
                                             configuration=self.configuration, edit_config_frame_master=self.edit_config_frame_master, corner_radius=0, fg_color="transparent")
        self.container_frame2.grid(row=0, column=1)



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
        if button.button_gestures is not None:
            radio_buttons_to_create.append(["Gestures", button.button_gestures])

        radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        radio_buttons_frame.grid(row=1, column=0)



        for i,v in enumerate(radio_buttons_to_create):
            radio_button_row = ctk.CTkFrame(master=radio_buttons_frame)
            radio_button_row.grid(row=i, column=0)

            radio_button = MatthewsRadioButton(master=radio_button_row, width=600, text=v[0], command=lambda c=v[1]: self.select_configuration(c))
            radio_button.grid(row=0, column=0)            

            if button.selected_button_config_id == v[1]:
                radio_button.radio_button_clicked()



            self.radio_buttons_dictionary[v[1]] = radio_button


        self.keypress_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        self.keypress_radio_buttons_frame.grid(row=2, column=0)


        if len(button.button_keypresses) > 0:
            for i in button.button_keypresses.keys():
                self.create_keypress_radio_button_row(i=i)
        else:
            self.keypress_radio_buttons_frame.grid_forget()

        self.changehost_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        self.changehost_radio_buttons_frame.grid(row=4, column=0)

        if len(button.button_changehost) > 0:
            for i in button.button_changehost.keys():
                self.create_changehost_radio_button_row(button_config_id=i)
        else:
            self.changehost_radio_buttons_frame.grid_forget()


        self.changedpi_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        self.changedpi_radio_buttons_frame.grid(row=5, column=0)

        if len(button.button_changedpi) > 0:
            for i in button.button_changedpi.keys():
                self.create_changedpi_radio_button_row(button_config_id=i)
        else:
            self.changedpi_radio_buttons_frame.grid_forget()



        self.cycledpi_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        self.cycledpi_radio_buttons_frame.grid(row=6, column=0)

        if len(button.button_cycledpi) > 0:
            for i in button.button_cycledpi.keys():
                self.create_cycledpi_radio_button_row(button_config_id=i)
        else:
            self.cycledpi_radio_buttons_frame.grid_forget()


        self.axis_radio_buttons_frame = ctk.CTkFrame(master=self.container_frame)
        self.axis_radio_buttons_frame.grid(row=7, column=0)

        if len(button.button_axes) > 0:
            for i in button.button_axes.keys():
                self.create_axes_radio_button_row(button_config_id=i)
        else:
            self.axis_radio_buttons_frame.grid_forget()


        # self.gestures_label = ctk.CTkLabel(master=self.container_frame, text="Here are the gestures")
        # self.gestures_label.grid(row=0, column=1)



    def create_cycledpi_radio_button_row(self, button_config_id):
        cycledpi_button_row = ctk.CTkFrame(master=self.cycledpi_radio_buttons_frame)
        cycledpi_button_row.pack()

        radio_button = MatthewsRadioButton(master=cycledpi_button_row, width=600, text=f"cycledpi {self.button.button_cycledpi[button_config_id].dpi_array}", command=lambda c=button_config_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

        if self.button.selected_button_config_id == button_config_id:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[button_config_id] = radio_button

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
                command=lambda c=button_config_id, f=cycledpi_button_row, : self.cycledpi_deletion_warning(c, f,)
        )
        delete_cycledpi_button.grid(row=0, column=3, pady="5", sticky="e")

        cycledpi_button_row.columnconfigure(1, weight=2)



    def create_changehost_radio_button_row(self, button_config_id):
        changehost_button_row = ctk.CTkFrame(master=self.changehost_radio_buttons_frame)
        changehost_button_row.pack()

        radio_button = MatthewsRadioButton(master=changehost_button_row, width=600, text=f"Changehost {self.button.button_changehost[button_config_id].host_change}", command=lambda c=button_config_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

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
                command=lambda c=button_config_id, f=changehost_button_row, : self.changehost_deletion_warning(c, f,)
        )
        delete_changehost_button.grid(row=0, column=3, pady="5", sticky="e")

        changehost_button_row.columnconfigure(1, weight=2)



    def create_axes_radio_button_row(self, button_config_id):
        axis_button_row = ctk.CTkFrame(master=self.axis_radio_buttons_frame)
        axis_button_row.pack()

        radio_button = MatthewsRadioButton(master=axis_button_row, width=600,
                                            text=f"Axis {self.button.button_axes[button_config_id].axis_button}: {self.button.button_axes[button_config_id].axis_multiplier}",
                                             command=lambda c=button_config_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")

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
        delete_axis_button.grid(row=0, column=3, pady="5", sticky="e")

        axis_button_row.columnconfigure(1, weight=2)


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



    def create_axes_radio_button_row(self, button_config_id):
        axis_button_row = ctk.CTkFrame(master=self.axis_radio_buttons_frame)
        axis_button_row.pack()

        radio_button = MatthewsRadioButton(master=axis_button_row, width=600,
                                            text=f"Axis {self.button.button_axes[button_config_id].axis_button}: {self.button.button_axes[button_config_id].axis_multiplier}",
                                             command=lambda c=button_config_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")

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
        delete_axis_button.grid(row=0, column=3, pady="5", sticky="e")

        axis_button_row.columnconfigure(1, weight=2)


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



    def create_changedpi_radio_button_row(self, button_config_id):
        changedpi_button_row = ctk.CTkFrame(master=self.changedpi_radio_buttons_frame)
        changedpi_button_row.pack()

        radio_button = MatthewsRadioButton(master=changedpi_button_row, width=600, 
                                           text=f"Changedpi {self.button.button_changedpi[button_config_id].increment}",
                                             command=lambda c=button_config_id: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")

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
        delete_changedpi_button.grid(row=0, column=3, pady="5", sticky="e")

        changedpi_button_row.columnconfigure(1, weight=2)


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




    def changehost_deletion_warning(self, c, f):
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
            self.button.delete_changehost(button_config_id=c)
            f.destroy()
            if len(self.button.button_changehost) == 0:
                self.changehost_radio_buttons_frame.grid_forget()


    def create_keypress_radio_button_row(self, i):     
        keypress_button_row = ctk.CTkFrame(master=self.keypress_radio_buttons_frame)                
        keypress_button_row.pack()

        radio_button = MatthewsRadioButton(master=keypress_button_row, width=300, 
                                        #    text=f"Keypress",
                                           text=f"Keypress: {self.button.button_keypresses[i].keypresses[0:29]}",
                                            #  font=ctk.CTkFont(family="Noto Sans", size=12),
                                               command=lambda c=i: self.select_configuration(c))
        radio_button.grid(row=0, column=0, sticky="w")            

        if self.button.selected_button_config_id == i:
            radio_button.radio_button_clicked()

        self.radio_buttons_dictionary[i] = radio_button

        edit_keypress_button = ctk.CTkButton(
                master=keypress_button_row,
                height=20,
                width=80,
                text="Edit",
                fg_color="transparent",
                # border_color="red",
                font=ctk.CTkFont(family="Noto Sans"),
                text_color="#6C757D",
                border_color="#6C757D",
                hover_color="#450C0F",
                border_width=1,
                corner_radius=2,
                # command=
        )
        edit_keypress_button.grid(row=0, column=2, pady="5", sticky="e")

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

    def select_configuration(self, button_configuration_id):
        if button_configuration_id == self.button.button_gestures:
            self.container_frame2.container_frame.pack()
        else:
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
        self.container_outer_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_outer_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_outer_frame.destroy(*args, **kwargs)




class MiddleButtons():
    def __init__(self, master_frame, button_dictionary, display_frame_callback, currently_selected_menu=None):
        self.master_frame = master_frame
        self.button_dictionary = button_dictionary
        self.display_frame_callback = display_frame_callback
        self.currently_selected_menu = currently_selected_menu

        self.setup_middle_buttons()

    def setup_middle_buttons(self):
        for i in self.button_dictionary.keys():
            pass


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
        """
        Allows DeviceFrame to be packed like a regular widget.
        Passes all arguments to its container_frame's pack method.
        """
        self.container_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)
class CentreButtonFrame():
    def __init__(self, master_frame, configuration, **kwargs):
        super().__init__(**kwargs)
        
        self.master_frame = master_frame
        self.configuration = configuration 
        self.currently_selected_button = None
        self.button_dictionary = {}
        self.container_frame = ctk.CTkFrame(master=master_frame)
        self.container_frame.grid(row=0, column=0)
        self.test_label = ctk.CTkLabel(master=master_frame, text = "Test Label")
        # thumbwheel_frame_label = ctk.CTkLabel(master=self.container_frame,)
        self.test_label.grid(row=0, column=0, columnspan=2)

    def init_buttons(self):
        pass


    def pack(self, *args, **kwargs):
        self.master_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.master_frame.pack_forget(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.master_frame.grid(*args, **kwargs)

    def grid_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.master_frame.grid_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)

class VerticalScrollwheelFrame():
    def __init__(self, master_frame, scroll_properties, configuration): 
        self.master_frame = master_frame
        self.configuration = configuration
        self.scroll_properties = scroll_properties


        self.container_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        self.container_frame.pack_forget()


        self.test_label2 = ctk.CTkLabel(master=master_frame, text = "Test Label2")


        # # self.center_frame = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color="transparent")
        # # self.center_frame.grid(row=0, column=0)

        # centre_frame = CentreButtonFrame(
        #     master_frame=self.container_frame,
        #     # master_frame=self.container_frame,

        #       configuration=configuration)
        # centre_frame.grid(row=10, column=10)
        # # centre_frame.grid_forget()




        if configuration.smartshift_support == True:

            smartshift_options_label = ctk.CTkLabel(master=self.container_frame, text=("SmartShift Options"), font=ctk.CTkFont( family="Roboto", size=18, ), )
            smartshift_options_label.grid(row=3, column=0, padx=(10,0), pady=(30,0), sticky="w")
            smartshift_frame = ctk.CTkFrame(master=self.container_frame)
            smartshift_frame.grid(row=4, column=0, sticky="ew")
            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = ctk.CTkCheckBox(master=smartshift_frame, text="SmartShift On", command=lambda: setattr(configuration, 'smartshift_on', check_var.get()), variable=check_var, onvalue=True, offvalue=False)
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
                                    db_query=configuration.update_smartshift_threshold,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    value=configuration.smartshift_threshold
                                    )
            
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
                                                   db_query=configuration.update_smartshift_torque,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    value=configuration.smartshift_torque
                                    )
            
            smartshift_torque_spinbox.set(configuration.smartshift_torque) #TODO: Update
            smartshift_torque_spinbox.grid(row=1, column=2)
            







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
        """
        Allows DeviceFrame to be packed like a regular widget.
        Passes all arguments to its container_frame's pack method.
        """
        self.container_frame.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs): # Same as pack method above, but for pack_forget
        self.container_frame.pack_forget(*args, **kwargs)

    def destroy(self, *args, **kwargs): # As above
        self.container_frame.destroy(*args, **kwargs)











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
            self.add_device_dropdown.destroy()
            button_for_adding_devices.configure(state="disabled",
                                                #  fg_color=("#545B62"),
                                                fg_color=gui_variables.secondary_colour
                                                 )
            new_configuration_id, new_device_id = execute_db_queries.add_new_device(self.selected_device)

            


            # TODO: Update this to get the number of possible devices from the DB and use this as the reference for the geometry position
            new_index = 4 + new_device_id
            
            create_left_buttons(self.selected_device, new_device_id, new_index)

            user_configurations[new_configuration_id] = Classes2.get_new_device_config(new_configuration_id=new_configuration_id)

            user_devices[new_device_id] = Classes2.get_new_user_device(new_device_id, self.selected_device, new_configuration_id)            




            create_device_frames(user_devices[new_device_id])
            # testfunc

            create_and_update_device_dropdown()



        def delete_buttons_function():
            for i in device_frames.values():
                i.pack_forget()
            for i in left_buttons.values():
                i.destroy()
            user_devices, user_configurations = Classes2.get_devices_and_configs()
            for i, (k, v) in enumerate(user_devices.items()):
                # v.destroy()
                # create_device_frames(v)
                create_left_buttons(device_name=v.device_name, device_id=v.device_id, index=i)

            


            if len(user_devices) > 0:
                the_current_device = list(device_frames.keys())[0]
                device_frames[the_current_device].pack(fill="both", expand=True)
                try:

                    left_buttons[the_current_device].configure(fg_color = "gray25")
                except:
                    pass
                self.current_device = the_current_device
            else:
                placeholder_device_frame.pack(fill="both", expand=True)
            





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
        


        user_devices_label = ctk.CTkLabel(
            master=left_frame,
            text="User Devices",
            font=ctk.CTkFont(
                family="Noto Sans",
                weight="bold",
                size=20
            ),
            # text_color=gui_variables.primary_colour
        )

        user_devices_label.grid(row=2, column=0, columnspan=2, pady=(30,0))




    





        device_frames = {}
        self.current_device = None
        left_buttons = {}
        self.selected_configurations = {}
        config_radio_buttons = {}


        delete_buttons_button = ctk.CTkButton(master=left_frame,
                                               command=delete_buttons_function
                                               )
        delete_buttons_button.grid(row=0, column = 4)







        def create_device_frames(device):


            this_frame = ctk.CTkFrame(master=devices_frame, corner_radius=0, fg_color="transparent")
            frame_title = ctk.CTkLabel(master=this_frame, text=device.device_name, font=ctk.CTkFont(
                family="Roboto",
                size=60,
            ),

                text_color="gray50"
            )
            frame_title.pack(fill="x", expand=False, pady=20)

            device_options_frame = ctk.CTkFrame(master=this_frame, corner_radius=0, fg_color="transparent",)
            device_options_frame.pack(fill="x", expand=False)


            def add_new_configuration(device_id, device_name):
                newest_configuration_id = execute_db_queries.new_empty_configuration(device_id, device_name)

                self.edit_configuration(configuration_id=newest_configuration_id,
                                                            #  devices_scrollable_frame,
                                                            #    create_devices_inner_frame
                                                               )

                create_device_frames(device)
                this_frame.pack_forget()


                # this_frame.pack()
                # self.edit_configuration(configuration_id = newest_configuration_id, is_new_config=True, devices_scrollable_frame=devices_scrollable_frame, create_devices_inner_frame=create_devices_inner_frame)
                # for widget in devices_scrollable_frame.winfo_children():
                #     widget.destroy()
                # create_devices_inner_frame()



            new_configuration_button = ctk.CTkButton(master=device_options_frame,
                                                        text="Add Device Configuration",
                                                        text_color="white",
                                                        fg_color="#198754",
                                                        height=40,
                                                        width=230,
                                                        hover_color="#28A745",
                                                        font=ctk.CTkFont(family="Noto Sans"),
                                                    #  corner_radius=3,
                                                    #  border_width=2,
                                                        command=lambda d=device.device_id, n=device.device_name: add_new_configuration(d, n))
            new_configuration_button.grid(row=0, column=1, sticky="e",
                                        #   padx=15
                                            )



            # TODO: fix dropdown being added twice to page upon clicking button
            # TODO: fix button highlight on left not being added to page on button click
            delete_device_button = ctk.CTkButton(master=device_options_frame,
                                                    text="Delete Device",
                                                fg_color="#DC3545",
                                                height=40,
                                                width=150,
                                                hover_color="red",
                                                font=ctk.CTkFont(family="Noto Sans"),
                                                command=lambda d=device.device_id: device_deletion_warning(d)
                                                    )
            delete_device_button.grid(row=0, column=2, sticky="e",
                                        padx=(25, 15))

            device_options_frame.columnconfigure((0), weight=1)

            device_options_frame.columnconfigure((1), weight=2)





            radio_button_frame = ctk.CTkFrame(master=this_frame)
            radio_button_frame.pack(fill="x", expand=False)



            def select_configuration(configuration_id):
                old_selected = self.selected_configurations[device.device_id]
                if config_radio_buttons.get(old_selected) is not None:
                    config_radio_buttons[old_selected].another_button_clicked()
                self.selected_configurations[device.device_id] = configuration_id
                device.selected_config = configuration_id


            

            for i, v in enumerate(device.config_ids):

                config_row_frame = ctk.CTkFrame(master=radio_button_frame)
                config_row_frame.pack()

                radio_button = MatthewsRadioButton(master=config_row_frame, width=600, text=user_configurations[v].configuration_name, command=lambda c=v: select_configuration(c))
                if device.selected_config == v:
                    self.selected_configurations[device.device_id] = v
                    radio_button.radio_button_clicked()
                config_radio_buttons[v] = radio_button
                radio_button.grid(row=0, column=0)

                duplicate_configuration_button = ctk.CTkButton(
                    master=config_row_frame,
                    height=20,
                    width=80,
                    fg_color="transparent",
                    # text_color="#198754",
                    font=ctk.CTkFont(family="Noto Sans"),
                    text_color="#6C757D",
                    border_color="#6C757D",
                    border_width=1,
                    # hover_color="#113A1B",
                    corner_radius=2,
                    text=" Copy",
                    # command=lambda: self.edit_configuration(configuration.configuration_id, devices_scrollable_frame, create_devices_inner_frame)
                )
                duplicate_configuration_button.grid(row=0, column=1, sticky="e", padx=15)


                edit_configuration_button = ctk.CTkButton(
                    master=config_row_frame,
                    height=20,
                    width=80,
                    fg_color="transparent",
                    # text_color="#198754",
                    font=ctk.CTkFont(family="Noto Sans"),
                    text_color="#6C757D",
                    border_color="#6C757D",
                    border_width=1,
                    hover_color="#113A1B",
                    corner_radius=2,
                    text=" Edit",
                    command=lambda v=v: self.edit_configuration(configuration_id=v,
                                                            #  devices_scrollable_frame,
                                                            #    create_devices_inner_frame
                                                               )
                )
                edit_configuration_button.grid(row=0, column=2, sticky="e")

                delete_configuration_button = ctk.CTkButton(
                    master=config_row_frame,
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
                    # border_spacing=5,
                    # command=lambda c=configuration.configuration_id, f=config_frame, s=configuration.is_selected: configuration_deletion_warning(c, f, s)
                    command=lambda c=v, f=config_row_frame, d=device.device_id: configuration_deletion_warning(c, f, d)
                )
                delete_configuration_button.grid(row=0, column=3, padx="15", pady="5", sticky="e")
                radio_button_frame.columnconfigure(1, weight=2)
                # config_frame.columnconfigure(2, weight=1)



            this_frame.pack_forget()
            device_frames[device.device_id] = this_frame


        def display_device_frame(device_id):
            if device_id == self.current_device:
                pass
            else:
                try:
                    # TODO: Fix this
                    device_frames[self.current_device].pack_forget()
                except:
                    pass
                left_buttons[device_id].configure(fg_color = "gray25")
                try:
                    left_buttons[self.current_device].configure(fg_color = "transparent")
                except:
                    pass
                device_frames[device_id].pack(fill="both", expand=True)
                self.current_device = device_id

        def create_left_buttons(device_name, device_id, index):
            device_button = ctk.CTkButton(
            master=left_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=device_name,
            font=ctk.CTkFont(
                family="Noto Sans",
                size=18
            ),
            command=lambda d=device_id: display_device_frame(d),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
    )
            left_buttons[device_id] = device_button
            # device_button.grid(row=index + 3, column=0, columnspan=2, sticky="ew", padx=5)
            calculated_row = 4 + device_id
            device_button.grid(row=calculated_row, column=0, columnspan=2, sticky="ew", padx=5)


        user_devices, user_configurations = Classes2.get_devices_and_configs()

        
        for i, (k, v) in enumerate(user_devices.items()):
            create_device_frames(v)
            create_left_buttons(device_name=v.device_name, device_id=v.device_id, index=i)

        if len(user_devices) > 0:
            current_device = list(device_frames.keys())[0]
            device_frames[current_device].pack(fill="both", expand=True)
            left_buttons[current_device].configure(fg_color = "gray25")
            self.current_device = current_device
        else:
            placeholder_device_frame.pack(fill="both", expand=True)
            



























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















            # def select_configuration(configuration_id):
            #     old_selected = self.selected_configurations[device.device_id]
            #     if config_radio_buttons.get(old_selected) is not None:
            #         config_radio_buttons[old_selected].another_button_clicked()
            #     self.selected_configurations[device.device_id] = configuration_id
            #     device.selected_config = configuration_id


        # device_frames = {}
        # self.current_device = None
        # left_buttons = {}
        # self.selected_configurations = {}
        # config_radio_buttons = {}

        # def configuration_deletion_warning(configuration_id, config_frame, is_selected):
        def configuration_deletion_warning(configuration_id, config_frame, device_id):
            # config_frame.destroy()


            msg = CTkMessagebox(title="Delete Configuration?",
                                message="Delete configuration?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
            if msg.get() == "Delete":
                # config_frame.destroy()
                execute_db_queries.delete_configuration(configuration_id)
                config_frame.destroy()
                if self.selected_configurations[device_id] == configuration_id:

                    self.main_page.destroy()
                    # self.main_page = MainPage(self.master)
                    # self.main_page.pack()

                    #                 if device.selected_config == v:
                    # self.selected_configurations[device.device_id] = v
                    # radio_button.radio_button_clicked()



                    self.selected_configurations[device_id] = execute_db_queries.get_selected_config(device_id)
                    
                    
                    # config_radio_buttons[self.selected_configurations[device_id]].radio_button_clicked()

                    # config_radio_buttons[self.selected_configurations[device_id]].radio_button_clicked()
                    
                    
                    # config_radio_buttons[self.selected_configurations[device_id]].destroy()



                #     if is_selected == True:
                #         devices_inner_frame.destroy()
                #         create_devices_inner_frame()
                #     else:
                #         config_frame.destroy()
                #         execute_db_queries.delete_configuration(configuration_id)




















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











class SplashScreen(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        

        self.label = ctk.CTkLabel(self, text="LogiOpsGUI", font=ctk.CTkFont(family="Noto Sans", size=60), text_color=gui_variables.primary_colour)

        self.label.pack(pady=(300, 50))  

        self.after(10, self.move_label_upwards)

        # Run the loading logic after the SplashScreen has been initialized
        self.after(10, self.start_loading)

    def start_loading(self):
        # Setup main_page in a separate thread
        self.loading_thread = threading.Thread(target=self.prepare_main_page)
        self.loading_thread.start()
        
        # After 2 seconds, check if main_page is ready
        self.after(50, self.check_main_page_ready)

    def prepare_main_page(self):
        # self.main_page = MainPage(self.master)
        # self.main_page.pack_forget()
        self.main_page = FrontPage(self.master)
        self.main_page.pack_forget()

    def check_main_page_ready(self):
        if not self.loading_thread.is_alive():
            self.destroy()
            self.main_page.pack(fill="both", expand=True)
        else:
            # Check again after a short delay if the loading_thread is done
            self.after(100, self.check_main_page_ready)

    def move_label_upwards(self, steps=10):
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


def get_window_and_widget_scaling():
    conn, cursor = execute_db_queries.create_db_connection()
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'window_scaling'""")
    window_scaling = float(cursor.fetchone()[0])
    cursor.execute("""SELECT value FROM UserSettings WHERE key = 'widget_scaling'""")
    widget_scaling = float(cursor.fetchone()[0])
    execute_db_queries.close_without_committing_changes(conn)
    return window_scaling, widget_scaling

def setup_gui(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    window_scaling, widget_scaling = get_window_and_widget_scaling()
    ctk.set_window_scaling(window_scaling)
    ctk.set_widget_scaling(widget_scaling)

    # print(root.winfo_screenwidth())
    # print(root.winfo_screenheight())


    root.geometry("1920x1080")
    root.resizable(True, True)
    root.title("LogiOpsGUI")
    # ctk.DrawEngine.preferred_drawing_method = "circle_shapes"
    ctk.DrawEngine.preferred_drawing_method = "font_shapes"
    # ctk.DrawEngine.preferred_drawing_method = "polygon_shapes"


    front_page = FrontPage(root)
    front_page.pack(fill="both", expand=True)


    # splash = SplashScreen(root)
    # splash.pack(fill="both", expand=True)




def main():
    root = ctk.CTk()
    
    create_app_data.configure_logging()  # Configure logging for the application
    create_app_data.initialise_database()  # Create DB, build required tables and triggers, add devices from DeviceData.py

    setup_gui(root)  # Configure GUI settings and pack main page into window.

    root.mainloop()

if __name__ == "__main__":
    main()







