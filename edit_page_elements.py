import customtkinter as ctk
import gui_variables
import Classes
import execute_db_queries

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
        else:
            config_name_stripped = configuration_name_textbox.get("1.0", "end-1c").strip()
            configuration.configuration_name = config_name_stripped
            configuration_name_textbox.delete("0.0", "end")
            configuration_name_textbox.insert("0.0", config_name_stripped)

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

    configuration_name_textbox.bind("<Tab>", focus_next_widget)
    configuration_name_textbox.bind("<FocusOut>", update_config_name_in_db)