import customtkinter as ctk
import cairosvg
from PIL import Image
import io
from typing import Callable



def svg_to_image(path, output_width=300, output_height=300):
    with open(path, 'rb') as svg_file:
        svg_content = svg_file.read()
    png_data = cairosvg.svg2png(bytestring=svg_content, output_width=output_width, output_height=output_height)
    return ctk.CTkImage(Image.open(io.BytesIO(png_data)), size=(output_width, output_height))
    
    """
    Some UI elements have rendering issues in CustomTkinter on Linux, radio buttons in particular look blocky.
    
    These class creates smooth-looking radio buttons using SVG files.
    
    See here for further information:
    https://github.com/TomSchimansky/CustomTkinter/issues/1384
    """

class MatthewsRadioButton:

    def __init__(self, master, text, font=None, command=None, hover_elements=None, selected_image_path="images/radio_button_selected.svg", deselected_image_path="images/radio_button_deselected.svg", hover_image_path="images/radio_button_hover.svg", icon_size=27, width=400, height=None, fg_color="transparent",):

        self.radio_button_selected = svg_to_image(path=selected_image_path, output_height=icon_size, output_width=icon_size)
        self.radio_button_deselected = svg_to_image(path=deselected_image_path, output_height=icon_size, output_width=icon_size)
        self.radio_button_hover = svg_to_image(path=hover_image_path, output_height=icon_size, output_width=icon_size)
        self.user_command = command
        self.hover_elements = None

        if height is None: # Set height to icon_size if not explicitly set
            height = icon_size

        if font == None:
            font=ctk.CTkFont(family="Noto Sans", size=17)

        self.button = ctk.CTkButton(master=master, text=text, image=self.radio_button_deselected, command=self.radio_button_clicked, anchor="w", font=font, text_color="gray65", height=height, width=width, fg_color=fg_color, hover=False)
        self.button.bind('<Enter>', lambda event: self.radio_button_enter(event))
        self.button.bind('<Leave>', lambda event: self.radio_button_leave(event))
        if hover_elements is not None:
            self.hover_elements = hover_elements
            if not isinstance(hover_elements, tuple):
                self.hover_elements = (hover_elements,)
            for i in self.hover_elements:
                i.bind('<Enter>', lambda event: self.radio_button_enter(event))
                i.bind('<Leave>', lambda event: self.radio_button_leave(event))
                i.bind('<Button-1>', self.radio_button_clicked)

        self.is_selected = False

    def radio_button_enter(self, event):
        self.button.configure(image=self.radio_button_hover)

    def radio_button_leave(self, event):
        self.button.configure(image=self.radio_button_deselected)
        # self.button.configure('<Leave>', text_color="gray65")

    def another_button_clicked(self):
        try:
            self.button.configure(image=self.radio_button_deselected)
            self.is_selected = False
            self.button.bind('<Enter>', lambda event: self.radio_button_enter(event))
            self.button.bind('<Leave>', lambda event: self.radio_button_leave(event))
            if self.hover_elements is not None:
                for i in self.hover_elements:
                    i.bind('<Enter>', lambda event: self.radio_button_enter(event))
                    i.bind('<Leave>', lambda event: self.radio_button_leave(event))
        except:
            pass

    def set_clicked(self):
        self.is_selected = True

        self.button.unbind('<Enter>')
        self.button.unbind('<Leave>')
        if self.hover_elements is not None:
            for i in self.hover_elements:
                i.unbind('<Enter>')
                i.unbind('<Leave>')
        self.button.configure(image=self.radio_button_selected)

    def radio_button_clicked(self, event=None):
        if self.is_selected: # If the button is already selected, just return without changing anything
            return

        self.set_clicked()

        if self.user_command: # Run the user's command, if provided
            self.user_command()

    def grid(self, **kwargs):
        self.button.grid(**kwargs)
    
    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def update_text(self, new_text):
        """Update the text of the radio button."""
        self.button.configure(text=new_text)

class FloatSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: float = 1.0, min_value: float = None, 
                 max_value: float = None, decimal_places: int = 1, command: Callable = None, db_query=None, value=None, **kwargs):
        super().__init__(*args, width=1, height=1, corner_radius=0, fg_color="transparent", **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places
        self.command = command
        self.db_query = db_query
        self.value = value if value is not None else (min_value if min_value is not None else 0.0)

        self.enabled = True  # Initial state is enabled

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)  # entry expands


        self.subtract_button = ctk.CTkButton(self, text="-", width=height+5, height=height, command=self.subtract_button_callback, fg_color="#0071C2", hover_color="#0089EB", font=ctk.CTkFont(size=int(height*0.55)), corner_radius=0)
        # self.subtract_button = ctk.CTkButton(self, text="-", width=height-2, height=height-2, command=self.subtract_button_callback)
        # self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.subtract_button.grid(row=0, column=0, padx=int(height*0.15), pady=int(height*0.15))

        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'), justify="center", width=width-(2.8*height), height=int(height*1.2), border_width=0, font=ctk.CTkFont(size=int(height*0.53)), corner_radius=0)
        # self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'), width=width-(2.8*height), height=height-4, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.insert(0, self.format_value(self.value))

        # self.add_button = ctk.CTkButton(self, text="+", width=height-2.5, height=height-2.5, command=self.add_button_callback)
        self.add_button = ctk.CTkButton(self, text="+", width=height+5, height=height, command=self.add_button_callback,fg_color="#0071C2",hover_color="#0089EB", font=ctk.CTkFont(size=int(height*0.55)), corner_radius=0)
        # self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.add_button.grid(row=0, column=2, padx=int(height*0.15), pady=int(height*0.15))

        self.entry.bind("<FocusOut>", self.on_focus_out)

    def format_value(self, value):
        return f"{value:.{self.decimal_places}f}"

    def validate(self, new_text):
        if new_text in ("", "-"):
            return True
        try:
            float(new_text)
            return True
        except ValueError:
            return False

    def on_focus_out(self, event):
        try:
            value = float(self.entry.get())
            value = max(self.min_value, value) if self.min_value is not None else value
            value = min(self.max_value, value) if self.max_value is not None else value
        except ValueError:
            value = self.value  # Use stored value if parsing fails

        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()

    def add_button_callback(self):
        try:
            value = float(self.entry.get())
            value = value + self.step_size
            value = min(self.max_value, value) if self.max_value is not None else value
        except ValueError:
            return
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()

    def subtract_button_callback(self):
        try:
            value = float(self.entry.get())
            value = value - self.step_size
            value = max(self.min_value, value) if self.min_value is not None else value
        except ValueError:
            return
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        if self.value != value:
            self.value = value
            self.run_db_query()
            self.run_command()

    def get(self) -> float:
        try:
            return float(self.entry.get())
        except ValueError:
            return self.value

    def set(self, value: float):
        value = max(self.min_value, value) if self.min_value is not None else value
        value = min(self.max_value, value) if self.max_value is not None else value
        self.entry.delete(0, "end")
        self.entry.insert(0, self.format_value(value))
        self.value = value

    def toggle_enable(self, new_enabled_state):
        self.enabled = new_enabled_state
        state = "normal" if self.enabled else "disabled"
        self.entry.configure(state=state)
        self.add_button.configure(state=state)
        self.subtract_button.configure(state=state)

    def run_command(self):
        if callable(self.command):
            self.command()

    def run_db_query(self):
        if callable(self.db_query):
            self.db_query(self.value)

class IntSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: int = 1, min_value: int = None, max_value: int = None,  command: Callable = None, db_query = None, value=None, **kwargs):
        super().__init__(*args, width=1, height=1, corner_radius=0, fg_color="transparent", **kwargs)
        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.command = command
        self.db_query = db_query
        self.value = value
        self.enabled = True  
        self.grid_columnconfigure((0, 2), weight=0) 
        self.grid_columnconfigure(1, weight=1)
        self.subtract_button = ctk.CTkButton(self, text="-", width=height+5, height=height, command=self.subtract_button_callback, fg_color="#0071C2", hover_color="#0089EB", font=ctk.CTkFont(size=int(height*0.55)), corner_radius=0)
        self.subtract_button.grid(row=0, column=0, padx=int(height*0.15), pady=int(height*0.15))
        self.default_value = 0 if min_value is None else min_value 
        vcmd = self.register(self.validate)
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(vcmd, '%P'), justify="center", width=width-(2.8*height), height=int(height*1.2), border_width=0, font=ctk.CTkFont(size=int(height*0.53)), corner_radius=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=0, pady=int(height*0.15), sticky="ew")
        self.entry.bind("<FocusOut>", self.on_focus_out)  
        self.add_button = ctk.CTkButton(self, text="+", width=height+5, height=height, command=self.add_button_callback,fg_color="#0071C2",hover_color="#0089EB", font=ctk.CTkFont(size=int(height*0.55)), corner_radius=0)
        self.add_button.grid(row=0, column=2, padx=int(height*0.15), pady=int(height*0.15))
        self.entry.insert(0, ["0" if self.value == None else self.value]) 

    def validate(self, new_text):
        if new_text == "":
            return True
        if self.min_value < 0:
            if new_text == "-":
                return True        
        try:
            int(new_text)
            return True
        except ValueError:
            return False

    def on_focus_out(self, event):
        try:
            value = int(self.entry.get())
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
        except ValueError:
            value = self.default_value

        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        if self.value != value:
            self.value = value
            self.run_db_query()

    def add_button_callback(self):
        try: 
            value = int(self.entry.get()) // self.step_size * self.step_size + self.step_size # Set new value to closest multiple of step size after the current value
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            if self.value != value:
                self.value = value
                self.run_db_query()
        except ValueError:
            return

    def run_db_query(self):
        if callable(self.db_query):
            self.db_query(self.value)

    def subtract_button_callback(self):
        try:
            def get_nearest_rounded_value(): # Set new value to closest multiple of step size after the current value
                previous_value = int(self.entry.get())
                return previous_value // self.step_size * self.step_size - self.step_size if previous_value % self.step_size == 0 else previous_value // self.step_size * self.step_size
            value = get_nearest_rounded_value()
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            if self.value != value:
                self.value = value
                self.run_db_query()
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
        self.value = value

    def toggle_enable(self, new_enabled_state):
        self.enabled = new_enabled_state
        state = "normal" if self.enabled else "disabled"
        self.entry.configure(state=state)
        self.add_button.configure(state=state)
        self.subtract_button.configure(state=state)
