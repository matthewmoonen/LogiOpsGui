import tkinter as tk
from tkinter import ttk


def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)


# This creates the main window that we put everything else on.
# Creates object that we will store inside window variable.
window = tk.Tk()


# Set the main title of the application
window.title('Demo')


# Set the size of the window in px
# Takes the following syntax: window.geometry('widthxheight')
window.geometry('300x150')


# Here we create our first widget
# The widget is called a label
# in Tkinter, a label is a fancy way of saying a string of text

# Here I create a new object of the "Label" class from the ttk module, and associate it with the 
# Window object as its parent, or master
# Font takes this syntax: font = 'font fontsize'
title_label = ttk.Label(master = window, text = "Miles to kilometers", font = 'Calibri 24 bold')


# To place the above label on the root window, we need to use another method.
# There are several ways to do this, but the below is the simplest
title_label.pack()


# Create an input field
# Here I want to create a text input next to a button
# Both widgets need to be inside a larger container
# We now have a frame that we can put widgets into
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable=entry_int)
button = ttk.Button(master = input_frame, text = 'Convert', command=convert)


# Now we need to take the above widgets and place them inside the frame, and then place the frame inside the window
# The side='left' argument places the input field and button next to one another
# padx and pady add padding to the widgets
entry.pack(side='left', padx=10)
button.pack(side='left')
input_frame.pack(pady=10)


# Create an output label
output_string = tk.StringVar
output_label = ttk.Label(
    master=window,
    text='Output',
    font = 'Calibri 24',
    textvariable=output_string)
output_label.pack(pady=5)


# Here we are calling the main loop
# Now we have created a basic window
window.mainloop()