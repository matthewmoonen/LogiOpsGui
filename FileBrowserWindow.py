import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class ListboxEntry(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def in_focus(self):
        self.configure(border_color="red")
        # self.configure(border_width=10)

    def out_of_focus(self):
        self.configure(border_color="gray10")


class FileScroller(ctk.CTkScrollableFrame):
    def __init__(self, master, input_box, current_path, create_back_button=True):
        super().__init__(master)

        self.current_path = current_path
        self.input_box = input_box
        self.create_controller_frame()
        self.selected_entry = None
        self.buttons = []
        
        self.create_back_button()

        self.create_entries()

    def update_current_path(self):

        pass
    def create_controller_frame(self):
        self.controller_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.controller_frame.pack(fill="both", expand="true")

    def create_button(self, button_text):
        
        button = ListboxEntry(master = self.controller_frame, text=button_text, corner_radius=0, height=10, border_width=2, border_color="gray10", font=ctk.CTkFont(family="Noto Sans",size=16 ), fg_color="gray10", text_color=("gray70"), hover_color=("gray15"), anchor="w")
        button.pack(fill="x", expand=True)
        self.buttons.append(button)

    def create_back_button(self):
        # print(self.current_path.count('/'))
        # if self.current_path
        # FileNotFoundError

        button = ListboxEntry(master = self.controller_frame, text="⤴..", corner_radius=0, height=10, border_width=2, border_color="gray10", font=ctk.CTkFont(family="Noto Sans",size=18 ), fg_color="gray15", text_color=("gray70"), hover_color=("gray20"), anchor="w")
        button.pack(fill="x", expand=True)
        self.buttons.append(button)

    def create_folder_buttons(self, folders):
        for folder in folders:
            self.create_button(button_text=folder)
        
    def create_file_buttons(self, files):
        for file in files:
            self.create_button(button_text=f"  {file}")

    def navigate_down(self, event):
            if self.selected_entry == None:
                self.input_box.delete("0.0", "end")
                if len(self.buttons) == 1:
                    self.buttons[0].in_focus()
                    self.selected_entry = 0
                    self.input_box.insert("0.0", self.buttons[0]._text)
                else:
                    self.buttons[1].in_focus()
                    self.selected_entry = 1
                    self.input_box.insert("0.0", self.current_path + "/" + self.buttons[self.selected_entry]._text.strip())
            elif self.selected_entry == len(self.buttons) - 1:
                if len(self.buttons) == 1:
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", self.current_path)
                    self.selected_entry = None
            else:
                self.buttons[self.selected_entry].out_of_focus()
                self.selected_entry = self.selected_entry + 1
                self.buttons[self.selected_entry].in_focus()
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.current_path + "/" + self.buttons[self.selected_entry]._text.strip())
                

    def navigate_up(self, event):
            if self.selected_entry == None:
                self.input_box.delete("0.0", "end")
                if len(self.buttons) == 1:
                    self.buttons[0].in_focus()
                    self.selected_entry = 0
                    self.input_box.insert("0.0", self.buttons[0]._text)
                else:
                    self.buttons[1].in_focus()
                    self.selected_entry = 1
                    self.input_box.insert("0.0", self.current_path + "/" + self.buttons[self.selected_entry]._text.strip())
            elif self.selected_entry == 0:
                if len(self.buttons) == 1:
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", self.current_path)
                    self.selected_entry = None                    
            elif self.selected_entry == 1:
                self.buttons[1].out_of_focus()
                self.selected_entry = 0
                self.buttons[0].in_focus()
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.buttons[0]._text)
            else:
                self.buttons[self.selected_entry].out_of_focus()
                self.selected_entry = self.selected_entry - 1
                self.buttons[self.selected_entry].in_focus()
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.current_path + "/" + self.buttons[self.selected_entry]._text.strip())

    def create_entries(self):
        folders = []
        files = []
    
        if self.current_path.count('/') == 0:
            self.current_path = "/"
        if len(self.current_path) > 1 and self.current_path[1] == "/":
            self.current_path = self.current_path[1:]
        entries = os.listdir(self.current_path)

        for entry in entries:
            if not entry.startswith('.'): 
                full_path = os.path.join(self.current_path, entry)
                if os.path.isdir(full_path):
                    folders.append(entry)
                else:
                    files.append(entry)
        self.create_folder_buttons(folders)
        self.create_file_buttons(files)

    def folder_selected(self, selected_folder):
        
        self.controller_frame.destroy()
        self.buttons = []
        self.create_controller_frame()
        self.current_path = selected_folder
        self.create_back_button()
        self.create_entries()
        self.selected_entry = None


class BrowserWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.current_path = os.path.expanduser("~")
        self.title = "Browse"
        self.geometry("800x600")
        


        def highlight_open_button(event):
            open_button.focus_set()
            return "break"  # Prevent the default behavior
        self.input_box = ctk.CTkTextbox(
            master=self,
            height=10,
            width=250,
            font=ctk.CTkFont(family="Noto Sans", size=16),
            corner_radius=1
        )
        self.input_box.insert("0.0", self.current_path)
        self.input_box.bind("<Tab>", highlight_open_button)

        button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        cancel_button = ctk.CTkButton(master=button_frame, text="Cancel", command=self.destroy)


        open_button = ctk.CTkButton(master=button_frame, text="Open", command=self.open_button_callback)
        
        self.file_scroller = FileScroller(master=self, input_box=self.input_box, current_path=self.current_path)
        self.file_scroller.pack(fill="both", expand="true", padx=10, pady=10)
        self.bind("<Up>", self.file_scroller.navigate_up)    # Bind Up arrow key
        self.bind("<Down>", self.file_scroller.navigate_down)  # Bind Down arrow key


        self.input_box.pack(fill="x", padx=10, pady=10)

        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        cancel_button.pack(side="right", padx=(10, 0))
        open_button.pack(side="right")
        def enter_key_callback(event):
            self.open_button_callback()
            return "break"
        self.input_box.bind("<Return>", enter_key_callback)
        self.bind("<Return>", enter_key_callback)


    def open_button_callback(self):
        textbox_contents = self.input_box.get("1.0", "end-1c").strip()
        if textbox_contents == "⤴..":
            # print(self.file_scroller.current_path)
            self.current_path = self.file_scroller.current_path.rsplit('/', 1)[0]
            self.file_scroller.folder_selected(selected_folder=self.current_path)
        elif textbox_contents[0] != "/":
            textbox_contents = f"/{textbox_contents}"
        if textbox_contents == self.current_path or textbox_contents == f"{self.current_path}/" or textbox_contents == "/⤴..":
            pass
        elif os.path.isdir(textbox_contents):
            self.file_scroller.folder_selected(selected_folder=textbox_contents)
            self.current_path = textbox_contents
            # print(self.current_path)
        else:
            if os.path.isdir(textbox_contents.rsplit('/', 1)[0]):
                # chatgpt, finish this
                self.master.input_box.delete("1.0", "end")
                self.master.input_box.insert("1.0", textbox_contents)
                self.destroy()
            else:
                CTkMessagebox(title="Invalid Filename", message="Invalid Filename", icon="warning", option_1="Okay")


class FrontPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.input_box = ctk.CTkTextbox(
            master=self,
            height=10,
            width=250,
            font=ctk.CTkFont(family="Noto Sans", size=16),
            corner_radius=1
        )
        self.input_box.pack(fill="x", padx=10, pady=10)

        def create_browser_window():
            browser_window = BrowserWindow(master=self)

        open_window_button = ctk.CTkButton(master=self, command=create_browser_window)
        open_window_button.pack()

def setup_gui(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    ctk.set_window_scaling(1.2)

    ctk.set_widget_scaling(1.35)

    root.geometry("800x600")

    front_page = FrontPage(root)
    front_page.pack(fill="both", expand=True)

def main():
    root = ctk.CTk()

    setup_gui(root)  # Configure GUI settings and pack main page into window.

    root.mainloop()

if __name__ == "__main__":
    main()
