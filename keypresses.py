import tkinter as tk

selected_box = None

def on_keypress(event):
    if event.keysym == 'Escape':
        root.quit()
    else:
        if selected_box is not None:
            print("Box {} - Key pressed: {}".format(selected_box, event.keysym))

def on_box1_click():
    global selected_box
    selected_box = 1
    print("Box 1 selected")

def on_box2_click():
    global selected_box
    selected_box = 2
    print("Box 2 selected")

def create_window():
    global root
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Click and Keypress Logger")

    label = tk.Label(root, text="Click a box and press a key:")
    label.pack(pady=10)

    box1 = tk.Button(root, text="Box 1", command=on_box1_click)
    box1.pack(pady=5)

    box2 = tk.Button(root, text="Box 2", command=on_box2_click)
    box2.pack(pady=5)

    root.bind("<Key>", on_keypress)
    root.mainloop()

create_window()
