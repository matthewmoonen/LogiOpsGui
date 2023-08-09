import customtkinter as ctk
from CTkListbox import *

class MainPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_edit_page):
        super().__init__(master)
        self.master = master

        top_frame = ctk.CTkFrame(master=self)
        top_frame.pack(padx=0, pady=0, fill="x")


        # Create label for devices section
        user_devices_label = ctk.CTkLabel(master=top_frame, 
        text="Your Devices",
        font=ctk.CTkFont(family="Roboto", size=24),
        padx=20,
        pady=20
        )
        user_devices_label.grid(row=0, column=0, padx=20, pady=20)

        button_for_adding_devices = ctk.CTkButton(master=top_frame,
                                        height=40,
                                        width=120,
                                        state="disabled",
                                        text="Add Device",
                                        text_color_disabled=("#9FA5AB"),
                                        fg_color=("#545B62"),
                                        hover_color=("#28A745"))
                                        # command=lambda: add_button_clicked('Select Device To Add'))
        button_for_adding_devices.grid(row=0, column=3)


        def create_and_update_device_dropdown():

            options = ['one', 'two', 'three', 'four']
            # options = execute_db_queries.get_unconfigured_devices()
            # print(options)
            

            selected_option_var = ctk.StringVar(value='Select Device To Add')
            add_device_dropdown = ctk.CTkOptionMenu(master=top_frame,
                                                    variable=selected_option_var,
                                                    values=options,
                                                    state="normal",
                                                    width=400,
                                                    height=36,
                                                    command=device_dropdown)
            add_device_dropdown.grid(row=0,
                                    column=2,
                                    padx=20,
                                    pady=20)


        def device_dropdown(new_device):
            button_for_adding_devices.configure(state="normal")
            button_for_adding_devices.configure(fg_color="#208637")
            # button_for_adding_devices.configure(command=lambda: on_button_click(new_device))  # Update button command with selected option
            button_for_adding_devices.configure(command=lambda: add_button_clicked(new_device))  # Update button command with selected option
            # button_for_adding_devices.configure(command=lambda: add_new_entry_and_click(new_device))  # Update button command with selected option


        def add_button_clicked(selected_option):
            button_for_adding_devices.configure(state="disabled", fg_color=("#545B62"))
            # current_datetime = int(time.time() * 1e9)
            switch_to_edit_page()
            print(f"logic for adding {selected_option} to the DB goes here")

        create_and_update_device_dropdown()




        # self.label = ctk.CTkLabel(self, text="Page 1: List of Entries")
        # self.label.pack(pady=10)

        # self.entries_listbox = CTkListbox(self)
        # self.entries_listbox.pack(pady=5)

        self.new_entry_button = ctk.CTkButton(self, text="Add New Entry", command=switch_to_edit_page)
        self.new_entry_button.pack(pady=5)

class EditPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_main_page):
        super().__init__(master)
        self.master = master

        self.label = ctk.CTkLabel(self, text="Page 2: Input fields for New Entry Content")
        self.label.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back to Page 1", command=switch_to_main_page)
        self.back_button.pack(pady=5)

def setup_gui(root, switch_to_main_page, switch_to_edit_page):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.geometry("1000x800")
    root.resizable(True, True)

    main_page = MainPage(root, switch_to_edit_page)
    edit_page = EditPage(root, switch_to_main_page)

    return main_page, edit_page

def main():
    root = ctk.CTk()

    def show_main_page():
        main_page.pack(padx=0, pady=0, fill="both")
        edit_page.pack_forget()

    def show_edit_page():
        main_page.pack_forget()
        edit_page.pack(padx=0, pady=0, fill="both")

    main_page, edit_page = setup_gui(root, show_main_page, show_edit_page)

    show_main_page()

    root.mainloop()

if __name__ == "__main__":
    main()
