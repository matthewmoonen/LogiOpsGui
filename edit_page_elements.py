import customtkinter as ctk
import gui_variables

def create_name_device_label(master_frame, edit_page_title):

    device_name_label = ctk.CTkLabel(master=master_frame,
                                            text=edit_page_title,
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


def device_configuration_widgets(master_frame, configuration):


    configuration_name_label = ctk.CTkLabel(master=master_frame,
                                            text="Configuration Name",
                                            )
    configuration_name_label.pack()

    configuration_name_textbox = ctk.CTkTextbox(master=master_frame,
                                                height=10,
                                                width=500,
                                                corner_radius=1
                                                )
    configuration_name_textbox.pack()

    configuration_name_textbox.insert("0.0", configuration.configuration_name)



    configuration_name_var = configuration_name_textbox.get(0.0, "end")
    print(configuration_name_var)