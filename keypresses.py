import tkinter as tk

selected_box = None

def on_keypress(event):
    if event.keysym == 'Escape':
        if selected_box is not None:
            print("Box {} - ESC key pressed".format(selected_box))
            box_text = box_text_map[selected_box] + " ESC"
            update_box_text(selected_box, box_text)
    else:
        if selected_box is not None:
            box_text = box_text_map[selected_box] + " " + event.keysym
            print("Box {} - Key pressed: {}".format(selected_box, event.keysym))
            update_box_text(selected_box, box_text)

def on_box_click(box_number):
    global selected_box
    selected_box = box_number
    print("Box {} selected".format(box_number))

def update_box_text(box_number, text):
    if box_number in box_buttons:
        box_buttons[box_number].configure(text=text)
        box_text_map[box_number] = text

def create_window():
    root = tk.Tk()
    root.geometry("500x400")
    root.title("Click and Keypress Logger")

    label = tk.Label(root, text="Click a box and press a key:")
    label.pack(pady=10)

    global box_buttons
    box_buttons = {}

    box_names = {
        1: "Wheel Button",
        2: "Top Button",
        3: "Thumb Wheel Left",
        4: "Thumb Wheel Right",
        5: "Forward Button",
        6: "Back Button",
        7: "Thumb Button"
    }

    global box_text_map
    box_text_map = {box_number: "" for box_number in range(1, 8)}

    for box_number, box_name in box_names.items():
        box_button = tk.Button(root, text=box_name, command=lambda num=box_number: on_box_click(num))
        box_button.pack(pady=5)
        box_buttons[box_number] = box_button

    root.bind("<Key>", on_keypress)
    root.mainloop()

create_window()
