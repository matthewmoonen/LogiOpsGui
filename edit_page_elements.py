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


