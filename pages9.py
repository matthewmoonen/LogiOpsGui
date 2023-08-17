import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
import create_app_data
import execute_db_queries
import LogitechDeviceData

class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.text_entry = tk.Entry(self)
        self.okay_button = tk.Button(self, text="OKAY", command=self.open_edit_page)
        
        self.text_entry.pack()
        self.okay_button.pack()
        
        self.dynamic_label = tk.Label(self, text="Dynamic Label")
        self.dynamic_label.pack()

    def open_edit_page(self):
        self.pack_forget()
        edit_page = EditPage(self.master, self.text_entry.get(), self)
        edit_page.pack()

    def show(self):
        self.pack()

    def update_label(self, new_text):
        self.dynamic_label.config(text=new_text)

class EditPage(ctk.CTkFrame):
    def __init__(self, master, text, main_page):
        super().__init__(master)
        self.main_page = main_page
        self.text = text
        
        self.label = tk.Label(self, text=text)
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        
        self.new_text_entry = tk.Entry(self)
        self.update_button = tk.Button(self, text="Update Label", command=self.update_main_label)
        
        self.label.pack()
        self.back_button.pack()
        self.new_text_entry.pack()
        self.update_button.pack()

    def go_back(self):
        self.pack_forget()
        self.main_page.show()

    def update_main_label(self):
        new_text = self.new_text_entry.get()
        self.main_page.update_label(new_text)

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
    main_page = MainPage(root)
    main_page.show()
    root.mainloop()

if __name__ == "__main__":
    main()
