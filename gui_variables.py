import customtkinter as ctk

primary_colour = "#3A9EE9"
primary_colour1 = "#7A9DB7"
# "#9ED1F7"
secondary_colour = "#363636"

# colour1 = ("gray78", "gray28")
colour1 = "gray78"

textbox1_grey1 = "#1E2023"



grey_array = ['#242424', '#2C2C2C', '#353535', '#3D3D3D',
              '#454545', '#4D4D4D', '#565656', '#5E5E5E',
              '#666666', '#6E6E6E', '#777777', '#7F7F7F']




grey_standard1 = "#303235"
grey_standard2 = "#85888a"

standard_red1 = "#f77067"
standard_red2 = "#ef555c"
standard_red3 = "#f0544c"
standard_red4 = "#DC3545"
standard_red5 = "#da4453"
standard_red6 = "#C82333"

bg_grey1 = "#181818"
bg_grey2 = "#2B2B2B"
bg_grey3 = "#1e2023"
bg_grey4 = "#282A2C"
bg_grey5 = "#1F1F1F"
bg_grey6 = "#202020"
bg_grey7 = "#313131"

text_grey1 = "#7d7d7d"


standard_green1 = "#198754"
standard_green2 = "#28A745"
standard_green3 = "#218838"

blue_standard1 = "#62A1FE"


class Label1(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(font=ctk.CTkFont(
                                        # family="Roboto",
                                        family="Noto Sans",
                                        # family="Helvetica Neue",
                                        #  weight="bold",
                                         size=16,), 
                                        #  text_color=primary_colour1                       
                       )

class EditPageLabel1(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(font=ctk.CTkFont(
                                        # family="Roboto",
                                        # family="Noto Sans",
                                        family="Helvetica Neue",
                                         weight="bold",
                                         size=16,), 
                                        #  text_color=primary_colour1
                                         )

class MainPageLabel1(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(font=ctk.CTkFont(family="Noto Sans", weight="bold", size=20))


class MainPageLabel2(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(font=ctk.CTkFont(family="Noto Sans", weight="bold", size=16))