import tkinter as tk

def on_keypress(event):
    if event.keysym == 'Escape':
        root.quit()
    else:
        print("Key pressed:", event.keysym)

def create_window():
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Keypress Logger")

    label = tk.Label(root, text="Press any key:")
    label.pack(pady=10)

    root.bind("<Key>", on_keypress)
    root.mainloop()

create_window()
