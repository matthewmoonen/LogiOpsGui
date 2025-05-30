import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import time
import gui_variables
import threading
import create_cfg


class ListboxEntry(ctk.CTkButton):
    def __init__(self, browser_window=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if browser_window is not None:
            self.browser_window = browser_window
    def in_focus(self):
        self.configure(border_color=gui_variables.standard_red6)

    def out_of_focus(self):
        self.configure(border_color="#212121")



class FileScroller(ctk.CTkScrollableFrame):
    def __init__(self, master, input_box,permitted_extensions=None, create_back_button=True):
        super().__init__(master)
        self.master = master
        self.permitted_extensions = permitted_extensions
        self.input_box = input_box
        self.create_controller_frame()
        self.selected_entry = None
        self.buttons = []
        self.bind_all("<Button-4>", self.handle_scroll_up)
        self.bind_all("<Button-5>", self.handle_scroll_down)
        self.create_back_button()
        self.create_entries()

    def bind_file_click(self, button_text):
        self.input_box.delete("0.0", "end")
        self.input_box.insert("0.0", f"{self.master.current_path}/{button_text}/")



    def create_controller_frame(self):
        self.controller_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.controller_frame.pack(fill="both", expand="true")

    def create_button(self, button_text, is_folder=False):
        button = ListboxEntry(master = self.controller_frame, browser_window=self.master, text=button_text, corner_radius=0, height=45, border_width=2, border_color="#212121", font=ctk.CTkFont(family="Noto Sans",size=14), fg_color="transparent", text_color=("gray70"), hover_color=("gray15"), anchor="w")

        if is_folder == True:
            button.bind('<Button-1>', lambda event, button_text=button_text: self.clicked_button(button_text))
        else:
            button._text_label.grid(padx=30)
            def make_button_allowed():
                button.bind('<Button-1>', lambda event, button_text=button_text: self.bind_file_click(button_text=button_text))

            if self.permitted_extensions is not None:
                if "." not in button_text or button_text.rstrip().rsplit('.', 1)[1] not in self.permitted_extensions:
                    button.configure(text_color="gray40")
                else:
                    make_button_allowed()
            else:
                make_button_allowed()
                
        button.pack(fill="x")
        self.buttons.append(button)

    def create_back_button(self):
        if self.master.current_path not in ["/",""]:

            button = ListboxEntry(master = self.controller_frame, text="⤴..", corner_radius=0, height=10, border_width=2, border_color="#212121", font=ctk.CTkFont(family="Noto Sans",size=18 ), fg_color="gray15", text_color=("gray70"), hover_color=("gray20"), anchor="w")
            button.pack(fill="x", expand=True)
            button.bind('<Button-1>', lambda event: self.back_button_clicked())
            self.buttons.append(button)
            

    def folder_clicked(self, selected_folder):
        
        if hasattr(self.master, "reminder_button"):
            self.master.reminder_button.pack_forget()

        self.controller_frame.destroy()
        self.buttons = []
        self.create_controller_frame()
        if len(selected_folder)>0 and selected_folder[0] == "/":
            self.master.current_path = selected_folder
        elif len(selected_folder) == 0 and len(self.master.current_path) == 0:
            self.master.current_path = "/"
        else:
            self.master.current_path = f"{self.master.current_path}/{selected_folder}"
        self.create_back_button()
        self.create_entries()
        self._parent_canvas.yview_moveto(0)
        self.selected_entry = None

    def clicked_button(self, button_text):
        if hasattr(self.master, "reminder_button"):
            self.master.reminder_button.pack_forget()

        self.input_box.delete("0.0", "end")
        if self.master.current_path == "/":
            self.input_box.insert("0.0", f"/{button_text}/")
        else:
            self.input_box.insert("0.0", f"{self.master.current_path}/{button_text}/")
        self.folder_clicked(selected_folder=button_text)


    def back_button_clicked(self):
        if hasattr(self.master, "reminder_button"):
            self.master.reminder_button.pack_forget()

        self.input_box.delete("0.0", "end")
        if self.master.current_path != "/":
            new_path = self.master.current_path.rsplit('/', 1)[0]
            if new_path == "":
                self.master.current_path = "/"
                # self.master.current_path = "/"
            else:
                # self.master.current_path = new_path
                self.master.current_path = new_path
            self.input_box.insert("0.0", f"{self.master.current_path}/")
            self.folder_clicked(selected_folder=self.master.current_path)
            if self.master.current_path == "/":
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", "/")

        else:
            self.input_box.insert("0.0", "/")

    def create_folder_buttons(self, folders):
        for folder in folders:
            if self.master.current_path != "/" or folder != "bin":
                self.create_button(button_text=folder, is_folder=True)

            
        
    def create_file_buttons(self, files):
        for file in files:
            self.create_button(button_text=f"{file}")

    def navigate_down(self, event):
        self.master.focus_set()
        if self.selected_entry == None:
            self.input_box.delete("0.0", "end")
            if len(self.buttons) == 1:
                self.buttons[0].in_focus()
                self.selected_entry = 0
                self.input_box.insert("0.0", self.buttons[0]._text)
            else:
                self.buttons[1].in_focus()
                self.selected_entry = 1
                if self.master.current_path == "/":
                    self.input_box.insert("0.0", "/" + self.buttons[self.selected_entry]._text)
                else:
                    self.input_box.insert("0.0", self.master.current_path + "/" + self.buttons[self.selected_entry]._text)
        elif self.selected_entry == len(self.buttons) - 1:
            if len(self.buttons) == 1:
                self.buttons[self.selected_entry].out_of_focus()
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.master.current_path)
                self.selected_entry = None
        else:
            self.buttons[self.selected_entry].out_of_focus()
            self.selected_entry = self.selected_entry + 1
            self.buttons[self.selected_entry].in_focus()
            self.input_box.delete("0.0", "end")
            if self.master.current_path == "/":
                self.input_box.insert("0.0", self.master.current_path + self.buttons[self.selected_entry]._text)
            else:
                self.input_box.insert("0.0", self.master.current_path + "/" + self.buttons[self.selected_entry]._text)
            

    def navigate_up(self, event):
        self.master.focus_set()
        if self.selected_entry == None:
            self.input_box.delete("0.0", "end")
            if len(self.buttons) == 1:
                self.buttons[0].in_focus()
                self.selected_entry = 0
                self.input_box.insert("0.0", self.buttons[0]._text)
            else:
                self.buttons[1].in_focus()
                self.selected_entry = 1
                if self.master.current_path != "/":
                    self.input_box.insert("0.0", self.master.current_path + "/" + self.buttons[self.selected_entry]._text)
                else:
                    self.input_box.insert("0.0", f"/{self.buttons[self.selected_entry]._text}")
        elif self.selected_entry == 0:
            if len(self.buttons) == 1:
                self.buttons[self.selected_entry].out_of_focus()
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.master.current_path)
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
            if self.master.current_path == "/":
                self.input_box.insert("0.0", self.master.current_path + self.buttons[self.selected_entry]._text)
            else:
                self.input_box.insert("0.0", self.master.current_path + "/" + self.buttons[self.selected_entry]._text)

    def create_entries(self):
        self.focus_set()
        folders = []
        files = []

        if self.master.current_path.count('/') == 0:
            # self.current_path = "/"
            self.master.current_path = "/"
        if len(self.master.current_path) > 1 and self.master.current_path[1] == "/":
            # self.current_path = self.current_path[1:]
            self.master.current_path = self.master.current_path[1:]

        entries = os.listdir(self.master.current_path)
        for entry in entries:
            if not entry.startswith('.'): 
                full_path = os.path.join(self.master.current_path, entry)
                if os.path.isdir(full_path):
                    folders.append(entry)
                else:
                    files.append(entry)
        self.create_folder_buttons(sorted(folders))
        self.create_file_buttons(sorted(files))

    def folder_selected(self, selected_folder):
        if hasattr(self.master, "reminder_button"):
            self.master.reminder_button.pack_forget()

        if selected_folder != "/bin":
            self.controller_frame.destroy()
            self.buttons = []
            self.create_controller_frame()
            # self.current_path = selected_folder
            self.master.current_path = selected_folder
            self.create_back_button()
            self.create_entries()
            self.selected_entry = None
        else:
            # self.current_path = "/"
            self.master.current_path = "/"
            self.selected_entry = None

    def handle_scroll_up(self, event):
        if self._parent_canvas.winfo_height() < self.winfo_height():
            self._parent_canvas.yview_scroll(-1, "units")
            
    def handle_scroll_down(self, event):
        if self._parent_canvas.winfo_height() < self.winfo_height():
            self._parent_canvas.yview_scroll(1, "units")



