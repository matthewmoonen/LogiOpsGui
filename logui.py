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
import Classes2
from CTkMessagebox import CTkMessagebox




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



        # Create a dictionary to store UI elements by configuration ID
        config_ui_elements = {}
        device_ui_elements = {}

        def create_config_ui(device, configuration):
            # Create the UI elements
            radio_button = ctk.CTkRadioButton(master=devices_frame,
                                            text=f"{configuration.configuration_id}: {configuration.configuration_name}",
                                            variable=selected_configurations[device],
                                            value=configuration.configuration_id,
                                            command=lambda c=configuration: select_configuration(c),
                                            radiobutton_width=24,
                                            radiobutton_height=24,
                                            corner_radius=10,
                                            border_width_unchecked=6,
                                            border_width_checked=9,
                                            hover_color=gui_variables.primary_colour
                                            )

            edit_configuration_button = ctk.CTkButton(
                master=devices_frame,
                height=40,
                width=120,
                text="Edit Configuration",
                command=lambda: self.edit_configuration(configuration.configuration_id)
            )

            delete_configuration_button = ctk.CTkButton(
                master=devices_frame,
                height=40,
                width=120,
                text="Delete Configuration",
                command=lambda c=configuration.configuration_id: config_deletion_warning(c)
            )

            # Pack the UI elements
            radio_button.pack()
            if configuration.is_selected:
                radio_button.select()
            edit_configuration_button.pack()
            delete_configuration_button.pack()

            # Store UI elements in the dictionary
            config_ui_elements[configuration.configuration_id] = {
                "radio_button": radio_button,
                "edit_button": edit_configuration_button,
                "delete_button": delete_configuration_button,
            }

        def config_deletion_warning(configuration_id):
            msg = CTkMessagebox(title="Delete Config?",
                                message="Are you sure you want to delete?",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
            if msg.get() == "Delete":
                execute_db_queries.delete_configuration(configuration_id)
                # Remove the UI elements associated with the deleted configuration
                ui_elements = config_ui_elements.get(configuration_id)
                if ui_elements:
                    ui_elements["radio_button"].destroy()
                    ui_elements["edit_button"].destroy()
                    ui_elements["delete_button"].destroy()


        def create_device_ui(device):

            device_label = ctk.CTkLabel(master=devices_frame,
                                        text=device.device_name,
                                        font=ctk.CTkFont(
                                            family="Roboto",
                                            weight="bold",
                                            size=20,
                                        ),
                                        )
            device_label.pack()
            
            new_configuration_button = ctk.CTkButton(master=devices_frame,
                                                     text="Add New Config",
                                                     command=lambda d=device.device_id, n=device.device_name: add_new_configuration(d, n))
            new_configuration_button.pack()


            delete_device_button = ctk.CTkButton(master=devices_frame,
                                                 text="Delete Device",
                                                command=lambda d=device.device_id: device_deletion_warning(d)
                                                 )
            delete_device_button.pack()

            device_ui_elements[device.device_id] = {
                "device_label": device_label,
                "delete_device_button": delete_device_button,
                "new_configuration_button": new_configuration_button
            }


        def add_new_configuration(device_id, device_name):

            print(f"TODO: make a new configuration for {device_id}")
            execute_db_queries.new_empty_configuration(device_id, device_name)
            
        def device_deletion_warning(device_id):
            msg = CTkMessagebox(title="Delete Device?",
                                message="Deleting device will also delete all its configurations.",
                                option_1="Delete",
                                option_2="Cancel",
                                width=600,
                                height=300,
                                fade_in_duration=200
                                )
            if msg.get() == "Delete":
                # Iterate through devices and configurations to find the device
                for device in user_devices_and_configs:
                    if device.device_id == device_id:
                        # Delete all configurations associated with the device
                        for configuration in device.configurations:
                            execute_db_queries.delete_configuration(configuration.configuration_id)
                            # Remove the UI elements associated with the deleted configuration
                            ui_elements = config_ui_elements.get(configuration.configuration_id)
                            if ui_elements:
                                ui_elements["radio_button"].destroy()
                                ui_elements["edit_button"].destroy()
                                ui_elements["delete_button"].destroy()

                        # Remove the UI elements associated with the deleted device
                        ui_elements = device_ui_elements.get(device_id)
                        if ui_elements:
                            ui_elements["device_label"].destroy()
                            ui_elements["delete_device_button"].destroy()
                            ui_elements["new_configuration_button"].destroy()

                        # Finally, delete the device itself
                        execute_db_queries.delete_device(device_id)
                        break


        user_devices_and_configs = Classes.get_main_page_user_devices()
        selected_configurations = {}

        for device in user_devices_and_configs:
            
            create_device_ui(device)
            
            def select_configuration(configuration):
                execute_db_queries.update_selected_configuration(configuration.configuration_id)

            selected_configurations[device] = ctk.StringVar()

            for configuration in device.configurations:
                # Create and pack UI elements, and store references
                create_config_ui(device, configuration)





























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
                           configuration_id
                           ):

        configuration = Classes.DeviceConfig.create_from_configuration_id(configuration_id)



        self.edit_page = EditPage(self.master, configuration=configuration, main_page=self.show)
        
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

        edit_page_elements.device_configuration_widgets(self, configuration)
        print(configuration.configuration_name)









        dpi_label = ctk.CTkLabel(
                                master=self,
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


        dpi_spinbox = IntSpinbox(master=self,
                                width=200,
                                step_size=50,
                                min_value=configuration.min_dpi,
                                max_value=configuration.max_dpi
                                )
        
        dpi_spinbox.set(configuration.dpi) #TODO: Update
        dpi_spinbox.pack()






        print(configuration.smartshift_support)

        if configuration.smartshift_support == True:

            smartshift_options_label = ctk.CTkLabel(
                                    master=self,
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

            def checkbox_event():
                print("checkbox toggled, current value:", check_var.get())

            check_var = ctk.BooleanVar(value=configuration.smartshift_on)
            checkbox = ctk.CTkCheckBox(master=self, text="SmartShift On", command=checkbox_event,
                                                variable=check_var, onvalue=True, offvalue=False)
            checkbox.pack()






            smartshift_options_label = ctk.CTkLabel(
                                    master=self,
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
            

            
            smartshift_threshold_label = ctk.CTkLabel(
                                    master=self,
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
            smartshift_threshold_label.pack()

            smartshift_threshold_spinbox = IntSpinbox(master=self,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    )
            
            smartshift_threshold_spinbox.set(configuration.smartshift_threshold) #TODO: Update
            smartshift_threshold_spinbox.pack()



            smartshift_torque_label = ctk.CTkLabel(
                                    master=self,
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
            smartshift_torque_label.pack()

            smartshift_torque_spinbox = IntSpinbox(master=self,
                                    width=140,
                                    step_size=5,
                                    min_value=1,
                                    max_value=255,
                                    )
            
            smartshift_torque_spinbox.set(configuration.smartshift_torque) #TODO: Update
            smartshift_torque_spinbox.pack()

            # TODO: Smartshift threshold, smartshift torque


        if configuration.hires_scroll_support == True:

            hiresscroll_options_label = ctk.CTkLabel(
                                    master=self,
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

            def hiresscroll_hires_event():
                print("checkbox toggled, current value:", check_var.get())

            hiresscroll_hires_var = ctk.BooleanVar(value=configuration.hiresscroll_hires)
            hirescroll_hires_checkbox = ctk.CTkCheckBox(master=self, text="HiRes Scroll On", command=hiresscroll_hires_event,
                                                variable=hiresscroll_hires_var, onvalue=True, offvalue=False)
            hirescroll_hires_checkbox.pack()


            def hiresscroll_invert_event():
                print("checkbox toggled, current value:", check_var.get())

            hiresscroll_invert_var = ctk.BooleanVar(value=configuration.hiresscroll_invert)
            hirescroll_invert_checkbox = ctk.CTkCheckBox(master=self, text="Scroll Invert", command=hiresscroll_invert_event,
                                                variable=hiresscroll_invert_var, onvalue=True, offvalue=False)
            hirescroll_invert_checkbox.pack()


            def hiresscroll_target_event():
                print("checkbox toggled, current value:", check_var.get())

            hiresscroll_target_var = ctk.BooleanVar(value=configuration.hiresscroll_target)
            hirescroll_target_checkbox = ctk.CTkCheckBox(master=self, text="Scroll target", command=hiresscroll_target_event,
                                                variable=hiresscroll_target_var, onvalue=True, offvalue=False)
            hirescroll_target_checkbox.pack()


        if configuration.has_scrollwheel == True:
            
            if configuration.has_thumbwheel == True:
                scrollwheel_label_text = "Vertical Scrollwheel"
            else:
                scrollwheel_label_text = "Scrollwheel"

            scrollwheel_label = ctk.CTkLabel(
                                    master=self,
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


        if configuration.has_thumbwheel == True:
            thumbwheel_label = ctk.CTkLabel(
                                    master=self,
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

            
            def thumbwheel_divert_event():
                print("checkbox toggled, current value:", check_var.get())

            thumbwheel_divert_var = ctk.BooleanVar(value=configuration.thumbwheel_divert)
            thumbwheel_divert_checkbox = ctk.CTkCheckBox(master=self, text="Thumbwheel Divert", command=thumbwheel_divert_event,
                                                variable=thumbwheel_divert_var, onvalue=True, offvalue=False)
            thumbwheel_divert_checkbox.pack()


            def thumbwheel_invert_event():
                print("checkbox toggled, current value:", check_var.get())

            thumbwheel_invert_var = ctk.BooleanVar(value=configuration.thumbwheel_invert)
            thumbwheel_invert_checkbox = ctk.CTkCheckBox(master=self, text="Thumbwheel Invert", command=thumbwheel_invert_event,
                                                variable=thumbwheel_invert_var, onvalue=True, offvalue=False)
            thumbwheel_invert_checkbox.pack()









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
