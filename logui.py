import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkListbox import *
import create_app_data
import execute_db_queries
import LogitechDeviceData



# primary_colour = "#1F538D"
# primary_colour = "#7FC4E7"
primary_colour = "#3A9EE9"
secondary_colour = "#363636"

class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.edit_page = None
        self.selected_device = None

        def create_title_frame():
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
                                        text_color=primary_colour,
                                        pady=30,
                                        anchor='s'
                                        )
            app_title.pack()

        create_title_frame()

        top_frame = ctk.CTkFrame(master=self, fg_color="transparent")
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

    



        self.device_name_label = ctk.CTkLabel(master=self,
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
        self.device_name_label.pack()






        
        



        self.general_device_label = ctk.CTkLabel(
                                            master=self,
                                            text=("Device Settings:"),
                                            font=ctk.CTkFont(
                                                    family="Roboto",
                                                    weight="bold",
                                                    size=22,
                                                    ),
                                                    # text_color="#1F538D",
                                    # pady=30,
                                    # anchor='s'
                                            )
        self.general_device_label.pack()


        if device_attributes._smartshift_support == True:
            self.smartshift_label = ctk.CTkLabel(
                                            master=self,
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
            self.smartshift_label.pack()


            # Create threshold input
            threshold_value = tk.StringVar(value="30")  # Default value for threshold
            threshold_label = ttk.Label(master=self, text="Threshold")
            threshold_label.pack()
            # threshold_label.grid(row=0, column=1, padx=5, pady=5)
            threshold_spinbox = ttk.Spinbox(master=self, from_=0, to=255, textvariable=threshold_value, validate="key")
            # threshold_spinbox.grid(row=0, column=2, padx=5, pady=5)
            threshold_spinbox.pack()



            def checkbox_event():
                print("checkbox toggled, current value:", check_var.get())

            check_var = ctk.StringVar(value="on")
            checkbox = ctk.CTkCheckBox(self, text="CTkCheckBox", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off",
                                     checkbox_height=30,
                                     checkbox_width=30,
                                     corner_radius=0,
                                     border_width=3,
                                     )
            checkbox.pack()
            # def segmented_button_callback(value):
            #     print("segmented button clicked:", value)

            # segemented_button = ctk.CTkSegmentedButton(self, values=["Value 1", "Value 2", "Value 3"],
                                                       
            #                                                     command=segmented_button_callback)
            # segemented_button.set("Value 1")
            # segemented_button.pack()




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
