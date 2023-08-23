import customtkinter as ctk
import gui_variables

def create_title_frame(master_frame):
    title_frame = ctk.CTkFrame(master=master_frame,
                                fg_color="transparent")
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
                                text_color=gui_variables.primary_colour,
                                pady=30,
                                anchor='s'
                                )
    app_title.pack()