class BrowserWindow(ctk.CTkToplevel):
    def __init__(self, master, current_path=None, current_filename='', on_select=None, permitted_extensions=None, default_extension=None, warn_invalid_folder=False):
        super().__init__(master,)

        self.master=master
        self.title("Save Configuration")
        self.current_filename = f"/{current_filename}"
        self.default_extension = default_extension
        self.warn_invalid_folder = warn_invalid_folder


        if current_path is not None:
            self.current_path = current_path
        else:
            self.current_path = os.path.expanduser("~")
        self.geometry("1000x700")
        self.on_select=on_select
        if isinstance(permitted_extensions, str):
            self.permitted_extensions = (permitted_extensions,)
        elif isinstance(permitted_extensions, (tuple, list)):
            self.permitted_extensions = permitted_extensions
        else:
            self.permitted_extensions = None

        def tab_button_pushed(event):
            # TODO: add autocomplete functionality similar to terminal.
            return "break"
        
        def on_key_press(event):
            def handle_ctrl_backspace():
                cursor_position = self.input_box.index(ctk.INSERT) 
                
                if cursor_position == '1.0':
                    return
                
                line, column = map(int, cursor_position.split('.'))

                text_before_cursor = self.input_box.get("1.0", f"{line}.{column}")
                    
                if text_before_cursor[-1] in (" ", "/"):
                    self.input_box.delete("insert-1c")
                    handle_ctrl_backspace() # Recursively call function to handle multiple spaces or slashes at the end of the string.

                last_slash_index = text_before_cursor.rfind('/')
                last_space_index = text_before_cursor.rfind(' ')
                
                delete_to_index = max(last_slash_index, last_space_index)

                if delete_to_index != -1:
                    self.input_box.delete(f"1.0 + {delete_to_index + 2} chars", ctk.INSERT)
                else:
                    self.input_box.delete("1.0", ctk.INSERT)


            if event.keysym == 'BackSpace' and event.state & 0x0004:

                handle_ctrl_backspace()


        self.input_box = ctk.CTkTextbox(
            master=self,
            height=10,
            width=250,
            font=ctk.CTkFont(family="Noto Sans", size=16),
            corner_radius=1
        )

        if not os.path.isdir(self.current_path):
            self.current_path = os.path.expanduser("~")
            self.current_filename = "/logid.cfg"
        self.input_box.insert("0.0", f"{self.current_path}{self.current_filename}")
        self.input_box.bind("<Tab>", tab_button_pushed)
        self.input_box.bind("<KeyPress>", on_key_press)
        
        def handle_keypresses(event):
            box_text = self.input_box.get("1.0", "end-1c")
            is_dir = os.path.isdir(box_text)
            if box_text.endswith("/") == True:
                box_text = box_text[:-1]
            if is_dir and box_text != self.current_path or box_text == "⤴..":
                self.open_button.configure(text="Open")
            else:
                self.open_button.configure(text="Save")

            if self.file_scroller.selected_entry is not None and event.keysym not in ["Up", "Down", "Left", "Right"] or event.keysym == 'Up' and event.state & 0x0008 and self.current_path in ["", "/"]:
                self.file_scroller.buttons[self.file_scroller.selected_entry].out_of_focus()
                self.file_scroller.selected_entry = None
                if self.current_path in ["", "/"] and event.keysym == "Up":
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", "/")    
                
            if hasattr(self, "reminder_button"):
                self.reminder_button.destroy()
            if event.keysym == 'l' and event.state & 0x0004:
                self.input_box.focus_set()
            elif event.keysym == 'Up' and event.state & 0x0008 and self.current_path not in ["", "/"]:
                self.file_scroller.back_button_clicked()
        
        
        self.bind("<KeyPress>", handle_keypresses)
        def input_focusin(event):
            if self.input_box.get("1.0", "end-1c") == "⤴..":
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", self.current_path)
            handle_keypresses(event)
        self.input_box.bind("<FocusIn>", input_focusin)
        
        def input_focusout(event):
            if self.input_box.get("1.0", "end-1c") in ["", "/"] and len(self.current_path) > 1:
                self.input_box.insert("0.0", self.current_path)

        self.input_box.bind("<FocusOut>", input_focusout)

        self.button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        cancel_button = ctk.CTkButton(master=self.button_frame, text="Cancel", command=self.destroy, height=40, width=150, hover_color="#606060", corner_radius=0, fg_color="#555555", text_color="gray80", font=ctk.CTkFont(size=15))
        self.open_button = ctk.CTkButton(master=self.button_frame, text="Save", command=self.open_button_callback, height=40, width=150, fg_color="#0071C2", corner_radius=0, hover_color="#0091EA", font=ctk.CTkFont(size=16))
        
        self.file_scroller = FileScroller(master=self, input_box=self.input_box, permitted_extensions=self.permitted_extensions,)
        self.file_scroller.pack(fill="both", expand="true", padx=10, pady=10)
        def go_up(event):
            self.file_scroller.navigate_up(event)
            handle_keypresses(event)
        def go_down(event):
            self.file_scroller.navigate_down(event)
            handle_keypresses(event)
        self.bind("<Up>", go_up)
        self.bind("<Down>", go_down)
        

        self.input_box.pack(fill="x", padx=10, pady=10)

        self.button_frame.pack(fill="x", padx=10, pady=(10, 20))

        cancel_button.pack(side="right", padx=(25, 0))
        self.open_button.pack(side="right")

        def returnkey(event=None):
            current_focus = self.input_box.focus_get()

            reset_focus = False
            if str(current_focus).startswith(str(self.input_box)):
                reset_focus = True

            tc=self.input_box.get("1.0", "end-1c")
            self.open_button_callback(textbox_contents=tc)

            if reset_focus:
                self.input_box.focus_set()
                
            return "break"
            

        self.bind("<Return>", returnkey)


    def open_button_callback(self, event=None, textbox_contents=None):

        if textbox_contents == None:
            textbox_contents = self.input_box.get("1.0", "end-1c")

        if "\n" in textbox_contents:
            textbox_contents = textbox_contents.replace("\n", "")

        if textbox_contents in ["/", "\n" "//", "///", "////", " /", " //", " ///", " ////", "/ ", "// ", "/// ", "//// ",]:
            self.input_box.delete("0.0", "end")
            self.input_box.insert("0.0", self.current_path)
            return

        textbox_contents = textbox_contents.rstrip(" ").rstrip("/")

        if "//" in textbox_contents:
            textbox_contents=textbox_contents.replace("//", "/")
            self.open_button_callback(textbox_contents=textbox_contents)


        def open_reminder():
            
            self.input_box.focus_set()
            if hasattr(self, "reminder_button"):
                self.reminder_button.pack_forget()
            self.reminder_button = ctk.CTkButton(master=self.button_frame, text="Enter file name", fg_color="transparent", border_color=gui_variables.standard_red5, border_width=0, corner_radius=0, hover="false", font=ctk.CTkFont(size=12), text_color=gui_variables.standard_red6)
            self.reminder_button.pack(side="left", fill="x", expand="true", padx=20)
            return

        if textbox_contents in ["⤴..", "/⤴..", "/⤴../", "⤴../", "/"]:
            self.current_path = self.current_path.rsplit('/', 1)[0]

            self.file_scroller.folder_selected(selected_folder=self.current_path)
            
            self.input_box.delete("0.0", "end")
            if self.current_path not in ["", "/"]:
                self.input_box.insert("0.0", f"{self.current_path}/")
            else:
                self.input_box.insert("0.0", "/")

        elif textbox_contents == "":
            self.input_box.insert("0.0", f"{self.current_path}/")

        elif textbox_contents in ["bin", "/bin", "//bin"]:
            pass
        else:

            if textbox_contents[0] != "/":
                textbox_contents = f"/{textbox_contents}"

            if textbox_contents in [self.current_path, f"{self.current_path}/"]:
                open_reminder()
                if textbox_contents[-1] != "/":
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", f"{self.current_path}/")

            elif os.path.isdir(textbox_contents):
                self.file_scroller.folder_selected(selected_folder=textbox_contents)
                self.current_path = textbox_contents
                self.input_box.delete("0.0", "end")
                self.input_box.insert("0.0", f"{self.current_path}/")
            else:
                directory, filename = textbox_contents.rsplit('/', 1)

                if not os.path.isdir(directory):
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", f"{self.current_path}/")
                    if self.warn_invalid_folder:
                        CTkMessagebox(title="Invalid Filename", message="Folder does not exist", icon="warning", option_1="OK", width=600, height=300, fade_in_duration=200)

                elif "." not in filename and self.default_extension is not None and filename[0] != " ":
                    if self.current_path == directory:
                        self.input_box.delete("0.0", "end")
                        self.input_box.insert("0.0", f"{self.current_path}/{filename}.{self.default_extension}")

                elif len(filename) > 1 and filename.rsplit('.', 1)[1] not in self.permitted_extensions:
                    box_text = self.input_box.get("1.0", "end-1c")
                    box_text.replace("\n", "")
                    self.input_box.delete("0.0", "end")
                    self.input_box.insert("0.0", box_text)
                    format_message = self.permitted_extensions[0] if len(self.permitted_extensions) == 1 else ", ".join(self.permitted_extensions)
                    CTkMessagebox(title="Invalid Filename", message=f"Invalid Format. File must be .{format_message}", icon="warning", option_1="OK", width=600, height=300, fade_in_duration=200)

                else:
                    overwrite = BrowserWindow.check_overwrite(path_to_check=textbox_contents, filename=filename)
                    if overwrite in [None, True]:

                        try_generating = create_cfg.generate_in_user_chosen_directory(overwrite=overwrite, save_directory=textbox_contents)
                        
                        if type(try_generating) == PermissionError:
                            self.input_box.delete("0.0", "end")
                            self.input_box.insert("0.0", textbox_contents)
                            CTkMessagebox(title="Error", message="Could not write to this location", icon="cancel", option_1="OK", width=600, height=300, fade_in_duration=200)
                            return

                        else:
                            status, info = try_generating
                            if status == create_cfg.Status.SUCCESS:
                                self.master.cfg_location = directory
                                self.master.cfg_filename = filename
                                self.destroy()
                                create_cfg.set_cfg_location(directory, filename)


    @staticmethod
    def check_overwrite(path_to_check, filename):
        if os.path.exists(path=path_to_check):
            message = CTkMessagebox(title="test", message=f"The file {filename} already exists. Do you wish to overwrite it?", option_2="Overwrite", option_1="Cancel", width=600, height=300, fade_in_duration=200)
            if message.get() == "Overwrite":
                return True
            else:
                return False
        else:
            return None

