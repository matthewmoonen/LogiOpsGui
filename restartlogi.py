import tkinter as tk
from tkinter import messagebox
import subprocess

def restart_logid():
    try:
        # Execute the terminal command using pkexec
        command = 'pkexec systemctl restart logid'
        subprocess.run(command, shell=True, check=True)

        messagebox.showinfo("Success", "logid service restarted successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to restart logid service.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
app = tk.Tk()
app.title("Restart logid Service")

# Create and add the button
button = tk.Button(app, text="Restart logid Service", command=restart_logid)
button.pack(pady=20)

# Run the main event loop
app.mainloop()
